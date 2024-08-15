from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys

def get_codeforces_input(problem_url):
    # Set up Chrome options to run headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run headless
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
    chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    chrome_options.add_argument("--window-size=1920x1080")  # Set a large enough window size
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  # Set a user agent
    
    # Initialize the Chrome WebDriver with options
    driver = webdriver.Chrome(options=chrome_options)

    # Open the problem URL
    driver.get(problem_url)

    # Get the page source after rendering
    page_source = driver.page_source

    # Parse with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all input sections
    input_divs = soup.find_all('div', class_='input')
    if not input_divs:
        print("Could not find input sections on the page.")
        return None

    all_inputs = []
    for i, input_div in enumerate(input_divs, 1):
        input_pre = input_div.find('pre')
        if input_pre:
            # Replace <br> tags with newline characters
            for br in input_pre.find_all("br"):
                br.replace_with("\n")
            # Get the text and ensure it has proper line breaks
            formatted_input = input_pre.get_text()
            all_inputs.append(f"input{i}\n{formatted_input}\n")

    # Close the driver
    driver.quit()

    return "\n".join(all_inputs)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the Codeforces problem URL as an argument.")
        sys.exit(1)

    problem_url = sys.argv[1]
    input_data = get_codeforces_input(problem_url)

    if input_data:
        with open('input.txt', 'w') as f:
            f.write(input_data)
        print("Input data has been saved to input.txt")
    else:
        print("Failed to retrieve input data.")

