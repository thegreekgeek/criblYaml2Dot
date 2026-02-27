@echo off
REM Cleanup redundant markdown files from root directory
REM Run this from the project root directory

echo Cleaning up redundant markdown files...
echo.

REM Feature #1 files
echo Removing Feature #1 files...
del /q "FEATURE_1_QUICK_REFERENCE.md" 2>nul
del /q "FEATURE_1_COMPLETE.md" 2>nul
del /q "FEATURE_1_FINAL_REPORT.md" 2>nul
del /q "FEATURE_1_DOCUMENTATION_INDEX.md" 2>nul
del /q "FEATURE_1_CHECKLIST.md" 2>nul

REM Feature #2 files
echo Removing Feature #2 files...
del /q "FEATURE_2_QUICK_REFERENCE.md" 2>nul
del /q "FEATURE_2_COMPLETE.md" 2>nul
del /q "FEATURE_2_DELIVERY_REPORT.md" 2>nul
del /q "FEATURE_2_FINAL_SUMMARY.md" 2>nul
del /q "FEATURE_2_DOCUMENTATION_INDEX.md" 2>nul
del /q "FEATURE_2_VERIFICATION.md" 2>nul

REM Planning files
echo Removing Planning files...
del /q "FEATURE_2_IMPLEMENTATION_PLAN.md" 2>nul
del /q "FEATURE_2_PLANNING_SUMMARY.md" 2>nul
del /q "FEATURE_2_VISUAL_PLAN.md" 2>nul

REM Cleanup/Organization files
echo Removing Cleanup/Organization files...
del /q "DOCUMENTATION_CLEANUP.md" 2>nul
del /q "CLEANUP_COMPLETE.md" 2>nul
del /q "DOCS_REORGANIZED.md" 2>nul
del /q "PROJECT_STRUCTURE.md" 2>nul
del /q "DELIVERY_SUMMARY.md" 2>nul
del /q "VISUAL_SUMMARY.md" 2>nul

echo.
echo Cleanup complete!
echo Root directory is now cleaner with only essential files.
echo.
pause
