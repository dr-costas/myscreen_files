# -*- coding: utf-8 -*-

"""Script to get the weather."""

__docformat__ = 'reStructuredText'

from subprocess import run, PIPE


def main():
    weather = run(
        'curl wttr.in/?format="%c+%t"',
        shell=True,
        stdout=PIPE
    ).stdout.rstrip().decode('utf-8').split()

    if len(weather) == 0:
        print('No weather info', flush=True, end='')
    else:
        print(f'{weather[0]}  {weather[1]}', flush=True, end='')


if __name__ == '__main__':
    main()

# EOF
