@echo off

cd ./scripts
for %%A IN (*.py) do start /b /wait "" python "%%~fA"
