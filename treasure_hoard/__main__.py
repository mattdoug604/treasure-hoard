#!/usr/bin/env python
import argparse
import logging
import re
from typing import List

from .database import Database
from .util import convert_to_gp


def build_parser():
    parser = argparse.ArgumentParser(
        description="Generate a treasure hoard for D&D 5e.", add_help=False
    )
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-c",
        "--cr",
        type=int,
        required=True,
        help="monster's CR, or average level of the party",
    )
    optional = parser.add_argument_group("optional arguments")
    optional.add_argument(
        "-r", "--roll", type=int, help="aligned reads in SAM or BAM format"
    )
    optional.add_argument(
        "-g", "--convert-to-gp", action="store_true", help="convert all coins to gp"
    )
    optional.add_argument(
        "-v", "--verbose", action="store_true", help="print additional information"
    )
    optional.add_argument(
        "-h", "--help", action="help", help="show this help message and exit"
    )

    return parser


def main(argvl: List = []) -> None:
    parser = build_parser()
    if argvl:
        args = parser.parse_args(argvl)
    else:
        args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    item_dict = Database().get_hoard(args.cr, args.roll)

    if args.convert_to_gp:
        item_dict = convert_to_gp(item_dict)

    for item, count in item_dict.items():
        if re.match(r"[A-Z]P", str(item)):
            print(f"{count:,} {item}")
        else:
            if count == 1:
                print(item)
            elif count > 1:
                print(f"{count:,}x {item}")


if __name__ == "__main__":
    main()
