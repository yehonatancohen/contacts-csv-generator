import csv, re
from os.path import join, dirname, realpath
from io import StringIO, BytesIO
import pandas as pd

def convert_phone_numbers(file_path):
    # Read the file based on its extension
    if type(file_path) == str:
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
    else:
        phone_numbers = file_path
    converted_numbers = []
    for number in phone_numbers:
        number = ''.join(digit for digit in number if digit.isalnum())
        if number.startswith('0'):
            converted_numbers.append('+972' + number[1:]) 
        elif number.startswith('+972'):
            converted_numbers.append(number)
        else:
            converted_numbers.append('+972' + number)

    return converted_numbers

def generate_names(phone_numbers, prefix, group_size=10):
    names = []
    index = 0
    for number in phone_numbers:
        name = prefix + str(index // int(group_size))
        names.append(name)
        index += 1
    return names

def generate_file(phone_numbers, names):
    csv_file = StringIO()
    writer = csv.writer(csv_file)
    with open(join(dirname(realpath(__file__)), 'Template.csv'), 'r') as template_file:
        reader = csv.reader(template_file)
        
        # Read the header row from the template file
        header_row = next(reader)
        
        # Get the indices of the columns
        name_index = header_row.index('Name')
        group_membership_index = header_row.index('Group Membership')
        phone_type_index = header_row.index('Phone 1 - Type')
        phone_value_index = header_row.index('Phone 1 - Value')

        # Write the header row to the output file
        writer.writerow(header_row)

        # Iterate over phone numbers and names simultaneously
        for number, name in zip(phone_numbers, names):
            # Construct the row with empty fields for columns other than the specified ones
            row = [""] * len(header_row)
            row[name_index] = name
            row[group_membership_index] = "*MyContacts"
            row[phone_type_index] = "Mobile"
            row[phone_value_index] = number
            writer.writerow(row)

        csv_file.seek(0)

        return csv_file

def get_phone_numbers(file_path):
    file_ext = file_path.split('.')[-1]
    if file_ext == 'csv':
        with open(file_path, 'r') as file:
            phone_numbers = [line.strip() for line in file]
    elif file_ext == 'xlsx':
        df = pd.read_excel(file_path)
        phone_numbers = df['Phone Number'].tolist()
    else:
        raise ValueError("Unsupported file extension. Only CSV and XLSX files are supported.")

def create_csv(phone_numbers, prefix, group_size=10):
    if isinstance(phone_numbers, str) and phone_numbers.endswith(('.csv', '.xlsx')):
        # Assume phone_numbers is a file path
        get_phone_numbers(phone_numbers)
    else:
        # Assume phone_numbers is a list of phone numbers
        phone_numbers = [phone.strip() for phone in phone_numbers.split(',')]
    names = generate_names(phone_numbers, prefix, group_size)
    phone_numbers = convert_phone_numbers(phone_numbers)
    return generate_file(phone_numbers, names)