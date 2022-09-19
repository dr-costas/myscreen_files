# -*- coding: utf-8 -*-

"""Simple script to get the SSID.
To be used with the `.screenrc` file, in order to display
the VPN result in the GNU Screen's status bar.
"""

__authors__ = ['Konstantinos Drosos']
__docformat__ = 'reStructuredText'

from subprocess import run, PIPE

def main():

    x = (
        run(
            [
                "/System/Library/PrivateFrameworks/Apple80211.framework/Resources/airport",
                "-I",
            ],
            stdout=PIPE,
        )
        .stdout.decode(
            encoding="utf-8",
            errors="strict",
        )
    )

    if "AirPort: Off" in x:
        x = x.replace(": Off", " is off").strip()
    else:
        x = (x
            .split(" SSID: ")[-1]
            .split("\n")[0]
            .strip()
        )

        if "" == x:
            x = "Not connected"

    print(f' {x}')


if __name__ == '__main__':
    main()


# EOF
