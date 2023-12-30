import requests
import json

# Define the API endpoint
url = "https://api.elsevier.com/content/search/scopus"

# Define the headers
headers = {
    "X-ELS-APIKey": "e7a6bb9ac93a6622119aa31d5194f01c",
    "Accept": "application/json"
}

# Define the parameters
params = {
    "query": "AFFIL(Vietnam National University, Hanoi)",
    "count": 25  # maximum number of results per request
}

# Make the first GET request
response = requests.get(url, headers=headers, params=params)

# Parse the response to JSON
data = json.loads(response.text)

# Extract the total number of results
total_results = int(data['search-results']['opensearch:totalResults'])

# Calculate the total number of pages
total_pages = total_results // params['count']
if total_results % params['count'] > 0:
    total_pages += 1

# Print the total number of pages
print(f"Total pages: {total_pages}")

# Loop through all pages
for page in range(total_pages):
    # Update the 'start' parameter for pagination
    params['start'] = page * params['count']

    # Make the GET request for the current page
    response = requests.get(url, headers=headers, params=params)

    # Parse the response to JSON
    data = json.loads(response.text)

    # Process the data as needed
    # Check if 'search-results' is in the data
    if 'search-results' in data:
        # Process the data as needed
        print(f"Page {page + 1}: {len(data['search-results']['entry'])} results")
    else:
        print(f"Page {page + 1}: No results")

print(f"The total number of articles is: {total_results}")