import re
from typing import Tuple
from requesting_urls import get_html


## -- Task 3 (IN3110 optional, IN4110 required) -- ##

# create array with all names of months
month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_date_patterns():
    """Return strings containing regex pattern for year, month, day
    arguments:
        None
    return:
        year, month, day (tuple): Containing regular expression patterns for each field
    """

    # Regex to capture days, months and years with numbers
    # year should accept a 4-digit number between at least 1000-2029
    year = r"(?P<year>1[0-9]{3}|20[0-2][0-9])"

    # month should accept month names or month numbers
    jan = r"\b[dJ]an(?:uary)?\b"
    feb = r"\b[dF]eb(?:ruary)?\b"
    mar = r"\b[dM]ar(?:ch)?\b"
    apr = r"\b[dA]pr(?:il)?\b"
    may = r"\b[dM]ay\b"
    jun = r"\b[dJ]un(?:e)?\b"
    jul = r"\b[dJ]ul(?:y)?\b"
    aug = r"\b[dA]ug(?:ust)?\b" 
    sep = r"\b[dS]ep(?:tember)?\b"    
    oct = r"\b[dO]ct(?:ober)?\b"
    nov = r"\b[dN]ov(?:ember)?\b"
    dec = r"\b[dD]ec(?:ember)?\b"
    month = rf"(?P<month>[0-1]?\d|{jan}|{feb}|{mar}|{apr}|{may}|{jun}|{jul}|{aug}|{sep}|{oct}|{nov}|{dec})"
    
    # day should be a number, which may or may not be zero-padded
    day = r"(?P<day>\d\d?)"

    return year, month, day


def convert_month(s: str):
    """Converts a string month to number (e.g. 'September' -> '09'.

    You don't need to use this function,
    but you may find it useful.

    arguments:
        month_name (str) : month name
    returns:
        month_number (str) : month number as zero-padded string
    """
    # If already digit do nothing
    if s.isdigit():
        return zero_pad(s)

    # Convert to number as string
    for month in month_names:
        if s.lower().startswith(month[0:3].lower()):
            return zero_pad(str(month_names.index(month) + 1))
   

def zero_pad(n: str):
    """zero-pad a number string

    turns '2' into '02'

    You don't need to use this function,
    but you may find it useful.
    """
    if len(n) == 1:
       return "0" + n
    return n


def find_dates(text: str, output: str = None):
    """Finds all dates in a text using reg ex

    arguments:
        text (string): A string containing html text from a website
    return:
        results (list): A list with all the dates found
    """
    year, month, day = get_date_patterns()

    # Date on format DD MM YYYY
    DMY = rf"({day} {month} {year})"

    # Date on format MM DD, YYYY
    MDY = rf"({month} {day}\, {year})"

    # Date on format YYYY MM DD
    YMD = rf"({year} {month} {day})"

    # Date on format YYYY-MM-DD - ISO
    ISO = rf"({year}-{month}-{day})"

    # list with all supported formats
    formats = [ISO, DMY, MDY, YMD]
    dates = []

    # find all dates in any format in text
    
    #dates = re.findall(rf"{ISO}|{DMY}|{MDY}|{YMD}", text)
    #datePattern = re.compile(rf"{ISO}|{DMY}|{MDY}|{YMD}")
    for format in formats:
        datePat = re.compile(format)
        for date in datePat.findall(text):
            match = datePat.search(date[0])
            if match:
                y, m, d = match.group("year"), match.group("month"), match.group("day")
                m, d = convert_month(m), zero_pad(d)
                date = y + "/" + m + "/" + d
                dates.append(date)

    # Write to file if wanted
    if output:
        rfile = open(output, "w")
        for date in dates:
            rfile.write(date + "\n")
        rfile.close()

    return dates

url = "https://en.wikipedia.org/wiki/Serena_Williams"
html = get_html(url)
dates = find_dates(html, "SerenaDates.txt")