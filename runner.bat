@echo off
REM Install dependencies from requirements.txt
pip install -r requirements.txt

REM Run scrapy crawl nm_courts
scrapy crawl nm_courts

REM Prevent the terminal from closing automatically
pause
