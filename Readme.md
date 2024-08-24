# Run in terminal to fetch one date/ line

scrapy crawl nm_courts -a name="A" -a courtType="D" -a courtLocation="1" -a caseCategory="" -a startDate="1/1/2024" -a endDate="31/1/2024"

# Aggregator Run
1. Make sure you have the exhaustive inputs copied to input.csv
2. Clean output.csv
3. Run  python3 aggregator.py