import re
from typing import Tuple


def regex_range(string: str) -> range:
    """Split a string like '11-16' into range(11, 17)."""
    match = re.search(r"(\d+)-(\d+)", string)
    if match:
        return range(int(match.group(1)), int(match.group(2)) + 1)
    match = re.search(r"(\d+)\+", string)
    if match:
        return range(int(match.group(1)), 99)

    raise ValueError(string)


def regex_dice_str(string: str) -> Tuple[int, int, int]:
    string = str(string).replace(" ", "")
    match = re.match(r"(\d+)d(\d+)", string)
    if match:
        num = int(match.group(1))
        die = int(match.group(2))
    else:
        match = re.match(r"(\d+)", string)
        if match:
            die = int(match.group(1))
            num = 1
        else:
            return None, None, None

    match = re.search(r"x(\d+)", string)
    if match:
        multiply = int(match.group(1))
    else:
        multiply = 1

    return die, num, multiply
