import argparse
from pathlib import Path
import sys
from typing import Any, List, Tuple


class MailsyncArgumentParser(argparse.ArgumentParser):

    """This argument parser extends the standard library argument parser"""

    def __init__(self):
        super().__init__()

        arguments_std = [
            (
                "--gpghome-path",
                'custom path to the gpg home directory (default: "~/.gnupg")',
                str(Path.joinpath(Path.home(), ".gnupg")),
                str,
            ),
            (
                "--password-store-path",
                'custom path to the password store directory (default: "~/.password-store")',
                str(Path.joinpath(Path.home(), ".password-store")),
                str,
            ),
            (
                "--mbsyncrc-path",
                'custom path to the mbsyncrc file (default: "~/.mbsyncrc")',
                str(Path.joinpath(Path.home(), ".mbsyncrc")),
                str,
            ),
            (
                "--mbsync-binary-path",
                'custom path to the mbsyncrc binary (default: "/usr/local/bin/mbsync")',
                "/usr/local/bin/mbsync",
                str,
            ),
            ("--gpg-password", "gpg master password", None, str),
            (
                "--frequency",
                "frequency with which to sync mailboxes; specify it in seconds (default: 120s)",
                120,
                int,
            ),
        ]

        arguments_bool = [
            (
                "--print-keys",
                "print secret and public keys (useful for debugging home directory)",
                False,
            ),
            ("--quiet", "silence all outputs", False),
        ]

        self.add_standard_arguments(arguments_std)
        self.add_boolean_arguments(arguments_bool)

    def add_standard_arguments(
        self, arguments_std: List[Tuple[str, str, Any, type]]
    ) -> None:
        for flag, helpstr, defaultval, dtype in arguments_std:
            self.add_argument(flag, help=helpstr, default=defaultval, type=dtype)

    def add_boolean_arguments(
        self, arguments_bool: List[Tuple[str, str, bool]]
    ) -> None:
        for flag, helpstr, defaultval in arguments_bool:
            self.add_argument(
                flag,
                help=helpstr,
                action="store_false" if defaultval else "store_true",
                default=defaultval,
            )

    def get_args(self) -> argparse.Namespace:
        return self.parse_args(sys.argv[1:])
