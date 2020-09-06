@echo off

set /p Build=<path_get_pos.txt

rem replace with the place of the path of get_pos.txt (the position must be equal for all the get_pos.txt)

set /p Build2=<path_n_loop.txt

rem replace with the place of the path of n_loop.txt (the position must be equal for all the n_loop.txt)

set /a n_loop = Build2

set /a timer = Build

set /a timer2 = Build
:Loop

Timeout /t 1 /nobreak >nul

set /a timer += 1

set /a timer2 += 1

set /a timer1 = timer2 / 60

if /i %timer% GEQ 60 (set /a timer = timer - 60)

if /i %timer% GEQ 60 (set /a timer = timer - 60)

if /i %timer% GEQ 60 (set /a timer = timer - 60)

if /i %timer% GEQ 60 (set /a timer = timer - 60)

if /i %timer% GEQ 60 (set /a timer = timer - 60)

if /i %timer% GEQ 60 (set /a timer = timer - 60)

if /i %timer% GEQ 60 (set /a timer = timer - 60)

if /i %timer1% EQU 0 (
   if /i %timer% LSS 10 (
      echo 0%timer1% : 0%timer%
   ) ELSE (echo 0%timer1% : %timer%)
) ELSE (
   if /i %timer% LSS 10 (
      echo 0%timer1% : 0%timer%
      ) ELSE (echo 0%timer1% : %timer%)
      )

set /a n_loop = n_loop - 1

if /i %n_loop% == 0 (goto finish)

set /p Build3=<path_stop.txt

rem replace with the place of the path of stop.txt (the position must be equal for all the stop.txt)

set /a stop = Build3

if /i %stop% == 3  (goto finish)

goto Loop

:finish

exit
