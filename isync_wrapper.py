from subprocess import check_output
from typing import Dict


def sync_all(mbsync_binary_path: str, credentials: Dict[str, str], quiet=False) -> str:
    credstr = "\n".join([email + " " + password for email,
                         password in credentials.items()])
    command = [mbsync_binary_path, "-a", "--passwords"]

    if not quiet:
        print("Process started.")
        print("Command: ", command)

    output = check_output(command, input=credstr.encode())

    if not quiet:
        print("Process exited.")

    return str(output, encoding='utf-8')
