Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "run.bat" & Chr(34) & " > log.txt 2>&1", 0, True
Set WshShell = Nothing

