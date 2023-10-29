# Programmering i høynivåspråk

## Assignment 1 : Setting up
1. First commited file
2. Retrieve old commit
3. Resolve merge conflicts
4. Cfreating pull request


## Assignment 2: Creating array class and implement operating methods
- The methods include getitem, add, sub, mul, min, mean
- Both 1D and 2D
- To achieve operations of nD arrays, I started on a recursive method

## Assignment 3: Implementing filters, rgb image to gray and sepia
- Using three implementations python, numpy and numba
- Also made a report to time their performances

## Assignment 4: Comparing and :
These scripts use packages requests and BeautifulSoup/bs4.
Includes web scraping, regular expressions, and a small amount of pandas.

The assignment involves an implementation design to fetch and analyze Olympic statistics for the Scandinavian countries (Norway, Denmark, and Sweden) from Wikipedia. It retrieves data such as URLs, total medal counts, sport-specific medal counts, and the best-performing country in each sport. The program then generates various visualizations, including bar charts and markdown tables, and saves these outputs to specific files. 

### Tasks

**Task 1: HTTP Request and URL Filtering**

I implemented functions to handle HTTP requests and filter URLs from HTML text.

**Task 3: Parsing Wikipedia Pages for Anniversaries**

For this task, I utilized BeautifulSoup4 to parse HTML from Wikipedia pages in the "Wikipedia:Selected_anniversaries" namespace. I implemented functions to extract highlighted anniversary paragraphs, process the extracted strings into a DataFrame, and create markdown tables for each month. 

**Task 4 - implementing methods**

Implemented these methods for ...
Task 4.1 - get_scandi_stats function:
The function retrieves the URLs and gold medal statistics for Scandinavian countries from a provided Wikipedia URL, filtering the data to the specified list of countries and returning a dictionary with country names as keys and corresponding URLs and medal counts by summer and winter as values.

Task 4.2 - get_sport_stats function: 
Extracts specific sport statistics from a country's Olympic performance page, taking a URL to the country's performance page and a summer sport name as input. It returns the gold, silver, and bronze medal counts for the requested sport, or {"Gold": 0, "Silver": 0, "Bronze": 0} if the country does not compete in the specified sport.

Task 4.3 - find_best_country_in_sport function: 
Compares the results of different countries in a specific sport based on the specified medal type (Gold, Silver, or Bronze) and returns the name(s) of the best country in the given sport based on the highest number of the specified medal type.

Task 4.4 - report_scandi_stats function: 
Ties the previous functions together by retrieving and processing Scandinavian country statistics, creating and saving bar charts and markdown tables, and storing all the generated files in a designated directory.