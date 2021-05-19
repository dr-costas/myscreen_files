#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from sys import argv
import subprocess
from pathlib import Path

__author__ = 'Konstantinos Drossos'
__docformat__ = 'reStructuredText'
__all__ = ['main']


# The file name of the file to keep the previously playing song
_song_index_path = Path.home().joinpath('.myscreen_files', 'songindex')

# The apple script file name
_osa_scrpt_file = Path.home().joinpath('.myscreen_files', 'currently_playing.scpt')

# The maximum length of the info string
_len_thr = 49

# Character step for moving the info string
_str_step = 3


def main():
    # Get the output of the Applescript for the currently playing song
    in_arg = subprocess.run(
            ['osascript', str(_osa_scrpt_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        check=True
    ).stdout.strip()

    # Initialize the string output so the linter will not complain
    to_return = ''

    # Check if we have some output from the script
    if in_arg == '' or in_arg.startswith('missing'):
        # If not, then nothing is playing
        to_return = 'Nothing is playing.'
    else:
        # Else, now is playing something, add the indication to the
        # string to be returned
        to_return = 'Now playing'

        # Split the return string from the Apple script
        arg_str = in_arg.split(' || ')

        # Check the case where there is radio playing in Music app
        if arg_str[0].startswith('radio'):
            # Then the argument at 1 index is the station
            tmp_m = f' ({arg_str[1]})'

            # The rest are the sondg and artist
            song_str = arg_str[-1].split(' - ')
        else:
            # No radio station here
            tmp_m = ''

            # All arguments are song and artist
            song_str = arg_str

        # Add the info for radio in the string to be returned
        to_return = f'{to_return}{tmp_m}: '

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
        song_info = f'{song_info}{" " * (2 * _str_step)}'

        # And calculate the length of the info string
        # without the `Now playing: ` part
        len_thr = _len_thr - len(to_return)

        # If the string is longer than the indicated length
        if len(song_info) > len_thr:

            # Check our previous situation
            try: 
                saved_text = _song_index_path.read_text().split('\n')
            except FileNotFoundError:
                # If there is no previous file, then assign initial values
                saved_text = '0\n\n'

            # Parse the previous situation
            str_index = int(saved_text[0])
            prv_artist = saved_text[1].strip()
            prv_track = saved_text[2].strip()

            # Check if we are still in the same artist and song
            if prv_artist != artist or prv_track != track:
                # If we are not, initialize the string index to be used next
                str_index = 0

            # Trim the song info string
            song_info = song_info[str_index:]

            # Check if the remaining string is longer than the limit
            if len(song_info) > len_thr:
                # If it is, trim 
                song_info = song_info[:len_thr]
                # and update the string index to be used next
                str_index += _str_step
            else:
                # Else, initialize the string index
                str_index = 0
        else:
            # Again, initialize the string index
            str_index = 0

        # Write the current situation to the file that we use
        _song_index_path.write_text(f'{str_index}\n{artist}\n{track}')

        # Assign to the variable the info for what is playing now
        to_return = f'{to_return}{song_info}'.strip()

    # Printout the info
    print(to_return.ljust(_len_thr), end='', flush=True)


if __name__ == '__main__':
    main()

# EOF
