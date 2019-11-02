@echo off
echo Start calculating structural change...
R CMD BATCH --args ./scripts/structual_change.R
echo Saved breakpoints of structural change to [./models/db/]
echo Saved figures of structural change to [./results/]
pause