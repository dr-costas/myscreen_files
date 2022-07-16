# -*- coding: utf-8 -*-

"""Module to get the battery charge and remaining."""

__all__ = ["get_battery_status_string"]
__docformat__ = 'reStructuredText'

import subprocess


def get_battery_status_string() -> str:
    """Creates and returns the string to display the
    batter status.

    :return: String containing the description of the batter
             status.
    :rtype: str
    """
    x = subprocess.run(
        ["pmset", "-g", "batt"],
        stdout=subprocess.PIPE,
    ).stdout.decode(
        encoding='utf-8',
        errors="strict",
    )

    x = x.split("\n")

    if x[0] == "Now drawing from 'AC Power'":
        return "  "
    else:
        x = x[1].split(";")

        prcnt_charge = int(x[0].split("\t")[-1].strip()[:-1])
        is_charging = " charging" in x[1]

        if is_charging:
            if prcnt_charge > 90:
                batt_symbol = " "
            elif prcnt_charge > 80:
                batt_symbol = " "
            elif prcnt_charge > 60:
                batt_symbol = " "
            elif prcnt_charge > 40:
                batt_symbol = " "
            elif prcnt_charge > 30:
                batt_symbol = " "
            else:
                batt_symbol = "v"
        else:
            if prcnt_charge > 90:
                batt_symbol = ""
            elif prcnt_charge > 80:
                batt_symbol = ""
            elif prcnt_charge > 60:
                batt_symbol = ""
            elif prcnt_charge > 40:
                batt_symbol = ""
            elif prcnt_charge > 30:
                batt_symbol = ""
            else:
                batt_symbol = ""

        rem_str = f"{x[-1].split('remaining')[0].strip()} to {'' if is_charging else ''}"

        if x[-1].split('remaining')[0].strip() == "0:00" and prcnt_charge > 90:
            rem_str = ""
            batt_symbol = " "
        elif "no estimate" in x[-1]:
            rem_str = "(no estimate)"
        elif "not charging present: true" in x[-1]:
            rem_str = "(not charging)"
        else:
            rem_str = f"({rem_str})"

        return "{b_s} {batt} {rem} ".format(
            b_s=batt_symbol,
            batt=x[0].split("\t")[-1].strip(),
            rem=rem_str,
        )


def main():
    print(get_battery_status_string(), flush=True, end="")


if __name__ == '__main__':
    main()


# EOF
