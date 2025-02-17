import os
import json
import requests
from urllib.parse import urlparse


# Load URLs from the JSON file
def load_urls(json_file):
  with open(json_file, 'r') as file:
    return json.load(file)


# Download an image from a URL
def download_image(url, save_directory):
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check if the request was successful

    # Extract the filename from the URL
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)

    # Save the image to the specified directory
    file_path = os.path.join(save_directory, filename)
    with open(file_path, 'wb') as file:
      for chunk in response.iter_content(1024):
        file.write(chunk)

    print(f"Downloaded: {filename}")
  except Exception as e:
    print(f"Failed to download {url}: {e}")


# Main function to handle the download process
def main(json_file, save_directory):
  # Ensure the save directory exists
  os.makedirs(save_directory, exist_ok=True)

  # Load URLs and download images
  urls = load_urls(json_file)
  for url in urls:
    download_image(url, save_directory)


if __name__ == "__main__":
  # Specify the path to the JSON file and the directory to save images
  json_file = "aggregated_urls.json"
  save_directory = "downloaded_images"

  main(json_file, save_directory)