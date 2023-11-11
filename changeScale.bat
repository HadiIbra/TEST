@ECHO OFF

REM Close ms-settings:display window if it's open
taskkill /f /fi "IMAGENAME eq SystemSettings.exe"

REM Access the variables passed from Python and convert them to integers
REM NOTE: e.g. "numOfButtonAction=%1" ist not allowed to be write like "numOfButtonAction = %1" 
SET numOfButtonAction=%1
SET moveDirection=%2

REM Convert the string arguments to integers
SET /A numOfButtonAction = %numOfButtonAction%

REM Print the variables ...
ECHO move direction 1: %moveDirection%
ECHO number of needed Button Actions 2: %numOfButtonAction%

REM open the "Anzeigeeinstellungen" in Windows settings...
explorer ms-settings:display

ping -n 2 127.0.0.1 > nul

REM This is a label that is used in the script to return to a specific point in the script.
:VBSDynamicBuild

REM This command defines an environment variable "TempVBSFile", which saves the path to a temporary VBS file.
SET TempVBSFile=%tmp%\~tmpSendKeysTemp.vbs

REM check if TempVBSFile already exists
IF EXIST "%TempVBSFile%" DEL /F /Q "%TempVBSFile%"

REM create an instance of Windows Scripting Host Shell-Objekts.
ECHO Set WshShell = WScript.CreateObject("WScript.Shell")                               >>"%TempVBSFile%"

REM sleep command ...
ECHO Wscript.Sleep 500                                                                  >>"%TempVBSFile%"

REM Simulate pressing TAB two times and the Down Button one time and then ENTER → it's just for navigating to the scale settings in windows
REM now start changing the scale
ECHO WshShell.SendKeys "{TAB}{TAB}{%moveDirection% %numOfButtonAction%}{ENTER}"         >>"%TempVBSFile%"
ECHO Wscript.Sleep 500                                                                  >>"%TempVBSFile%" 
REM ECHO WshShell.SendKeys "{TAB}{TAB}{%moveDirection% %numOfButtonAction%}{ENTER}"         >>"%TempVBSFile%"

ECHO Wscript.Sleep 800     

REM create VBS-File with CScript on order to execute the prev discussed Button Actions ...
CSCRIPT //nologo "%TempVBSFile%"

REM Close ms-settings:display window if it's still open
taskkill /f /im SystemSettings.exe


EXIT
