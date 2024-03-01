# Input excel file
# Detect phone numbers
# Convert to google contact's format
from translate_numbers import *
from create_csv import *

# Convert phone numbers from the input file
def convert_phone_numbers(file_name):
    numbers = convert_phone_numbers(file_name)
    return create_csv(numbers, 'P', 50)