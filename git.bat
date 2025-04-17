@echo off

REM Add all changes to the staging area
git add .

REM Use command line argument as commit message or prompt if not provided
if "%1"=="" (
    set /p commit_message="Enter commit message: "
) else (
    set commit_message=%*
)

git commit -m "%commit_message%"

REM Push changes to the remote repository
git push

echo "Changes have been added, committed, and pushed."