from subprocess import check_output
from typing import Dict

from journal_logger import logger as log


def sync_all(mbsync_binary_path: str, credentials: Dict[str, str], quiet=False) -> str:
    credstr = "\n".join(
        [email + " " + password for email, password in credentials.items()]
    )
    command = [mbsync_binary_path, "-a", "--passwords"]

    if not quiet:
        log.info(f"Process started with command: {command}")

    output = bytes("".encode("utf-8"))
    try:
        output = check_output(command, input=credstr.encode())
    except Exception as e:
        log.error(e)

    if not quiet:
        log.info("Process exited.")

    return str(output, encoding="utf-8")
