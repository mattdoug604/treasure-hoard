import logging
import os.path
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List

import pandas

from .regex import regex_dice_str, regex_range
from .util import roll


DATA_PATH = Path(os.path.dirname(__file__)) / "data" / "data.xlsx"


class Item:
    def __init__(self, name: str, source: str, extras: List[str] = []):
        self.name = name.strip()
        self.source = source
        self.extras = extras

    def __str__(self):
        if self.extras:
            return f"{self.name} ({'; '.join(self.extras)})"
        else:
            return self.name

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return self != other


class Table:
    def __init__(self, data: pandas.core.frame.DataFrame, name: str) -> None:
        self.data = data
        self.name = name

    def __str__(self):
        return self.name

    @property
    def min_roll(self) -> range:
        return min(self.data["Min Roll"])

    @property
    def max_roll(self) -> range:
        return max(self.data["Max Roll"])

    def roll(self) -> int:
        return roll(die_max=self.max_roll, die_min=self.min_roll)

    def _select_row(self, user_roll: int) -> pandas.core.frame.DataFrame:
        return self.data[
            (self.data["Min Roll"] <= user_roll) & (self.data["Max Roll"] >= user_roll)
        ]


class HoardTable(Table):
    def get(self, user_roll: int = None) -> Dict[str, int]:

        item_dict = OrderedDict()

        def add_item(item, count=1):
            if item in item_dict:
                item_dict[item] += count
            else:
                item_dict[item] = count

        if user_roll is None:
            user_roll = self.roll()
            logging.info(f"'{self}' rolled {user_roll}")

        values = self._select_values(user_roll)
        for column, value in values.items():
            die, num, multiply = regex_dice_str(value)
            count = roll(die_max=die, num_die=num, multiply=multiply) if die else 0
            if column in Database.item_tables:
                for _ in range(count):
                    item = Database.item_tables[column].get()
                    add_item(item)
            else:
                item = Item(column, column)
                add_item(item, count=count)
                logging.info(f"{count} rolled for '{item}'")

        return item_dict

    def _select_values(self, user_roll: int = None) -> Dict[str, str]:
        row = self._select_row(user_roll)
        row = row.drop(["Min Roll", "Max Roll"], axis=1)
        return {k: v.values[0] for k, v in row.items()}


class ItemTable(Table):
    def get(self, user_roll: int = None) -> str:
        if user_roll is None:
            user_roll = self.roll()
            logging.info(f"'{self}' rolled {user_roll}")

        value = self._select_value(user_roll)
        if value in Database.item_tables:
            return Database.item_tables[value].get()
        else:
            extras = self._select_extras(user_roll)
            return Item(value, self.name, extras)

        return value

    def _select_value(self, user_roll: int = None) -> str:
        row = self._select_row(user_roll)
        return row.iloc[:, 2].values[0]

    def _select_extras(self, user_roll: int = None) -> List[str]:
        row = self._select_row(user_roll)
        return list(row.iloc[:, 3:].values[0])


class Database:

    hoard_tables = {}
    item_tables = {}

    @classmethod
    def load(cls, path: str) -> None:
        sheet_dict = pandas.read_excel(path, sheet_name=None)
        for name, df in sheet_dict.items():
            if name.startswith("Treasure Hoard CR"):
                cls.hoard_tables[name] = HoardTable(df, name)
                logging.info(f"Loaded hoard table: {name}")
            else:
                cls.item_tables[name] = ItemTable(df, name)
                logging.info(f"Loaded item table: {name}")

    def get_hoard(self, cr: int, user_roll: int = None) -> Dict[str, int]:
        table = self._select_hoard_table(cr)
        return table.get(user_roll)

    def _select_hoard_table(self, cr: int) -> HoardTable:
        for name in self.hoard_tables:
            if cr in regex_range(name):
                logging.info(f"selected hoard table: {name}")
                return self.hoard_tables[name]


Database.load(DATA_PATH)
