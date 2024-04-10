import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://chatgpt.com")
    while True:
        x = str(input("Press enter to continue..."))
        if x:
            break
    with open("cookies.json", "w") as f:
        f.write(json.dumps(context.cookies()))
    browser.close()

