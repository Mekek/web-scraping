
# Task:
Scrape all 638 results from:

https://franklin.oh.publicsearch.us/results?_docTypes=MO&department=RP&limit=50&offset=0&recordedDateRange=20241014%2C20241018&searchOcrText=false&searchType=quickSearch

Use Legal Description’s Pcl as in  “Lt/Un 178 PINNACLE CLUB SEC 2 PHASE 1 Pcl# 04001297200 Plt PB 10…” to match data with the Inventory in  119k Average Inventory
Create a dataset with the most correct matches possible.
Split the dataset in two, where in one the Owners in “Owner Name 1” are Legal Entities like LLC, LTD, INC, TR (Ignore others) and another where the Owners in Owner Name 1 are not these entities but a natural person.
Identify repeating owners as in “Owner Name 1” with more than one record in each.

# Solution

## Step 1
Insert you OpenAI API-KEY and path to your version of chromedriver to ```config.json```. 

About chromedriver: https://developer.chrome.com/docs/chromedriver/downloads

## Step 2
Build the Docker image: Open a terminal and navigate to your project directory where the Dockerfile is located, then run the command:
```docker build -t my-python-scripts .```

Run the project:
```docker run --rm my-python-scripts```


## After this, the following tables with data will be located in the data folder.

```average_inventory.csv``` - source table (https://docs.google.com/spreadsheets/d/1cuHluZpEFZAlommWr3LGcPaHIgJajSjC1B9SiG29yzg/edit?usp=sharing)

```collected_data.csv``` -  collected data (from https://franklin.oh.publicsearch.us/results?_docTypes=MO&department=RP&limit=50&offset=0&recordedDateRange=20241014%2C20241018&searchOcrText=false&searchType=quickSearch)

```compared_data.csv``` - matched records from 2 source tables (left only records in which the Legal Description contains a Parcel Number).

```legal_entities.csv``` - owners in “Owner Name 1” are Legal Entities like LLC, LTD, INC, TR

```repeated_names.csv``` - repeating owners as in “Owner Name 1” with more than one record.




# Steps and Approach Taken
### Web Scraping:
Used Selenium and BeautifulSoup4 to extract data from the website.
Since the site uses pagination, I collected all the results (in this case 638 results) by adjusting the offset in the URL.

Combine the scraped data with the matched entries from the Average Inventory into a single dataset.
Used a tool like Pandas in Python to create a DataFrame that will facilitate data manipulation.

### Split the Dataset:

Identifid legal entities in the "Owner Name 1" field (i.e., entries containing LLC, LTD, INC, TR).
Splited the combined dataset into two DataFrames: one for legal entities and another for natural persons (using API OpenAI).
Identify Repeating Owners:

Counted occurrences of owners in the "Owner Name 1" field to identify those with multiple records.

### Output the Results:

Saved the final datasets (both legal entities and natural persons) to CSV files for further analysis or reporting.


# Ideas for Automation and Streamlining
Scheduled Scraping:
- Use a task scheduler (like cron jobs) to run the scraping script at specific intervals (daily, weekly) to keep data updated.

Logging and Error Handling:
- Implement logging for errors or issues during scraping to easily troubleshoot problems.

Data Validation:
- Before saving results, validate the data to ensure consistency (e.g., check for duplicate Parcel Numbers).

Data Pipeline:
- Consider building a data pipeline using tools like Apache Airflow to automate the entire process, from scraping to data storage.

User Interface:
- Develop a simple web interface for users to trigger the scraping process and view results dynamically.

Visualization:
- Create dashboards using tools like Tableau or Power BI to visualize the data and trends from the scraped results.

Integrating Machine Learning:
- Use machine learning models to predict or classify data based on historical trends, potentially improving the matching process with the inventory.