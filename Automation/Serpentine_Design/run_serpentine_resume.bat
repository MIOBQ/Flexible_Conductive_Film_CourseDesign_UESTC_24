@echo off
setlocal
set "COMSOLROOT=D:\COMSOL56\Multiphysics"
set "ROOT=D:\Github_codes\Flexible_Conductive_Film_CourseDesign_UESTC_24"
set "PATH=%COMSOLROOT%\lib\win64;%PATH%"
"%COMSOLROOT%\java\win64\jre\bin\java.exe" -cp "%COMSOLROOT%\plugins\*;%ROOT%\Automation\Serpentine_Design" SerpentineResumeSweep %*
endlocal
