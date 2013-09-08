@echo off
set PYTHONPATH=%CD%
set PY31=c:\python31

%PY31%\python.exe %PY31%\scripts\py.test-script.py --basetemp=.\tests
