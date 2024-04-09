import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from check import text_to_dictionary
from write_excel import write_dictionary

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Launches a browser
    context = browser.new_context()  # Creates a new browser context
    context = browser.new_context(
  viewport={ 'width': 1400, 'height': 620 }
)
    page = context.new_page()  # Opens a new page in the browser context
    

    # Load the cookies from cookies.json
    with open("cookies.json", "r") as f:
        cookies = json.load(f)  # Directly use json.load to read from the file
        context.add_cookies(cookies)  # Adds the cookies to the context

    page.goto("https://chatgpt.com")  # Navigates to the specified page
    while True:
        x=int(input("Press 1 for Qury and 2 for writing testcases and 3 for exit::"))
        if(x==1):
            query=input('Enter the Query::')
            page.wait_for_selector('#prompt-textarea').fill(query)
            page.keyboard.press('Enter')
        elif(x==2):
            
            element_html=page.content()
            soup = BeautifulSoup(element_html, 'html.parser')

            # Find the element with the class name 'markdown'
            text_obj = soup.find(class_='markdown')
            text=text_obj.get_text(separator='\n')
            test_cases=text_to_dictionary(text)
            # print(test_cases)
            write_dictionary(test_cases)
            
        else:
            break

    

    browser.close()  # Closes the browser
