from pathlib import Path
import sys
import argparse
import gnupg
import getpass
from mailsync_argument_parser import MailsyncArgumentParser
filepath = './testmail@gmail.com.gpg'

parser =


cli_args = parser.parse_args(sys.argv[1:])

# gpg initialization
home = str(Path.joinpath(Path.home(), '.gnupg'))
gpg = gnupg.GPG(gnupghome=home)
gpg.encoding = 'utf-8'

# Print keys
if cli_args.print_keys:
    print("Public keys:")
    for pub_key in gpg.list_keys():
        for k, v in pub_key.items():
            print(f"{k}: {v}")
    print("Private keys:")
    for priv_key in gpg.list_keys(True):
        for k, v in priv_key.items():
            print(f"{k}: {v}")

password = None

try:
    password = getpass.getpass()
except Exception as error:
    print('ERROR', error)
else:
    print('Password entered:', password)


with open(filepath, 'rb') as enc_f:
    dec_obj = gpg.decrypt_file(enc_f, passphrase=password)
    if not dec_obj.ok:
        print(f"Decryption failed with status: {dec_obj.status}")
    else:
        print(f"Decryption succeeded.\nData: {dec_obj.data}")
