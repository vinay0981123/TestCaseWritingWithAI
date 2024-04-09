import re
import json

def text_to_dictionary(text):
    text = text.replace('\n',' ')
    text = text.replace('  ', ' ')
    test_cases = re.split(r'Test Case \d+:', text)
    test_cases_list=[]
    dict_list_testcases=[]
    # The first element might be empty due to the split, so we remove it if it's empty
    test_cases = [case.strip() for case in test_cases if case]

    # Adding back the "Test Case X:" part that was removed by split, except for the first element which didn't have it before split
    test_cases = [f'Test Case {i+1}: {case}' for i, case in enumerate(test_cases)]

    #Grouping different testcases in list
    for case in test_cases:
        test_cases_list.append(case)
        # print(case)
        # print('---') 
    # print(test_cases_list)
    #Converting list test cases in proper json format
    for i in test_cases_list:

        # Define a pattern to match the sections and their content
        pattern = r'(Test Objective|Objective|User Story|Action Steps|Steps|Prerequisite|Severity|Expected Result|Result): (.*?)\s*(?=(Test Objective|Objective|User Story|Action Steps|Steps|Prerequisite|Severity|Expected Result|Result|$))'

        # Find all matches in the text
        matches = re.findall(pattern, i, re.DOTALL)

        # Convert matches to a dictionary
        result = {match[0]: match[1].strip() for match in matches}
        dict_list_testcases.append(result)
    return dict_list_testcases


    