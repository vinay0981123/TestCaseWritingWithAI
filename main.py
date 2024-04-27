import json
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from check import text_to_dictionary
from write_excel import write_dictionary
import time


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Launches a browser
    context = browser.new_context()  # Creates a new browser context
    context = browser.new_context(viewport={ 'width': 1400, 'height': 620 })
    page = context.new_page()  # Opens a new page in the browser context
    
    x=False
    # # Load the cookies from cookies.json
    try:
        with open("cookies.json", "r") as f:
            try:
                cookies = json.load(f)  # Directly use json.load to read from the file
                context.add_cookies(cookies)  # Adds the cookies to the context
            except json.decoder.JSONDecodeError:
                print("The file 'cookies.json' contains invalid JSON data.")
    except FileNotFoundError:
        print("No cookies found")

    page.goto("https://chatgpt.com")  # Navigates to the specified page
    # Check if the element is present
    page.wait_for_selector('//textarea[@id="prompt-textarea"]')
    time.sleep(3)
    element = page.locator('//span[text()="Upgrade plan"]')
    if (element.is_visible()):
        print("Already Logged In\n")
        # with open("cookies.json", "r") as f:
        #     cookies = json.load(f)  # Directly use json.load to read from the file
        #     context.add_cookies(cookies)  # Adds the cookies to the context
    else:
        x=True
        while x:
            element = page.locator('//span[text()="Upgrade plan"]')
            if(element.is_visible()):
                x=False
        time.sleep(3)
        with open("cookies.json", "w") as f:
            f.write(json.dumps(context.cookies()))
            print("Successfully written")
    
    def processResponse():
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
        print("text is::",text)
        test_cases=text_to_dictionary(text)
        print(test_cases)
        write_dictionary(test_cases)
    page.expose_function('processResponse', processResponse)
   
    page.evaluate('''() => {
        let button = document.createElement('button');
        const xpath = '//textarea[@id="prompt-textarea"]';
        const textarea = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
        button.innerHTML = '+';
        button.id = 'saveButton';
        button.style.width = '29.9px';
        button.style.height = '29.9px';
        button.style.backgroundColor = 'black';
        button.style.color = 'white';
        button.style.border = 'none';
        button.style.cursor = 'pointer';
        button.style.fontSize = '20px';
        button.style.display = 'flex';
        button.style.justifyContent = 'center';
        button.style.alignItems = 'center';
        button.style.borderRadius = '10px';
        button.id = 'saveButton';
        button.style.color = 'rgba(180, 180, 180, 1)'; // Apply color
        button.style.transitionDuration = '.15s'; // Apply transition duration
        button.style.transitionProperty = 'color, background-color, border-color, text-decoration-color, fill, stroke'; // Apply transition properties
        button.style.transitionTimingFunction = 'cubic-bezier(.4,0,.2,1)'; // Apply transition timing function
        button.style.color = 'rgba(255, 255, 255, 1)'; // Apply color
        button.style.padding = '.125rem'; // Apply padding
        button.style.backgroundColor = 'rgba(0, 0, 0, 1)'; // Apply background color
        button.style.borderColor = 'rgba(0, 0, 0, 1)'; // Apply border color
        button.style.borderWidth = '1px'; // Apply border width
        button.style.borderRadius = '.5rem'; // Apply border radius
        button.style.position = 'absolute'; // Apply position
        button.style.cursor = 'pointer'; // Apply cursor
        button.style.webkitAppearance = 'button'; // Apply webkit appearance
        button.style.textTransform = 'none'; // Apply text transform
        button.style.fontFeatureSettings = 'inherit'; // Apply font feature settings
        button.style.fontFamily = 'inherit'; // Apply font family
        button.style.fontSize = '150%'; // Apply font size
        button.style.fontVariationSettings = 'inherit'; // Apply font variation settings
        button.style.fontWeight = 'inherit'; // Apply font weight
        button.style.letterSpacing = 'inherit'; // Apply letter spacing
        button.style.lineHeight = 'inherit'; // Apply line height
        button.style.margin = '0'; // Apply margin
        button.style.padding = '0';
        button.style.marginLeft = '90%';
        button.style.marginTop = '1.5%';
        button.style.fontweight = 'bold';
                  button.style.paddingBottom = '1.8px';
        // Insert the button as a sibling to the textarea element
        textarea.parentNode.insertBefore(button, textarea.nextSibling);
    }''')
    

    # Add an event listener to the button
    page.evaluate('''() => {
        const button = document.getElementById('saveButton');
        button.addEventListener('mousedown', () => {
            button.style.backgroundColor = 'grey';
        });
        button.addEventListener('mouseup', () => {
            button.style.backgroundColor = 'black';
            window.saveResponse = true;
        });
    }''')
    while True:
        saveResponse = page.evaluate('window.saveResponse')
        if saveResponse:
            processResponse()
            page.evaluate('window.saveResponse = false')
            time.sleep(5)
