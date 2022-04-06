import sys
import argparse
from typing import List, Tuple


class MailsyncArgumentParser(argparse.ArgumentParser):

    """ This argument parser extends the standard library argument parser """

    def __init__(self):
        super().__init__()

        arguments_std = []

        arguments_bool = [
            ("--print-keys",
             "Print secret and public keys (useful for debugging home directory)",
             False),
        ]

        self.add_standard_arguments(arguments_std)
        self.add_boolean_arguments(arguments_bool)

    def add_standard_arguments(self, arguments_std: List[Tuple[str, str, bool, type]]) -> None:
        for flag, helpstr, defaultval, dtype in arguments_std:
            self.add_argument(flag, help=helpstr,
                              default=defaultval, type=dtype)

    def add_boolean_arguments(self, arguments_bool: List[Tuple[str, str, bool]]) -> None:
        for flag, helpstr, defaultval in arguments_bool:
            self.add_argument(flag, help=helpstr,
                              action='store_false'
                              if defaultval else 'store_true',
                              default=defaultval)

    def get_args(self) -> argparse.Namespace:
        return self.get_args()
