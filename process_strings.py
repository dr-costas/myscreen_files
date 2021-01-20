#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv
import subprocess
from pathlib import Path

__author__ = ''
__docformat__ = ''
__all__ = []


_song_index_path = Path.home().joinpath('.myscreen_files', 'songindex')
_osa_scrpt_file = Path.home().joinpath('.myscreen_files', 'currently_playing.scpt')
_len_thr = 49
_str_step = 3



def main():
    in_arg = subprocess.run(
            ['osascript', str(_osa_scrpt_file)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        check=True
    ).stdout

    to_return = ''

    if in_arg == '':
        to_return = 'Nothing is playing'
    else:
        to_return = 'Now playing'
        arg_str = in_arg.split(' || ')
        if arg_str[0].startswith('radio'):
            tmp_m = f' ({arg_str[1]})'
            song_str = arg_str[-1].split(' - ')
        else:
            tmp_m = ''
            song_str = arg_str

        to_return = f'{to_return}{tmp_m}: '

        if len(song_str) == 1:
            song_info = 'No stream info available.'
            artist = ''
            track = ''
        else:
            song_info = f'{" - ".join(song_str)}'
            artist = song_str[0].strip()
            track = song_str[1].strip()

        song_info = f'{song_info}{" " * (2 * _str_step)}'
        len_thr = _len_thr - len(to_return)

        if len(song_info) > len_thr:
            saved_text = _song_index_path.read_text().split('\n')

            str_index = int(saved_text[0])
            prv_artist = saved_text[1].strip()
            prv_track = saved_text[2].strip()

            song_info = song_info[str_index:]

            if prv_artist != artist or prv_track != track:
                str_index = 0

            if len(song_info) > len_thr:
                song_info = song_info[:len_thr]
                str_index += _str_step
            else:
                str_index = 0
        else:
            str_index = 0

        _song_index_path.write_text(f'{str_index}\n{artist}\n{track}')
        to_return = f'{to_return}{song_info}'.strip().ljust(_len_thr)

        print(to_return, end='', flush=True)


if __name__ == '__main__':
    main()

# EOF
