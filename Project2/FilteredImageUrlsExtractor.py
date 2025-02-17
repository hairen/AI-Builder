import json


def aggregate_urls(file_path):
  # Load the JSON data from the file
  with open(file_path, 'r') as file:
    data = json.load(file)

  # List to store the aggregated URLs
  aggregated_urls = []

  # Iterate through each element in the data
  for index, item in enumerate(data):
    # Navigate to the candidates node
    try:
      candidates = item['node']['image_versions2']['candidates']
    except KeyError:
      # Skip if the expected keys are not present
      print(f"Skipping item at index {index}: required keys are missing.")
      continue

    if candidates:  # Ensure 'candidates' is not empty
      last_candidate = candidates[-1]  # Get the last element from 'candidates'
      url = last_candidate.get('url')
      print(f"Matching URL found at index {index}: {url}")  # For debugging
      aggregated_urls.append(url)

  return aggregated_urls


# Usage
file_path = 'images.json'  # Replace with the actual path to your file
urls = aggregate_urls(file_path)

# Save the aggregated URLs into a new JSON file
output_file = 'aggregated_urls.json'  # Specify the output file name
with open(output_file, 'w') as outfile:
  json.dump(urls, outfile,
            indent=4)  # Write the list with indentation for readability

print(f"Aggregated URLs have been saved to {output_file}")

