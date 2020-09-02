@echo off

set /p Build=<get_pos.txt

set /a timer = Build

set /a timer2 = Build

:Loop

Timeout /t 1 /nobreak >nul

set /a timer += 1

set /a timer2 += 1

set /a timer1 = timer2 / 60

if /i %timer% EQU 60 (set /a timer = timer - 60)

if /i %timer1% EQU 0 (
   if /i %timer% LSS 10 (
      echo 0%timer1% : 0%timer%
   ) ELSE (echo 0%timer1% : %timer%)
) ELSE (
   if /i %timer% LSS 10 (
      echo 0%timer1% : 0%timer%
      ) ELSE (echo 0%timer1% : %timer%)
      )
goto Loop
