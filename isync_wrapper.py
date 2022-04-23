"""This modul wraps the call to mbsync"""

from subprocess import PIPE, Popen, TimeoutExpired
from typing import Dict

from config import config
from journal_logger import get_logger

log = get_logger(__name__)


def sync_all(mbsync_binary_path: str, credentials: Dict[str, str]) -> None:
    credstr = "\n".join(
        [email + " " + password for email, password in credentials.items()]
    )
    mbsync_command = [mbsync_binary_path, "-a", "--passwords"]

    if not config.quiet:
        log.debug(
            f"mbsync process started with command: '{' '.join(mbsync_command)} PASSWORDS'"
        )

    with Popen(mbsync_command, stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
        try:
            outputs, errors = proc.communicate(
                input=credstr.encode(), timeout=config.mbsync_timeout
            )
            if outputs and not config.quiet:
                log.debug(outputs)
            if errors and not config.quiet:
                log.error(errors)
        except TimeoutExpired as error:
            proc.kill()
            log.error(error)

        if not config.quiet:
            log.debug("mbsync process exited.")
