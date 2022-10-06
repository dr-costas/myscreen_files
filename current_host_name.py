# -*- coding: utf-8 -*-

"""Simple script to get the SSID.
To be used with the `.screenrc` file, in order to display
the VPN result in the GNU Screen's status bar.
"""

__authors__: list[str] = ['Konstantinos Drosos']
__docformat__: str = 'reStructuredText'

from subprocess import run, PIPE

def main() -> None:

    icon: str = ""
    x: str = (
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

    if any(i in x for i in ["AirPort: Off", "SSID: \n"]):

        x_2: str = run(
            [
                "route",
                "get",
                "default"
            ],
            stdout=PIPE,
        ).stdout.decode(
            encoding="utf-8",
            errors="strict",
        )

        if "not in table" not in x_2:
            icon: str = " "
            active_interface: str = x_2.split("interface:")[-1].split("\n")[0].strip()
            interfaces: list[str] = run(
                [
                    "networksetup",
                    "-listallhardwareports",
                ],
                stdout=PIPE,
            ).stdout.decode(
                encoding="utf-8",
                errors="strict",
            ).split("\n\n")

            for i_i in interfaces:
                if active_interface in i_i:
                    x: str = i_i.split("\n")[0].split(":")[-1].strip()
                    break

        else:
            x: str = ""

    else:
        x: str = (x
            .split(" SSID: ")[-1]
            .split("\n")[0]
            .strip()
        )
        icon: str = " "

    if "" == x:
        x: str = "Not connected"

    print(f'{icon} {x}')


if __name__ == '__main__':
    main()


# EOF
