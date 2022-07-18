# -*- coding: utf-8 -*-

"""Simple script to identify if the computer is under a VPN.
To be used with the `.screenrc` file, in order to display
the VPN result in the GNU Screen's status bar.
"""

__authors__ = ['Konstantinos Drosos']
__docformat__ = 'reStructuredText'

from os import uname

def main():
    h_name = uname().nodename

    if h_name.endswith('eu-west-1.compute.internal'):
        vpn_name = 'Wolt VPN'
    elif h_name.endswith('.local') or h_name.endswith('.lan'):
        vpn_name = 'local'
    else:
        vpn_name = h_name.split('.')[0]

    print(f' {vpn_name}')


if __name__ == '__main__':
    main()


# EOF
