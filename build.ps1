del ./dist
cxfreeze home/timetracker/TTApp.py --base-name=Win32GUI --icon=icon_time_tracker.ico  --target-dir dist
cp tt.ini ./dist/
cp -R ./img ./dist/
