# GNU Screen settings - macOS case

## Intro

This is a branch of the git repository with the settings files for GNU screen, focused on
the macOS. The difference from the main branch, is that here there are two extra files: 

1. File `currently_playing.scpt` that is used to get the currently playing info from
Music app
2. File `get_music_song`, that calls the `currently_playing.scpt` file, and processes
the output

The file `get_music_song` is called from an extra `backtick` directive in the `screenrc`
file, and the result is printed at the hardstatus line. 

## Table of contents

1. [How to use the files](#how-to-use-the-files)
2. [Explanation of `screen` file](#explanation-of-screenrc-file)

    1. [Deactivation of the start-up message](#deactivation-of-the-start-up-message)
    2. [Definition of Vim-like navigation between windows](#vim-like-navigation)
    3. [Similar, Vim-like, resizing of windows](#vim-like-resizing-of-windows)
    4. [Backtick command for currently playing music](#backtick-command-for-currently-playing-music)
    5. [Setting-up of hardstatus](#setting-up-of-hardstatus)
    6. [Small fixes for appearance](#fixes-of-appearance)
    7. [Declaration of color handling](#declaration-of-color-handling)
    8. [Activation/deactivation of hardstatus line](#activation-and-deactivation-of-hardstatus-line)


## How to use the files

Before you start, make sure that you have a back up of your current `.screenrc` file, by doing

```bash
$ mv ~/.screenrc ~/.screenrc_bak
```

----

To use the files in this branch of the repository, clone the current branch to your home directory by
doing

```bash
$ git clone --single-branch --branch macos git@github.com:dr-costas/myscreen_files.git
```

Then, change the name of the created directory, so you will not see it (as it happens by default with
the `.screenrc` file), by doing

```bash
$ mv ~/myscreen_files ~/.myscreen_files
```

Now, you have to edit the `screenrc` file in the `myscreen_files`, and replace the `<your_user_name>`
at the line

```bash
backtick 1 0 7 /Users/<your_user_name>/.myscreen_files/get_music_song
```

with your username. 

Finally, add a symbolik link of the `myscreen_files/screenrc` file where GNU Screen expects to find it,
by doing

```bash
$ ls -s ~/.myscreen_files/screenrc ~/.screenrc
```

## Explanation of screenrc file

The `screenrc` of this branch consists of the following sections: 

  1. [Deactivation of the start-up message](#deactivation-of-the-start-up-message)
  2. [Definition of Vim-like navigation between windows](#vim-like-navigation)
  3. [Similar, Vim-like, resizing of windows](#vim-like-resizing-of-windows)
  4. [Backtick command for currently playing music](#backtick-command-for-currently-playing-music)
  5. [Setting-up of hardstatus](#setting-up-of-hardstatus)
  6. [Small fixes for appearance](#fixes-of-appearance)
  7. [Declaration of color handling](#declaration-of-color-handling)
  8. [Activation/deactivation of hardstatus line](#activation-and-deactivation-of-hardstatus-line)

All the above are explained in the following sections. 

### Deactivation of the start-up message

This is performed with the line: 

```bash
startup_message off
```

The normal behavior would be to have a message like: 

>GNU Screen version 4.08.00 (GNU) 05-Feb-20
>
>Copyright (c) 2018-2020 Alexander Naumov, Amadeusz Slawinski
>Copyright (c) 2015-2017 Juergen Weigert, Alexander Naumov, Amadeusz Slawinski
>Copyright (c) 2010-2014 Juergen Weigert, Sadrul Habib Chowdhury
>Copyright (c) 2008-2009 Juergen Weigert, Michael Schroeder, Micah Cowan, Sadrul Habib Chowdhury
>Copyright (c) 1993-2007 Juergen Weigert, Michael Schroeder
>Copyright (c) 1987 Oliver Laumann
>
>This program is free software; you can redistribute it and/or modify it under the terms of the
>GNU General Public License as published by the Free Software Foundation; either version 3, or
>(at your option) any later version.
>
>This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
>even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
>General Public License for more details.
>
>You should have received a copy of the GNU General Public License along with this program (see
>the file COPYING); if not, see https://www.gnu.org/licenses/, or contact Free Software Foundation,
>Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02111-1301  USA.
>
>Send bugreports, fixes, enhancements, t-shirts, money, beer & pizza to screen-devel@gnu.org
>

If you want disable this message, then you should use the above mentioned command for screen in
the `screenrc`. 

### Vim-like navigation

With the current `screenrc` file, the navigation between the different split windows, happens with
Vim-like key mappings. That is

  * `j` is for down,
  * `k` for up,
  * `l` for right, and
  * `h` for left

To do the navigation, the command/control sequence of GNU Screen has to be pressed first, i.e.

```bash
ctrl-a j
```

to go down. 

This Vim-like navigation, is set by the commands: 

```bash
bind j focus down    # Ctl-a j goes down
bind k focus up      # Ctl-a k goes up
bind l focus right   # Ctl-a l goes right
bind h focus left    # Ctl-a h goes left
```

### Vim-like resizing of windows

When having multiple windows in the same time, in any combination of vertical and horizontal
splitting, you can resize them using (again) Vim-like key combinations. The difference with
the navigation is that at the resizing, the `j`, `k`, `l`, and `h`, have to be capital case.
That is, 

```bash
ctrl-a J
```

resizes the window and does not navigate you (notice the `J`). 

The full list of resizing combinations is

```bash
bind L resize -h +10  # Increase horizontally by 10
bind H resize -h -10  # Decrease horizontally by 10
bind K resize -v +10  # Increase vertically by 10
bind J resize -v -10  # Decrease vertically by 10
```
You change the step size (i.e. the `10`) at will. 

### Backtick command for currently playing music

In the `screenrc` file is the backtick command

```bash
backtick 1 0 7 /Users/<your_user_name>/.myscreen_files/get_music_song
```

This line declares that the script `~/.myscreen_files/get_music_song` will be executed 
every `7` seconds. The output of this script, is used at the hardstatus line, at the
position of the argument ``%1` ``.

### Setting up of hardstatus

The setting up of the hardstatus is done by the lines

```bash
hardstatus off
hardstatus alwayslastline
hardstatus string '%{= .g} %H |%=%{K}%{= w}%?%{K}%-Lw%?%{r}(%{W}%{w}%n%{w}*%f%t%?(%u)%?%{r})%{w}%?%{K}%+Lw%?%= %{g}|%{B} %1` %{g}|%{B} %m-%d  %{W}%c %{g} '
```

In a nutshell, the first line deactivates the default hardstatus, the second makes the hardstatus
to be always at last line, and the third defines the form. There are multiple capabilities to use
for the form of hardstatus, and this is beyond of the scope of this README. Please refer to the
multiple resources online, for adapting the hardstatus form to your tasting. 

### Fixes of appearance

The `screenrc` file of this repository, has some minor fixes for the appearance of GNU Screen. To
be honest, I haven't explicitly tried how these affect the appearance, but I keep using them. Feel
free to experiment and keep them or remove them. 

These fixes are at the lines

```bash
# Fix for residual editor text
altscreen on

# Fix for Name column in windowlist only show "bash"
windowlist string "%4n %h%=%f"
```

### Declaration of color handling

If you want to use the 256 color terminal emulation of GNU Screen, then you have to declare it.

**Note bold** that in order to use the 256 colors, you have to have a GNU Screen that is built with
256 colors capabilities. If you do not know how to do this, you can check
[this blog post](https://kdrossos.net/blog/14/) (is for macOS, but it stands true for Linux as
well). 

The line that declares the 256 color support is

```bash
term screen-256color
```

### Activation and deactivation of hardstatus line

Finally, at the last lines of the `screenrc` file, there is a key mapping to activate and
deactivate the appearance of the hardstatus line. These lines are

```bash
bind f eval "hardstatus ignore"
bind F eval "hardstatus alwayslastline"
```

and they indicate that when you use 

```bash
ctrl-a f
```

you make the hardstatus line to disappear, and when you use

```bash
ctrl-a F
```

you make the hardstatus line to appear (notice the capital `F`).

Enjoy!
