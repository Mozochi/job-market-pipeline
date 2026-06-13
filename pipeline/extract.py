import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from typing import Any
import os
from dotenv import load_dotenv
from pathlib import Path
import json
from datetime import datetime

dotenv_path = Path(__file__).parent.parent / "configs" / ".env"
load_dotenv(dotenv_path)

API_KEY = os.getenv("ADZUNA_API_KEY")
APPLICATION_KEY = os.getenv("ADZUNA_APPLICATION_ID")
RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"
MANIFEST_FILE = Path(__file__).parent.parent / "data" / "manifest.json"
SEARCH_TYPES = {0: "results", 1: "categories"}


class AdzunaClient:
    def __init__(self):
        self.base_url = "https://api.adzuna.com/v1/api"
        self.headers = {"Accept" : "application/json"}
        self.api_key = API_KEY
        self.app_id = APPLICATION_KEY
        
    def get_page(self, page: int, location: str):
        """Get a selected jobs page for a specified location 

        Args:
            page (int): The page number
            location (str): Location to search jobs for

        Returns:
            json: {count, mean, results[id, title, description, created, redirect_url, adref, latitude, longitude, location]} 
        """
        try:
            r = requests.get(f"{self.base_url}/jobs/{location}/search/{page}?app_id={self.app_id}&app_key={self.api_key}", headers=self.headers)
            r.raise_for_status()
            save_raw_data(json_data=r.json()["results"], 
                          type=SEARCH_TYPES.get(0),
                          location=location, 
                          page=page,
                          category="N/A")
            
        except HTTPError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except ConnectionError:
            print("Failed to connect - check your internet or the API url")
        except Timeout:
            print("Request timed out")
        except Exception as e:
            print(f"An error has occured: {e}")
    
    
    def get_page_with_category(self, page: int, location: str, category: str):
        """Get a selected jobs page in the requested category for a specified location 

        Args:
            page (int): The page number
            location (str): Location to search jobs for
            category (str): Category of the job (tag)

        Returns:
            json: {count, mean, results[id, title, description, created, redirect_url, adref, latitude, longitude, location]} 
        """
        try:
            r = requests.get(f"{self.base_url}/jobs/{location}/search/{page}?app_id={self.app_id}&app_key={self.api_key}&category={category}", headers=self.headers)
            r.raise_for_status()
            save_raw_data(json_data=r.json()["results"], 
                          type=SEARCH_TYPES.get(0),
                          location=location, 
                          page=page,
                          category=category)
            
        except HTTPError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except ConnectionError:
            print("Failed to connect - check your internet or the API url")
        except Timeout:
            print("Request timed out")
        except Exception as e:
            print(f"An error has occured: {e}")
        
        
    def get_categories(self, location: str):
        """Get all available categories used in searching

        Args:
            location (str): Location that categories are checked for

        Returns:
            json: {results:[tag, label, __CLASS__]} 
            - tag is the string that would be passed to the search endpoint as the "category" parameter
            - label is a text string that is suitable for displaying
        """
        try:
            r = requests.get(f"{self.base_url}/jobs/{location}/categories?app_id={self.app_id}&app_key={self.api_key}", headers=self.headers)
            r.raise_for_status()
            save_raw_data(json_data=r.json()["results"], 
                          type=SEARCH_TYPES.get(1),
                          location=location, 
                          page=1,
                          category="N/A")
        
        except HTTPError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except ConnectionError:
            print("Failed to connect - check your internet or the API url")
        except Timeout:
            print("Request timed out")
        except Exception as e:
            print(f"An error has occured: {e}")

def save_raw_data(json_data: Any, type: str, location: str, page: int, category: str): 
    """Save the raw data to data/raw and update the manifest to include the file

    Args:
        file_path (str): path to the file
        json_data (Any): json data to be saved
        type (str): {0: "results", 1: "categories"}
        location (str): location for the search
        page (int): page number of the search
        category (str): category of the job search e.g. it-job
    """
    
    current_date = datetime.today().strftime('%Y-%m-%d')
    if category == "N/A":
        file_name = f"{type}-{location}-{page}-{current_date}.json"
    else:
        file_name = f"{type}-{location}-{page}-{category}-{current_date}.json"
    
    with open(f"{RAW_DATA_PATH}/{file_name}", "w") as raw_file:
        json.dump(json_data, raw_file)
    print(f"Saved {file_name}.json successfully")
    
    # TODO
    # Updating manifest.json (NDJSON)
    # {filepath:f"{RAW_DATA_PATH}/{file_name}", type: results or categories, date: current_date, location: location, category:job_category, processed: true or false}
        

if __name__ == "__main__":
    client = AdzunaClient()
    #client.get_page(page=1, location="gb")["results"]
    client.get_categories("gb") 
    client.get_page_with_category(1, "gb", "it-jobs")
