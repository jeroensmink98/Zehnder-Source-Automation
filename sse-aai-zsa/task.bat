@echo off

:: This file is being used to run the ExtentionService under the virtual
:: pyhton environment.
:: This script is called once every server boot with the service user


:: Make sure this points to the right location of the program
cd C:\Production\Zehnder-Source-Automation\sse-aai-zsa\Zsa


conda activate ZSA && python ExtentionService_zsa.py


