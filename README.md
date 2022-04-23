# Purpose

Neomutt is an awesome terminal email client.
Unfortunately I couldn't find a solution, which allowed me to enter a single
master password, to enable mailbox synchronization for the whole session, without
saving the mailbox passwords as plain text in a configuration file, or caching
gpg credentials via the gpg agent.
I therefore modified isync to take credentials from stdin, and wrote a custom daemon
that feeds in the necessary credentials.

# Installation

This daemon has been tested with python 3.10.3 on Arch Linux.

To install dependencies, run:

```
pip install python-gnupg daemonize systemd-python
```

To set up Neomutt and offline email access with it, I recommend
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

2. You have all required, with gnupg encrypted, mailbox passwords saved
at the same location, e.g. `~/.password-store/`.

# Usage

Run:

```
./mailsync-daemon.py --quiet [options]
```

For an overview regarding the available options, run:

```
./mailsync-daemon.py -h
```

# Licensing

This daemon periodically runs mbsync to synchronize local copies of emails with their remote counterparts.
Copyright © 2022 Matteo Gätzner <m.gaetzner@gmx.de>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.

