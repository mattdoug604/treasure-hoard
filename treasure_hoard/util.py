import random
from collections import OrderedDict
from typing import Dict


def convert_to_gp(item_dict: Dict) -> Dict:
    temp = OrderedDict()
    for item, count in item_dict.items():
        if item == "CP":
            # 100 cp == 1 gp
            temp["GP"] = temp.get("GP", 0) + 0.01 * count
        elif item == "SP":
            # 10 sp == 1 gp
            temp["GP"] = temp.get("GP", 0) + 0.1 * count
        elif item == "GP":
            # 1 gp == 1 gp
            temp["GP"] = temp.get("GP", 0) + count
        elif item == "EP":
            # 2 ep == 1 gp
            temp["GP"] = temp.get("GP", 0) + 0.5 * count
        elif item == "PP":
            # 1 p == 10 gp
            temp["GP"] = temp.get("GP", 0) + 10 * count
        else:
            temp[item] = count

    # convert gp to a whole number
    temp["GP"] = round(temp.get("GP", 0))

    return temp


def roll(die_max: int, die_min: int = 1, num_die: int = 1, multiply: int = 1) -> int:
    return sum([random.randint(die_min, die_max) for i in range(num_die)]) * multiply
