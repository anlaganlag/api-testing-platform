@echo off
REM Set the path to your Python executable (if not in PATH)
REM set PYTHON_PATH=C:\Path\To\Python\python.exe

REM Set the path to the enhanced_book_generator_fixed.py script
set SCRIPT_PATH=D:\test\BookWriting\src\enhanced_book_generator_fixed.py

REM Set the path to the Excel outline file
set EXCEL_PATH=D:\test\BookWriting\data\book_outline.xlsx

REM Set the API provider (optional, default is "all")
set PROVIDER=all

REM Set the number of worker threads (optional)
set THREADS=2

REM Run the script
python "%SCRIPT_PATH%" --excel "%EXCEL_PATH%" --provider "%PROVIDER%" --threads %THREADS%

REM Pause to see the output
pause