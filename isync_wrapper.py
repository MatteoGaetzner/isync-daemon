from subprocess import PIPE, Popen, STDOUT
from typing import Dict

from journal_logger import logger as log

# TODO: Put this in (currently not exisiting) config file
TIMEOUT = 120


def sync_all(mbsync_binary_path: str, credentials: Dict[str, str], quiet=False) -> None:
    credstr = "\n".join(
        [email + " " + password for email, password in credentials.items()]
    )
    command = [mbsync_binary_path, "-a", "--passwords"]

    if not quiet:
        log.info(f"Process started with command: {command}")

    proc = Popen(command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    try:
        outputs, errors = proc.communicate(input=credstr.encode(), timeout=TIMEOUT)
        if outputs and not quiet:
            log.info(outputs)
        if errors and not quiet:
            log.error(errors)
    except Exception as error:
        proc.kill()
        log.error(error)

    if not quiet:
        log.info("Process exited.")
