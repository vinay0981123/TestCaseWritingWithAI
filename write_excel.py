from openpyxl import load_workbook
import time
def number_to_alphabet(num):
    if num < 0:
        return None
    elif num <= 25:
        return chr(ord('A') + num)
    else:
        return None 
def check_matching(text1, text2):
    # Convert both texts to lowercase
    text1_lower = text1.lower()
    text2_lower = text2.lower()

    # Check if one text is a substring of the other
    return text1_lower in text2_lower or text2_lower in text1_lower


# new_data = [
#     {'Test Objective': 'To verify that users can successfully create an account by filling in the required details.', 
#      'User Story': "As a new user, I want to create an account so that I can access the application's features.", 
#      'Action Steps': '\n1. Click on the "Create an account" link from the login screen.\n2. Fill in the email, password, and confirm password fields.\n3. Click on the "Submit" button.', 
#      'Expected Result': "User account should be successfully created, and the user should be redirected to the application's dashboard/homepage.", 
#      'Prerequisite': 'The application must be installed and accessible.', 
#      'Severity': 'High.'}, 
#     {'Test Objective': 'To verify that users can toggle the visibility of the password fields.', 
#      'User Story': 'As a user, I want the option to see my password while typing it to ensure I am entering it correctly.', 
#      'Action Steps': '\n1. Click on the eye icon beside the "Password" field.\n2. Verify that the password is displayed in plain text.\n3. Click on the eye icon again to toggle back to the masked password.', 
#      'Expected Result': "Password should toggle between visible and masked states as per the user's action.", 
#      'Prerequisite': 'The application must be installed and accessible.', 
#      'Severity': 'Medium.'}
# ]
def write_dictionary(new_data):
    import os

    # Get the current working directory
    current_directory = os.getcwd()

    # List all files in the current directory
    all_files = os.listdir(current_directory)

    # Filter out files with the extension .xlsx
    xlsx_files = [file for file in all_files if file.endswith('.xlsx')]
    filename=''
    # Print the list of XLSX filenames
    for file in xlsx_files:
        filename=file
        print(filename)
    # Load the Excel workbook
    workbook = load_workbook(filename)
    sheet = workbook.active
    # # Access the desired worksheet
    # sheet = workbook.active  # Or you can specify the worksheet name, e.g., workbook['Sheet1']
    time.sleep(2)
    
    cell_cordinate=''
    # Iterate through cells in column A
    column_A = sheet['A']
    for cell in column_A:
        # Check if cell is empty
        is_empty = cell.value is None
        cell_cordinate=cell.coordinate
        if(is_empty):
            break

    cell_no=str(int(cell_cordinate[1:]))
    
    print("cell_no:::::::::", cell_no)
    for data in new_data:
        # Search for the key containing "Objective"
        # print("data::", data)
        for key in data:
            # print("key::", key)
            # Define the list of keys
            l = ['Test Objective', 'TC_ID', 'User Story', 'AC Mapping', 'Severity', 'Prerequisite', 'Action Steps', 'Expected Result']
            for i in range(len(l)):

                # print("i::", check_matching(key, l[i]))
                if check_matching(key, l[i]):
                    cell_alpha=number_to_alphabet(i)
                    cell_cordinate=cell_alpha+cell_no
                    # print("cell_cordinate::", cell_cordinate)
                    # print("new::",cell_cordinate)
                    # print("data written is::",data[key])
                    if(i==6):
                        # print("Action Steps Are::::",data[key])
                        # print("key Are::::",key)
                        actions_text=data[key]
                        sentences = actions_text.split('.')
                        # Remove empty strings from the list
                        sentences = [sentence.strip() for sentence in sentences if sentence.strip()]

                        # Number each sentence
                        numbered_sentences = [f'{m}. {sentence}' for m, sentence in enumerate(sentences, start=1)]

                        # Join the numbered sentences into a single string
                        formatted_text = '\n'.join(numbered_sentences)
                        sheet[cell_cordinate] = formatted_text
                        continue
                    sheet[cell_cordinate] = data[key]
        cell_no=str(int(cell_no)+1)
        # print("\n")
                    
                    
            
            
    # Write content to cell A24
    # sheet[cell_cordinate] = "Your content here"  # Assign the desired value to the cell
    # Save the workbook
    workbook.save(filename)
    workbook.close()

