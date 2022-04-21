from subprocess import PIPE, Popen, STDOUT
from typing import Dict

from config import config
from journal_logger import logger as log


def sync_all(mbsync_binary_path: str, credentials: Dict[str, str]) -> None:
    credstr = "\n".join(
        [email + " " + password for email, password in credentials.items()]
    )
    mbsync_command = [mbsync_binary_path, "-a", "--passwords"]

    if not config.quiet:
        log.debug(
            f"Process started with command: '{' '.join(mbsync_command)} PASSWORDS'"
        )

    proc = Popen(mbsync_command, stdout=PIPE, stdin=PIPE, stderr=PIPE)
    try:
        outputs, errors = proc.communicate(
            input=credstr.encode(), timeout=config.mbsync_timeout
        )
        if outputs and not config.quiet:
            log.debug(outputs)
        if errors and not config.quiet:
            log.error(errors)
    except Exception as error:
        proc.kill()
        log.error(error)

    if not config.quiet:
        log.debug("Process exited.")
