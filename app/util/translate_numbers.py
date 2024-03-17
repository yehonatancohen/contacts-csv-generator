import re
import csv
import pandas as pd

def convert_phone_numbers(file_path):
    # Read the file based on its extension
    if file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            content = file.read()
    elif file_path.endswith('.csv'):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            content = '\n'.join(','.join(row) for row in reader)
    elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
        content = pd.read_excel(file_path, dtype=str).to_string(index=False)
    else:
        print("Unsupported file format.")
        return

    content = content.replace('\n', ' ')
    
    # Find and convert phone numbers
    phone_numbers = re.findall(r'(?:\+972|0)?(?:-)?(?:5[0-9])(?:-)?(?:\d(?:-)?){7}', content)
    converted_numbers = []
    for number in phone_numbers:
        if number.startswith('0'):
            converted_numbers.append('+972' + number[1:]) 
        elif number.startswith('+972'):
            converted_numbers.append(number)
        else:
            converted_numbers.append('+972' + number)

    return converted_numbers