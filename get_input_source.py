# -*- coding: utf-8 -*-

"""Summary of the module.

Detailed description.
"""

__docformat__ = 'reStructuredText'

from pathlib import Path
import subprocess


def get_input_source() -> str:
    x = subprocess.run(
        [
            'defaults',
            'read',
            f'{Path.home()}/Library/Preferences/com.apple.HIToolbox.plist',
        ],
        stdout=subprocess.PIPE,
    ).stdout.decode(
        encoding='utf-8',
        errors='strict',
    ).split(
        'AppleSelectedInputSources'
    )[-1].split(
        'KeyboardLayout Name'
    )[-1].split(
        '\n'
    )[0].split(
        '='
    )[-1].split(
        ';'
    )[0].strip()

    to_print = '  '

    print(x)

    if x == 'ABC':
        to_print = f'{to_print}US'
    elif x == 'Greek':
        to_print = f'{to_print}GR'

    return to_print


def main():
    print(get_input_source(), flush=True, end='')


if __name__ == '__main__':
    main()


# EOF
