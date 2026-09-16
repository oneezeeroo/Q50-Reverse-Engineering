#!/usr/bin/env python3
"""Read-only Q50 / Connexis EPK v2 structure inspector."""

import argparse
import struct
from pathlib import Path

MAGIC = b".epk"
KEY_FIELD_SIZE = 256
NAME_FIELD_SIZE = 128


def read_exact(handle, size):
    data = handle.read(size)
    if len(data) != size:
        raise ValueError(f"unexpected EOF: wanted {size} bytes, got {len(data)}")
    return data


def inspect_epk(filename):
    path = Path(filename)

    with path.open("rb") as f:
        magic = read_exact(f, 4)

        if magic != MAGIC:
            raise ValueError(f"not an EPK file: magic={magic!r}")

        version = struct.unpack(">H", read_exact(f, 2))[0]
        payload_type = struct.unpack(">H", read_exact(f, 2))[0]
        block_count = struct.unpack(">H", read_exact(f, 2))[0]
        key_size = struct.unpack(">H", read_exact(f, 2))[0]

        if key_size > KEY_FIELD_SIZE:
            raise ValueError(f"invalid wrapped-key length: {key_size}")

        read_exact(f, KEY_FIELD_SIZE)

        print(f"file:         {path}")
        print(f"magic:        {magic.decode('ascii')}")
        print(f"version:      {version}")
        print(f"payload type: {payload_type}")
        print(f"blocks:       {block_count}")
        print(f"key length:   {key_size} bytes")

        for block in range(block_count):
            raw_name = read_exact(f, NAME_FIELD_SIZE)
            name = raw_name.split(b"\x00", 1)[0].decode("ascii", errors="replace")
            encrypted_len = struct.unpack(">I", read_exact(f, 4))[0]
            data_offset = f.tell()

            print(
                f"block {block + 1}: "
                f"name={name!r}, encrypted={encrypted_len} bytes, "
                f"data_offset=0x{data_offset:X}"
            )

            f.seek(encrypted_len, 1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Inspect the structure of a Q50 / Connexis EPK v2 file"
    )
    parser.add_argument("epk", help="path to the EPK file")
    args = parser.parse_args()

    inspect_epk(args.epk)
