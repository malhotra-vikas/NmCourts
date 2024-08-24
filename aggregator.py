import pandas as pd
import subprocess

# Load the CSV file
data = pd.read_csv('/Users/vikas/builderspace/NmCourts/input.csv')

# Iterate over each row in the DataFrame
for index, row in data.iterrows():
    # Clean and format the date strings properly
    name = row['name'].strip('"')
    court_type = row['court_type'].strip('"')
    court_location = str(row['court_location'])  # Convert to string
    start_date = row['filing_start_date'].strip('"')
    end_date = row['filing_end_date'].strip('"')

    print("The command being run is - name - " + name)
    print("The command being run is - court_type - " + court_type)
    print("The command being run is - court_location - " + court_location)
    print("The command being run is - start_date - " + start_date)
    print("The command being run is - end_date - " + end_date)

    # Construct the Scrapy command
    command = [
        'scrapy',
        'crawl',
        'nm_courts',
        '-a', f'name={name}',
        '-a', f'courtType={court_type}',
        '-a', f'courtLocation={court_location}',
        '-a', f'caseCategory=""',
        '-a', f'startDate={start_date}',
        '-a', f'endDate={end_date}'
    ]

    print("The command being run is " + ' '.join(command))

    # Execute the command
    subprocess.run(command)

# You may want to print something here to confirm completion
print("All scrapy commands have been executed.")
