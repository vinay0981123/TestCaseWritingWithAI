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
            
            # element_html=page.content()
            # soup = BeautifulSoup(element_html, 'html.parser')

            # # Find the element with the class name 'markdown'
            # text_obj = soup.find(class_='markdown')

            element_html = page.content()
            soup = BeautifulSoup(element_html, 'html.parser')

            # Find all elements with the class name 'markdown'
            markdown_elements = soup.find_all(class_='markdown')
            text_obj=''
            # Check if there are elements with the 'markdown' class
            if markdown_elements:
                # Locate the last element
                last_markdown_element = markdown_elements[-1]
                text_obj=last_markdown_element
                # Now you can work with the last 'markdown' element
                # For example, you can access its text content
                # text_content = last_markdown_element.get_text()
                # Or you can further process the last 'markdown' element as needed
            else:
                # Handle the case when no elements with the 'markdown' class are found
                print("No elements with class 'markdown' found.")
            text=text_obj.get_text(separator='\n')
            print(text)
            test_cases=text_to_dictionary(text)
            # print(test_cases)
            write_dictionary(test_cases)
            
        else:
            break

    

    browser.close()  # Closes the browser
