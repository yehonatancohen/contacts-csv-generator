import csv

def generate_names(phone_numbers, prefix, group_size=10):
    names = []
    index = 0
    for number in phone_numbers:
        name = prefix + str(index // group_size)
        names.append(name)
        index += 1
    return names

def generate_file(phone_numbers, names):
    with open('Template.csv', 'r') as template_file, open('./output/output.csv', 'w', newline='') as csvfile:
        reader = csv.reader(template_file)
        writer = csv.writer(csvfile)
        
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

def create_csv(phone_numbers, prefix, group_size=10):
    names = generate_names(phone_numbers, prefix, group_size)
    generate_file(phone_numbers, names)