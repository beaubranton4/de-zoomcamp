from bs4 import BeautifulSoup
import requests
import time
from datetime import datetime
import pandas as pd
import re
from requests import Session
from datetime import datetime, timedelta
from google.cloud import storage
from os import path
from mage_ai.settings.repo import get_repo_path

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# GET request options
_HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Define variables for ingestion script
sport_code = "MBA"
academic_year = "2024"
division = "1"

#CONVERT TO A FUNCTION THAT READS WHICH DATES ARE NOT PRESENT IN GCS
#FROM START OF SEASON 2/16/2024 TO TODAY'S DATE - 1. Ok to rescrape as safeguard
#FUNCTION WILL RETURN LIST OF ALL DATES THAT HAVE NOT BEEN POPULATED YET
#TURN THIS INTO A GLOBAL VARIABLE
# start_date_str = "02/16/2024"
# end_date_str = "03/26/2024"

# start_date = datetime.strptime(start_date_str, "%m/%d/%Y")
# end_date = datetime.strptime(end_date_str, "%m/%d/%Y")
# date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

config_path = path.join(get_repo_path(), 'io_config.yaml')
config_profile = 'default'
bucket_name = 'mage_zoomcamp_beau_branton_bucket'
prefix = 'd1_baseball_project/batting_box_scores_test/date='

#Open webpage and locate home and away tables to scrape boxstats
def get_stats(url):
    with Session() as s:
        r = s.get('https://stats.ncaa.org'+url, headers=_HEADERS)
    if r.status_code == 403:
        print('An error occurred with the GET Request')
        print('403 Error: NCAA blocked request')
    soup = BeautifulSoup(r.text, features='lxml')
    tables = soup.find_all("table")

    away_table = tables[5]
    home_table = tables[6]

    away_df = scrape_box_stats(away_table)
    home_df = scrape_box_stats(home_table)

    return away_df, home_df

def scrape_box_stats(table):
    headers = [header.text for header in table.find('tr', {'class': 'grey_heading'}).find_all('th')]        
    data = []
    for row in table.find_all('tr', {'class': 'smtext'}):
        data.append([cell.text.strip().split('/')[0] for cell in row.find_all('td')])  # Split at '/' for dirty data and take the first part
    df = pd.DataFrame(data, columns=headers)
    df = df.replace('', 0)
    return df

def get_team_names(table_html):
    # Parse the HTML content
    soup = BeautifulSoup(table_html, 'html.parser')

    # Find the table rows
    rows = soup.find_all('tr')

    # Get the team names and remove the record in parentheses
    away_team_name = rows[1].find('a').text.rsplit(' (', 1)[0].strip()
    home_team_name = rows[2].find('a').text.rsplit(' (', 1)[0].strip()

    return {"Away Team": away_team_name, "Home Team": home_team_name}

def get_game_info(table_html):
    # Parse the HTML content
    soup = BeautifulSoup(table_html, 'html.parser')

    # Find the table rows
    rows = soup.find_all('tr')
    # Get the game date, location, and attendance (if the data is available)
    if len(rows)>=3:     
        game_date = rows[0].find_all('td')[1].text.strip()
        location = rows[1].find_all('td')[1].text.strip()
        attendance = rows[2].find_all('td')[1].text.strip()
    elif len(rows) == 2:
        # Case: len(rows) = 2
        game_date = rows[0].find_all('td')[1].text.strip()
        location = rows[1].find_all('td')[1].text.strip()
        attendance = None
    elif len(rows) == 1:
        # Case: len(rows) = 1
        game_date = rows[0].find_all('td')[1].text.strip()
        location = None
        attendance = None
    else:
        # Case: len(rows) = 0
        game_date, location, attendance = None, None, None

    return {"Game Date": game_date, "Location": location, "Attendance": attendance}

def get_box_score_links(html):
    # Parse the HTML content
    soup = BeautifulSoup(html, 'html.parser')
    # Find all the 'a' tags
    a_tags = soup.find_all('a')
    # Get the links that contain "box_score"
    links = [a['href'] for a in a_tags if "box_score" in a['href']]
    return links

def extract_dates(object_keys):
    dates = []
    for key in object_keys:
        key = urllib.parse.unquote(key)
        parts = key.split('/')
        for part in parts:
            if part.startswith('date='):
                date = part[len('date='):].split('%')[0]
                dates.append(date)
    return dates

def get_gcs_game_dates_missing(bucket_name, prefix):
    
    #Obtain dates for data that exists in Google Cloud Storage
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=prefix)
    object_keys = [blob.name for blob in blobs if blob.name.endswith('.parquet')]
    date_strings = extract_dates(object_keys)
    dates = [date_string for date_string in date_strings]
    
    #Get list of all dates since start of seasone until today
    start_date_str = '02/16/2024' #Replace with automatic variable for first day of season
    end_date = datetime.now().date()
    start_date = datetime.strptime(start_date_str, "%m/%d/%Y").date()
    all_dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
    
    #Return the difference between those lists
    missing_dates = [date for date in all_dates if date not in dates]
    return missing_dates

@data_loader
def load_data(*args, **kwargs):
    # return none
    # # Start the timer
    # start_time = time.time()
    date_range = get_gcs_game_dates_missing(bucket_name,prefix)
    print(date_range)
    return None
    # # Create empty dataframes for final stats
    # final_batting_df = pd.DataFrame()
    # for game_date in date_range:
        
    #     # Construct the base URL
    #     base_url = "https://stats.ncaa.org/contests/livestream_scoreboards"       
    #     # Create a dictionary of parameters
    #     params = {
    #         "utf8": "✓",
    #         "sport_code": sport_code,
    #         "academic_year": academic_year,
    #         "division": division,
    #         "game_date": game_date,
    #     }
        
    #     with Session() as s:
    #         r = s.get(base_url, params=params, headers=_HEADERS)
    #     if r.status_code == 403:
    #         print('An error occurred with the GET Request')
    #         print('403 Error: NCAA blocked request')
        
    #     #Retrieve all links to game box score webpages
    #     game_links = get_box_score_links(r.text)
    #     num_games = 0    
    #     for game in game_links:
    #         num_games+=1
    #         url = 'https://stats.ncaa.org'+game
    #         # print(f"Getting stats from: {url}")
            
    #         #------------------------GET URLS FOR BATTING,PITCHING,FIELDING
    #         with Session() as s:
    #             r = s.get(url, headers=_HEADERS)
    #         if r.status_code == 403:
    #             print('An error occurred with the GET Request')
    #             print('403 Error: NCAA blocked request')
    #         soup = BeautifulSoup(r.text, features='lxml')
            
    #         # Find the table element that contains the player data
    #         tables = soup.find_all("table")
            
    #         team_names = get_team_names(tables[0].prettify())
    #         game_info = get_game_info(tables[2].prettify())
    #         stat_type = tables[4].find_all('a')
            
            
    #         #Store URLs for batting
    #         url = stat_type[0]['href']

    #         # Get the home and away stats for each stat type
            
    #         away_df, home_df = get_stats(url)  
    #         ##MAKE INTO FUNCTION
    #         away_df['game_id'] =  int(re.search(r'\d+', game).group())
    #         home_df['game_id'] = int(re.search(r'\d+', game).group())
    #         away_df['team'] = team_names["Away Team"]
    #         home_df['team'] = team_names["Home Team"]
    #         away_df['date'] = game_date
    #         home_df['date'] = game_date
    #         away_df['location'] = game_info["Location"]
    #         home_df['location'] = game_info["Location"]
    #         away_df['attendance'] = game_info["Attendance"]
    #         home_df['attendance'] = game_info["Attendance"]
            
    #         # Append away and home stats to the final dataframe
    #         final_batting_df = pd.concat([final_batting_df, away_df, home_df])

    #     print(f"Finished scraping data from {num_games} games on {game_date}")
    # # End the timer and print the elapsed time
    # end_time = time.time()
    # print(f"Time taken: {end_time - start_time} seconds")
    # return final_batting_df

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
