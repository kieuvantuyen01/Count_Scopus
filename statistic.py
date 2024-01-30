import datetime
import config
import requests
import json
import csv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Define the API endpoint
url = "https://api.elsevier.com/content/search/scopus"

# Define the headers
headers = {
    "X-ELS-APIKey": config.API_KEY,
    "Accept": "application/json"
}

# Define the parameters
# If query by VNU institution, use AF-ID(60071364)
# If query by UET institution, use AF-ID(60071365)
# If query by VNUHN institution, use AF-ID(60071366)
# If query by VNU-UET institution, use AF-ID(60071367)
params = {
    "query": "AFFILCOUNTRY(Viet Nam) AND PUBYEAR IS 2023",
    "count": 25  # maximum number of results per request
}

# Make the first GET request
response = requests.get(url, headers=headers, params=params)

# Parse the response to JSON
data = json.loads(response.text)

# Extract the total number of results
total_results = int(data['search-results']['opensearch:totalResults'])

# Print the total number of results
print(f"The total number of articles is: {total_results}")

# Calculate the total number of pages
total_pages = total_results // params['count']
if total_results % params['count'] > 0:
    total_pages += 1

# Print the total number of pages
print(f"Total pages: {total_pages}")

# define csv file name follow the date time
csv_file_name = "articles_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".csv"
# Open a file for writing
with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Authors", "Affiliations"])

    # Loop through all pages
    for page in range(total_pages):
        # Update the 'start' parameter for pagination
        params['start'] = page * params['count']

        try:
            # Make the GET request for the current page
            session = requests.Session()
            retry = Retry(total=5, backoff_factor=0.1, status_forcelist=[ 500, 502, 503, 504 ])
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

            response = session.get(url, headers=headers, params=params)

            # Parse the response to JSON
            data = json.loads(response.text)

            # Check if 'search-results' is in the data
            if 'search-results' in data:
                # Loop through each article in the current page
                for article in data['search-results']['entry']:
                    try:
                        # Extract the desired information
                        title = article['dc:title']
                        authors = article['dc:creator']
                        affiliations = article['affiliation'] if 'affiliation' in article else 'No affiliation'

                        # Write the information to the file
                        writer.writerow([title, authors, affiliations])
                    except Exception as e:
                        print(f"Error extracting data from article: {e}")
            else:
                print(f"Page {page + 1}: No results")
        except Exception as e:
            print(f"Error making API request: {e}")