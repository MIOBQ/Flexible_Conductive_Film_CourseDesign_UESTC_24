@echo off
set CP=D:\COMSOL56\Multiphysics\plugins\*;D:\Github_codes\Flexible_Conductive_Film_CourseDesign_UESTC_24\Automation
D:\COMSOL56\Multiphysics\bin\win64\comsolcompile.exe D:\Github_codes\Flexible_Conductive_Film_CourseDesign_UESTC_24\Automation\Original2VResumeSweep.java
D:\COMSOL56\Multiphysics\java\win64\jre\bin\java.exe -cp "%CP%" Original2VResumeSweep %*
