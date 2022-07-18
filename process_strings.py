# -*- coding: utf-8 -*-

from pathlib import Path
from os import environ
from collections import deque
from itertools import (
    cycle,
    islice,
)

from dotenv import (
    find_dotenv as dotenv_find_dotenv,
    load_dotenv as dotenv_load_dotenv,
    set_key as dotenv_set_key,
)

__author__ = 'Konstantinos Drossos'
__docformat__ = 'reStructuredText'
__all__ = ['main']


# The apple script file name
_osa_output_path = Path.home().joinpath('.curr_playing')

# The maximum length of the info string
_len_thr = 40

# Character step for moving the info string
_str_step = 3

# Space after the string while rolling
_str_space = 6

# OS env variables
_env_var_indx = 'PRV_SONG_INDX'
_env_var_artist = 'PRV_SONG_ARTIST'
_env_var_track = 'PRV_SONG_TRACK'

_special_chars = [
    'Ohat', 'Odots', 'Oforwardaccent', 'Obackaccent', 'Oce', 'Oline', 'Odash', 'Otilde',
    'ohat', 'odots', 'oforwardaccent', 'obackaccent', 'oce', 'oline', 'odash', 'otilde',
    'Aforwardaccent', 'Abackaccent', 'Ahat', 'Adots', 'Ae', 'Atilde', 'Ao', 'Adash',
    'aforwardaccent', 'abackaccent', 'ahat', 'adots', 'ae', 'atilde', 'ao', 'adash',
    'Eforwardaccent', 'Ebackaccent', 'Ehat', 'Edots', 'Edash', 'Edot', 'Eturk',
    'eforwardaccent', 'ebackaccent', 'ehat', 'edots', 'edash', 'edot', 'eturk',
    'Uhat', 'Udots', 'Uforwardaccent', 'Ubackaccent', 'Udash',
    'uhat', 'udots', 'uforwardaccent', 'ubackaccent', 'udash',
    'Ihat', 'Idots', 'Ibackaccent', 'Ibar', 'Iturk', 'Iforwardaccent',
    'ihat', 'idots', 'ibackaccent', 'ibar', 'iturk', 'iforwardaccent',
]

_substitue_chars = [
    'Ô', 'Ö', 'Ò', 'Ó', 'Œ', 'Ø', 'Ō', 'Õ',
    'ô', 'ö', 'ò', 'ó', 'œ', 'ø', 'ō', 'õ',
    'À', 'Á', 'Â', 'Ä', 'Æ', 'Ã', 'Å', 'Ā',
    'à', 'á', 'â', 'ä', 'æ', 'ã', 'å', 'ā',
    'È', 'É', 'Ê', 'Ë', 'Ē', 'Ė', 'Ę',
    'è', 'é', 'ê', 'ë', 'ē', 'ė', 'ę',
    'Û', 'Ü', 'Ù', 'Ú', 'Ū',
    'û', 'ü', 'ù', 'ú', 'ū',
    'Î', 'Ï', 'Í', 'Ī', 'Į', 'Ì',
    'i', 'ï', 'í', 'ī', 'į', 'ì'
]


def replace_special_chars(the_string: str) -> str:
    for special_char, sub_char in zip(_special_chars, _substitue_chars):
        the_string = the_string.replace(special_char, sub_char)
    return the_string


def main():
    # Initialize the string output so the linter will not complain
    to_return = 'ﱘ '.strip()

    try:
        # Get the output of the Applescript for the currently playing song
        in_arg = _osa_output_path.read_text().strip()

        # Dotenv file
        dot_env_file = dotenv_find_dotenv()

        # Check if we have some output from the script
        if in_arg == '' or in_arg.startswith('missing'):
            # If not, then nothing is playing
            to_return = f'{to_return}: Nothing is playing.'
        else:
            # Else, now is playing something

            # Split the return string from the Apple script
            arg_str = in_arg.split(' || ')

            # Check the case where there is radio playing in Music app
            if arg_str[0].startswith('radio'):
                # Then the argument at 1 index is the station
                tmp_m = f' ({arg_str[1]})'

                # The rest are the song and artist
                song_str = arg_str[-1].split(' - ')
                song_str = [song_str[-1]] + song_str[:-1]
            else:
                # No radio station here
                tmp_m = ''

                # All arguments are song and artist
                song_str = arg_str

            # Add the info for radio in the string to be returned
            to_return = f'{to_return}:{tmp_m} '

            # Check if we have some info for the song
            if len(song_str) == 1:
                 # If we don't then using the no info avail string
                song_info = 'No info available.'

                # And use empty strings for artist and track
                artist = ''
                track = ''
            else:
                # Else, use the available info
                song_info = f'{" - ".join(song_str)}'
                artist = song_str[0].strip()
                track = song_str[1].strip()

            # Construct the song info string
            len_thr = _len_thr - len(to_return)
            len_diff = len(song_info) - len_thr

            if len_diff > 0:
                song_info = f'{song_info}{" " * _str_space}'
                s_cycle = cycle(song_info)

                dotenv_load_dotenv(dot_env_file)
                str_index = int(environ.get(_env_var_indx, 0))
                prv_artist = environ.get(_env_var_artist, '')
                prv_track = environ.get(_env_var_track, '')

                if prv_artist != artist or prv_track != track:
                    # If we are not, initialize the string index to be used next
                    str_index = 0

                deque(islice(s_cycle, str_index), maxlen=0)

                song_info = ''.join([str(next(s_cycle)) for _ in range(len_thr)])

                str_index += _str_step
            else:
                song_info = f'{song_info}{" " * abs(len_diff)}'
                str_index = 0

            dotenv_set_key(dot_env_file, _env_var_indx, str(str_index))
            dotenv_set_key(dot_env_file, _env_var_artist, artist)
            dotenv_set_key(dot_env_file, _env_var_track, track)
            if any([i in song_info for i in _special_chars]):
                song_info = replace_special_chars(song_info)
            to_return = f'{to_return}{song_info}'.strip()

        # Printout the info
        print(to_return.ljust(_len_thr), end="", flush=True)

    except FileNotFoundError:
        to_return = f"{to_return}: Currently playing is not set-up"

        print(to_return, end="", flush=True)


if __name__ == '__main__':
    main()

# EOF
