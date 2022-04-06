# Purpose

Neomutt is an awesome terminal email client.
Unfortunately I couldn't find a solution, which allowed me to enter a single
master password, to enable mailbox synchonization for the whole session, without
saving the mailbox passwords as plain text in a configuration file, or caching
gpg credentials via the gnupg agent.
I therefore modified isync to take credentials from stdin, and wrote a custom daemon
that feeds in the necessary credentials.

# Installation

This daemon has been tested with python 3.10.3.
Other versions haven't been tested, but it likely still
works with most python 3 versions since python-gnupg (a gpg wrapper for python)
is its only dependency apart from mbsync (isync).

To install `python-gnupg`, run:

```
pip install python-gnupg 

```

To set up neomutt and offline email access with it, I recommend
you to check out this fantastic project `https://github.com/LukeSmithxyz/mutt-wizard`.

You will need a modified version of mbsync (isync) for this daemon to work, because
the daemon relies on being able to pass credentials through stdin.
The official version (at least on arch linux) doesn't support that.

To install the compatible mbsync (isync) version, run:

```
git clone git@github.com:MatteoGaetzner/isync-with-cli-passwords.git
cd isync-with-cli-passwords
./autogen.sh 
./configure
make
sudo make install
```

Additionally make sure that:

1. You have not specified `Pass` or `PassCmd` in your `mbsyncrc` configuration file.

2. You have all required, and with gnupg encrypted, mailbox passwords saved
at the same location, e.g. `~/.password-store/`.

# Usage

for the entire session via the gnupg agent.`python3 mailsync-daemon.py [options]`

For an overview regarding the available options, run:

`python3 mailsync-daemon.py -h`
