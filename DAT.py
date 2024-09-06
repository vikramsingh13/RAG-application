import requests
from bs4 import BeautifulSoup

# Function to decode the secret message from the Google Doc.
# decode_secret_message function takes the google_doc_url as input
# and prints the decoded secret message of unicode characters.
def decode_secret_message(google_doc_url: str):

    # We will use the requests library to fetch the HTML content of the Google Doc.
    response = requests.get(google_doc_url)
    # We will work with the HTML content of the Google Doc from the response text.
    doc_html = response.text

    # BeautifulSoup will help us parse the HTML content.
    soup = BeautifulSoup(doc_html, 'html.parser')

    # In the HTML content, we will find the first table tag. 
    # This table tag contains the main table content of the google doc.
    table_content = soup.find('table')

    # The data variable will be used to store the x-coordinate, character, and y-coordinate of each cell in the table.
    data = []

    # First tr contains header. So, it is being skipped.
    for table_row in table_content.find_all('tr')[1:]:
        row = [table_cell.text.strip() for table_cell in table_row.find_all('td')]
        if len(row) == 3:
            # Append the x-coordinate, character, and y-coordinate to the data list as a dictionary.
            # We will convert the x-coordinate and y-coordinate to integers.
            data.append({
                'x-coordinate': int(row[0]),
                'Character': row[1],
                'y-coordinate': int(row[2])
            })

    # Find the max x and y coordinates to determine the grid size as it can 
    # be arbitrarily large based on the data provided.
    max_x = max(entry['x-coordinate'] for entry in data)
    max_y = max(entry['y-coordinate'] for entry in data)

    # Print the grid
    # We will create a grid initialized with spaces based on max_x and max_y.
    # Any missing characters will be represented by spaces as asked in the question.
    # Create a grid initialized with spaces based on max_x and max_y.
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Place characters in their respective coordinates, flipping the y-coordinate for bottom-left origin
    # so that the grid is printed correctly with the (0,0) coordinate at the bottom-left.
    for entry in data:
        grid[max_y - entry['y-coordinate']][entry['x-coordinate']] = entry['Character']

    # Print the grid by joining the characters in each row.
    for row in grid:
        print(''.join(row))

# URL of the Google Doc containing the secret message.
google_doc_url = 'https://docs.google.com/document/d/e/2PACX-1vSHesOf9hv2sPOntssYrEdubmMQm8lwjfwv6NPjjmIRYs_FOYXtqrYgjh85jBUebK9swPXh_a5TJ5Kl/pub'

# Call the decode_secret_message function with the google_doc_url as input.
decode_secret_message(google_doc_url)
