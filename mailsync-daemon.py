#!/usr/bin/env python3

"""
This daemon periodically runs mbsync to synchronize local copies of emails with their remote counterparts. 
Copyright © 2022 Matteo Gätzner <m.gaetzner@gmx.de>

it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
This program is free software; you can redistribute it and/or modify
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.
"""

import getpass
import os
from pathlib import Path
import tempfile
from time import sleep
from typing import Dict

from daemonize import Daemonize
import gnupg

import isync_wrapper
from journal_logger import logger as log
from mailsync_argument_parser import MailsyncArgumentParser

DEBUG = os.getenv("DEBUG_MAILSYNC") == "true"

parser = MailsyncArgumentParser()

cli_args = parser.get_args()

pid = tempfile.mkstemp(prefix="mailsync_daemon")[1]

# Gpg initialization
if cli_args.gpghome_path:
    home = cli_args.gpghome_path
else:
    home = str(Path.joinpath(Path.home(), ".gnupg"))
gpg = gnupg.GPG(gnupghome=home)
gpg.encoding = "utf-8"

# Log keys
if cli_args.print_keys and not cli_args.quiet:
    log.info("Public keys:")
    for pub_key in gpg.list_keys():
        for k, v in pub_key.items():
            print(f"{k}: {v}")
    log.info("Private keys:")
    for priv_key in gpg.list_keys(True):
        for k, v in priv_key.items():
            print(f"{k}: {v}")

# Get gpg password
gpg_password = cli_args.gpg_password
if not gpg_password:
    try:
        gpg_password = getpass.getpass()
    except Exception as error:
        if not cli_args.quiet:
            log.error("Error: Couldn't get the gpg master password")
            exit(1)


# Get credentials
def get_email_pass(email: str, gpg_password: str, password_store_home: str) -> str:
    with open(
        Path.joinpath(Path(password_store_home), Path(email + ".gpg")), "rb"
    ) as enc_f:
        dec_obj = gpg.decrypt_file(enc_f, passphrase=gpg_password)
        if not dec_obj.ok:
            if not cli_args.quiet:
                log.error(f"Decryption failed with status: {dec_obj.status}")
            exit(1)
        else:
            return str(dec_obj)


credentials: Dict[str, str] = {}

if cli_args.mbsyncrc_path:
    mbsyncrc_path = cli_args.mbsyncrc_path
else:
    mbsyncrc_path = Path.joinpath(Path.home(), ".mbsyncrc")

with open(mbsyncrc_path, "r") as f:
    for line in f:
        tokens = line.strip().split()
        if len(tokens) == 2 and tokens[0] == "User":
            credentials[tokens[1]] = get_email_pass(
                tokens[1], gpg_password, cli_args.password_store_path
            ).strip("\n")


# Periodically invoke custom isync with the extracted credentials
def main():
    while True:
        isync_wrapper.sync_all(cli_args.mbsync_binary_path, credentials, cli_args.quiet)
        sleep(cli_args.frequency)


if DEBUG:
    main()
else:
    daemon = Daemonize(app="mailsync-daemon", pid=pid, action=main)
    daemon.start()
