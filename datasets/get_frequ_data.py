# Get the grid frequency data from the homepage http://data.netzsin.us/ for a predefined time frame and save it to a csv
# file. The data can be corrected to achieve a CSV file with one entry for each second in the time frame.
# Data correction options:
# - Skipped seconds in the measurement data can be added by using the last given frequency value
# - Multiple entries for one second can be handled by only saving the first frequency value to the CSV file

import urllib.request
from bs4 import BeautifulSoup
import csv

# Define .csv file path and open+create that file.
csv_path = 'C:\\data\\grid_frequency_may_2015.csv'
# Define the start and end date (dates will be included) in the format yyyymmdd as integer.
start_date = 20150401
end_date = 20150431

# Define the URL.
url = 'http://data.netzsin.us/'

# Decide if skipped seconds should be added with the value of the previous timestamp.
add_skipped_seconds = True
# Decide if timestamps that occur more than once should be skipped.
skip_double_entries = True
# Initiate values.
last_timestamp = []
last_freq_value = []
n_replacement = 0
max_sequential_replacement = 0

# Create new .csv file (CSV file may not exist before).
with open(csv_path, "x") as csv_file:
    writer = csv.writer(csv_file, lineterminator='\n')

    # Load the HTML data from the homepage.
    with urllib.request.urlopen(url) as url_data:
        return_data = url_data.read()
    # Make the HTML data souply beautiful (beautiful soup parses the HTML data to an organized object).
    soup = BeautifulSoup(return_data, 'html.parser')
    # Create list to save link extension to text files in (e.g. '20150101.txt').
    link = []
    # Cycle through every hyperlink entry ('a' = hyperlink tag in HTML) and save the according link ('href').
    for i_link in soup.find_all('a'):
        link.append(i_link.get('href'))

    # Cycle through every link extension of the .txt files.
    for i_link in range(len(link)):
        output_data = []
        this_link = link[i_link]
        # If the link does not end with ".txt" then it is not valid and this loop run is skipped.
        if not this_link[-4:] == '.txt':
            continue

        # If this timeseries does not lie inbetween the defined start and end date, this loop run is skipped.
        # First get the date of this file as int (format yyyymmdd).
        this_date = int(this_link[:8])
        if this_date < start_date or this_date > end_date:
            # Case: This date is out of the defined time span of interest.
            continue

        # Open the URL of the frequency table.
        data = urllib.request.urlopen(url + this_link)
        # Cycle through each line.
        for line in data:
            # Convert bytestring to string.
            this_line = line.decode("utf-8")
            # Skipe comment lines, indicated by '#' at line start.
            if this_line[0] == '#':
                continue

            # Split this line (will split timestamp and value and remove new line character).
            this_line = this_line.split()

            # Some timestamps occur more than once and almost every second second is skipped. This will be addressed in
            # the following if condition.
            if last_timestamp:
                # Case: "last_timestamp" was already defined.

                # If multiple entries for one timestamp are given, only the first one is saved.
                if skip_double_entries and (this_line[0]) == last_timestamp:
                    # Case: Duplicate of timestamp, thus don't add this entry to the output list.
                    continue

                # If wanted, skipped seconds are added.
                if add_skipped_seconds:
                    # Count how many steps are sequentially skipped to indicate missing timeperiods.
                    n_sequential_replacement = 0
                    # Case: Skipped seconds are supposed to be added "last_timestamp" is already defined.
                    while int(this_line[0]) - last_timestamp > 1:
                        # Increment the timestep.
                        last_timestamp += 1
                        # Add replacement for skipped second to the output list.
                        replacement = [last_timestamp, last_freq_value]
                        output_data.append(replacement)
                        # Increment replacement counter
                        n_replacement += 1
                        n_sequential_replacement += 1

                    # Update the max. number of sequential skipps.
                    max_sequential_replacement = max(max_sequential_replacement, n_sequential_replacement)

            # Append the output data.
            output_data.append(this_line)
            # Save last timestamp for replacement.
            last_timestamp = int(this_line[0])
            last_freq_value = float(this_line[1])

        writer.writerows(output_data)

# Print out information about the replaced skipped seconds.
print('Computation is done. {} skipped seconds have been replaced'.format(n_replacement))
print('The max. number of sequential skipps is {}.'.format(max_sequential_replacement))



