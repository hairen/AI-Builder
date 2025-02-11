import csv
import ssl

from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# Create an unverified SSL context
ssl_context = ssl._create_unverified_context()

# Define the root URL for relative links
root_url = "https://openaccess.thecvf.com"

# Load the HTML file for the main repository page
with open("CVPR 2024 Open Access Repository.html", "r",
          encoding="utf-8") as file:
  html_content = file.read()

# Parse the main page's HTML
soup = BeautifulSoup(html_content, "html.parser")

# Extract paper titles and URLs
titles = []
article_urls = []

for title_tag in soup.find_all("dt", class_="ptitle"):
  title = title_tag.text.strip()
  titles.append(title)
  # Extract the relative URL of the article
  relative_url = title_tag.find("a")["href"]
  # Combine with the root URL to form the full URL
  full_url = root_url + relative_url
  article_urls.append(full_url)


# Function to make HTTP GET requests
def fetch_url_content(url):
  try:
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)
    with urlopen(request,
                 context=ssl_context, timeout=10
                 ) as response:  # Use the unverified SSL context
      return response.read().decode("utf-8")

  except Exception as e:
    print(f"Failed to fetch URL: {url}\nError: {e}")
    return None


# # Visit each article's page and extract its abstract
# abstracts = []
# for index, url in enumerate(article_urls):
#   html_content = fetch_url_content(url)
#   if html_content is not None:
#     article_soup = BeautifulSoup(html_content, "html.parser")
#     # Extract the abstract from the <div> tag with id="abstract"
#     abstract_tag = article_soup.find("div", id="abstract")
#     abstract = abstract_tag.text.strip() if abstract_tag else "N/A"
#     abstracts.append(abstract)
#   else:
#     # If URL is inaccessible, append "N/A" for abstract
#     print(f"Abstract not accessible for title: {titles[index]}")
#     abstracts.append("N/A")

# Extract authors
authors_list = []
for dd in soup.find_all("dd"):
  authors = [
    input_tag["value"].strip()
    for input_tag in
    dd.find_all("input", attrs={"name": "query_author", "type": "hidden"})
  ]
  authors_list.append(", ".join(authors))

# Extract PDF links
pdf_links = [root_url + a["href"] for a in soup.find_all("a", href=True) if
             ".pdf" in a["href"]]

# Prepare data for CSV
csv_data = []
for i in range(len(titles)):
  row = [
    titles[i],
    authors_list[i] if i < len(authors_list) else 'N/A',
    # abstracts[i] if i < len(abstracts) else 'N/A',
    pdf_links[i] if i < len(pdf_links) else 'N/A',
  ]
  csv_data.append(row)

# Define the CSV file path
csv_file_path = "scraped_data_with_abstracts.csv"

# Write data to CSV
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
  writer = csv.writer(csv_file)

  # Write the header
  writer.writerow(["Title", "Authors", "Abstract", "PDF Link"])

  # Write the data rows
  writer.writerows(csv_data)

print(f"Data has been successfully exported to '{csv_file_path}'")
