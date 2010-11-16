@ECHO OFF

:Loop
IF "%1"=="clean" GOTO clean
IF "%1"=="build" GOTO build

:build
(
  echo Building Lector...
  pyuic4 ui_lector.ui > ui_lector.py
  pylupdate4 lector.pro
  lrelease lector.pro
  lrelease ts/qt_it_IT.ts
  pyrcc4 -o resources_rc.py resources.qrc
  GOTO end
  REM EXIT /B 0
)

:clean
  rm -f ui_lector.py resources_rc.py ts/qt_it_IT.qm ts/lector_*.qm *.pyc

:end
  echo Done!
REM DOC
REM http://www.robvanderwoude.com/parameters.php
REM http://ss64.com/nt/syntax-args.html
REM http://skypher.com/index.php/2010/08/17/batch-command-line-arguments/