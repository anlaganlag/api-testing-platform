echo off

REM Add all changes to the staging area
git add .

REM Commit changes with a message
set /p commit_message="Enter commit message: "
git commit -m "%commit_message%"

REM Push changes to the remote repository
git push

echo "Changes have been added, committed, and pushed."