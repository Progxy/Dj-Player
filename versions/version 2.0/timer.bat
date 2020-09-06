@echo off

set /p Build_timer=<"C:\Users\Emanuele\Desktop\python\progetti\duration.txt"

set /a loop_n = Build_timer

set /a timer = 0

echo 00 : 00

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

set /a loop_n = loop_n - 1

if /i %loop_n% == 0 (goto finish)

goto Loop

:finish

exit