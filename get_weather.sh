#!/usr/bin/env bash

######################################################################
# @author      : kostas (kostas@woltbook.lan)
# @file        : get_weather
# @created     : Monday Apr 04, 2022 17:18:10 EEST
#
# @description : 
######################################################################


weather=`curl wttr.in/?format="%c+%t"`
weather=${weather// /}
echo $weather
