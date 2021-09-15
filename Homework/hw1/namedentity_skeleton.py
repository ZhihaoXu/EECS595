import re

# For Programming Problem 1, we will use regular expressions to replace certain types of named entity substrings with special tokens. 
#
# Please implement the ner() function below, and feel free to use the re library. 
# DO NOT modify any function definitions or return types, as we will use these to grade your work. However, feel free to add new functions to the file to avoid redundant code.
#
# *** Don't forget to additionally submit a README_1 file as described in the assignment. ***


# Description: Transforms a string into a string with special tokens for specific types of named entities.
# Input: Any string.
# Output: The input string, with the below types of named entity substrings replaced by special tokens (<expression type>: "<token>").
# - Times: "TIME"
# - Dates: "DATE"
# - Email addresses: "EMAIL_ADDRESS"
# - Web addresses: "WEB_ADDRESS"
# - Dollar amounts: "DOLLAR_AMOUNT"
#
def ner(input_string):
    # TODO: implement the transformation of input_string

    # TIME 
    # Consider the following cases:
    # HH:MM 12-hour format with AM/PM - '^(0?[1-9]|1[0-2]):([0-5][0-9]) ?([AaPp][Mm])'
    # HH:MM 24-hour format - '^([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]'
    time_re_sets = ['(0?[1-9]|1[0-2]):([0-5][0-9]) ?([AaPp][Mm])', '([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]']
    for reg_exp in time_re_sets:
        input_string = re.sub(reg_exp, 'TIME', input_string)

    # DATE
    # Consider the following cases:
    # dd/mm/yyyy or dd-mm-yyyy or dd.mm.yyyy: '(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9][0-9][0-9])', '(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([1-9][0-9][0-9])'
    # mm/dd/yyyy or mm-dd-yyyy or mm.dd.yyyy: '(0?[1-9]|1[012])[\/\-\.](0?[1-9]|[12][0-9]|3[01])[\/\-\.]([12][0-9][0-9][0-9])', '(0?[1-9]|1[012])[\/\-\.](0?[1-9]|[12][0-9]|3[01])[\/\-\.]([1-9][0-9][0-9])'
    # yyyy/mm/dd or yyyy-mm-dd or yyyy.mm.dd: '([12][0-9][0-9][0-9])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9]|3[01]|0?[1-9])', '([1-9][0-9][0-9])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9]|3[01]|0?[1-9])'
    # September 1st, 2020 or Sept. 1st, 2020
    # yesterday, today, tomorrow
    date_re_sets = ['(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9][0-9][0-9])', 
                    '(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([1-9][0-9][0-9])',
                    '(0?[1-9]|1[012])[\/\-\.](0?[1-9]|[12][0-9]|3[01])[\/\-\.]([12][0-9][0-9][0-9])',
                    '(0?[1-9]|1[012])[\/\-\.](0?[1-9]|[12][0-9]|3[01])[\/\-\.]([1-9][0-9][0-9])',
                    '([12][0-9][0-9][0-9])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9]|3[01]|0?[1-9])',
                    '([1-9][0-9][0-9])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9]|3[01]|0?[1-9])',
                    '((January|February|March|April|May|June|July|August|September|October|November|December)|((Jan|Feb|Mar|Apr|Aug|Sept|Oct|Nov|Dec)(\.?)))( ?)(0?[1-9]|[12][0-9]|3[01])((st|nd|rd|th)?)(,?)( ?)([12][0-9][0-9][0-9])',
                    '((January|February|March|April|May|June|July|August|September|October|November|December)|((Jan|Feb|Mar|Apr|Aug|Sept|Oct|Nov|Dec)(\.?)))( ?)(0?[1-9]|[12][0-9]|3[01])((st|nd|rd|th)?)(,?)( ?)([1-9][0-9][0-9])',
                    '(yesterday|today|tomorrow)']
    for reg_exp in date_re_sets:
        input_string = re.sub(reg_exp, 'DATE', input_string)

    # EMAIL_ADDRESS
    email_re_sets = ['(\w+)@(\w+)\.(\w+)\.(\w+)\.(\w+)',  '(\w+)@(\w+)\.(\w+)\.(\w+)', '(\w+)@(\w+)\.(\w+)']
    for reg_exp in email_re_sets:
        input_string = re.sub(reg_exp, 'EMAIL_ADDRESS', input_string)
    
    # DOLLAR_AMOUNT
    input_string = re.sub('\$[0-9]+\.[0-9]+', 'DOLLAR_AMOUNT', input_string)

    # WEB_ADDRESS
    # A full domain can have maximum 63 charachters
    # optional port
    input_string = re.sub('(http(s)?:\/\/)?[a-zA-Z0-9]{0,63}(\.[a-zA-Z0-9]{0,63})+(:[0-9]{1,5})?[a-zA-Z0-9()@:%-_\\\+\.~#?&//=]*', 'WEB_ADDRESS', input_string)
    return input_string # Feel free to modify this line if necessary


# GRADING: We will be importing and repeatedly calling your ner function from a separate script with various test case strings. For example (not exact):
str1 = ner('September 1 2020 she https://www.google.com $149.99 and bought a nice microphone from www.bestdevices.com yesterday')
# if str1 == 'she spent DOLLAR_AMOUNT and bought a nice microphone from WEB_ADDRESS DATE':
#    correct = True
print(str1)