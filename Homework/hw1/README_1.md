# Homework 1 Programming 1
Author: Zhihao Xu  

In the Programming Problem 1, we are asked to use regular expressions to replace certain types of named entity substrings with special tokens. 

**Problem Description**: Transforms a string into a string with special tokens for specific types of named entities.  
**Input**: Any string.  
**Output**: The input string, with the below types of named entity substrings replaced by special tokens (\<expression type\>: "\<token\>").
- Times: "TIME"
- Dates: "DATE"
- Email addresses: "EMAIL_ADDRESS"
- Web addresses: "WEB_ADDRESS"
- Dollar amounts: "DOLLAR_AMOUNT"

For each types, I consider multiple possible cases, which are listed below:

- Times: "TIME"  
  - HH:MM 12-hour format with AM/PM   
    `(0?[1-9]|1[0-2]):([0-5][0-9]) ?([AaPp][Mm])`  
  - HH:MM 24-hour format  
    `([0-9]|0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]`

- Dates: "DATE"
  - dd/mm/yyyy or dd-mm-yyyy or dd.mm.yyyy  
    `(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9][0-9][0-9])`  
    `(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([1-9][0-9][0-9])`
  -  mm/dd/yyyy or mm-dd-yyyy or mm.dd.yyyy  
    `(0?[1-9]|1[012])[\/\-\.](0?[1-9]|[12][0-9]|3[01])[\/\-\.]([12][0-9][0-9][0-9])`  
    `(0?[1-9]|1[012])[\/\-\.](0?[1-9]|[12][0-9]|3[01])[\/\-\.]([1-9][0-9][0-9])`
  - yyyy/mm/dd or yyyy-mm-dd or yyyy.mm.dd  
    `([12][0-9][0-9][0-9])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9]|3[01]|0?[1-9])`  
    `([1-9][0-9][0-9])[\/\-\.](0?[1-9]|1[012])[\/\-\.]([12][0-9]|3[01]|0?[1-9])`
  - e.g. September 1st, 2020 or Sept. 1st, 2020, both "," and "." here are optional.  
    `((January|February|March|April|May|June|July|August|September|October|November|December)|((Jan|Feb|Mar|Apr|Aug|Sept|Oct|Nov|Dec)(\.?)))( ?)(0?[1-9]|[12][0-9]|3[01])((st|nd|rd|th)?)(,?)( ?)([12][0-9][0-9][0-9]`  
    `((January|February|March|April|May|June|July|August|September|October|November|December)|((Jan|Feb|Mar|Apr|Aug|Sept|Oct|Nov|Dec)(\.?)))( ?)(0?[1-9]|[12][0-9]|3[01])((st|nd|rd|th)?)(,?)( ?)([1-9][0-9][0-9])`
  - yesterday, today, tomorrow  
    `(yesterday|today|tomorrow)`


- Email addresses: "EMAIL_ADDRESS"
  - xxx@xxx.xxx.xxx.xxx   
  `(\w+)@(\w+)\.(\w+)\.(\w+)\.(\w+)`  
  - xxx@xxx.xxx.xxx    
  `(\w+)@(\w+)\.(\w+)\.(\w+)`
  - xxx@xxx.xxx   
  `(\w+)@(\w+)\.(\w+)`

- Web addresses: "WEB_ADDRESS"  
In the web address, the domain can only have maximum 63 characters and the rest url can be very long. And there is a optional port with length 1 to 5. Here I also consider "http(s)://" as optional part in the front.  
`(http(s)?:\/\/)[a-zA-Z0-9]{0,63}(\.[a-zA-Z0-9]{0,63})+(:[0-9]{1,5})?[a-zA-Z0-9()@:%-_\\\+\.~#?&//=]*`

- Dollar amounts: "DOLLAR_AMOUNT"  
`\$[0-9]+\.[0-9]+`