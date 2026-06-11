import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout
from typing import Any
import os
from dotenv import load_dotenv
from pathlib import Path
import json

dotenv_path = Path(__file__).parent.parent / "configs" / ".env"
load_dotenv(dotenv_path)

API_KEY = os.getenv("ADZUNA_API_KEY")
APPLICATION_KEY = os.getenv("ADZUNA_APPLICATION_ID")

## TODO Need to update the returned type for the functions to fit the shape of the response

class AdzunaClient:
    def __init__(self):
        self.base_url = "https://api.adzuna.com/v1/api"
        self.headers = {"Accept" : "application/json"}
        self.api_key = API_KEY
        self.app_id = APPLICATION_KEY
        
    def get_page(self, page: int, location: str) -> Any:
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
            return r.json()
            
        except HTTPError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except ConnectionError:
            print("Failed to connect - check your internet or the API url")
        except Timeout:
            print("Request timed out")
        except Exception as e:
            print(f"An error has occured: {e}")
    
    
    def get_page_with_category(self, page: int, location: str, category: str) -> Any:
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
            return r.json()
            
        except HTTPError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except ConnectionError:
            print("Failed to connect - check your internet or the API url")
        except Timeout:
            print("Request timed out")
        except Exception as e:
            print(f"An error has occured: {e}")
        
        
    def get_categories(self, location: str) -> Any:
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
            r.raise_for_status
            return r.json()
        
        except HTTPError as e:
            print(f"HTTP error: {e.response.status_code} - {e.response.text}")
        except ConnectionError:
            print("Failed to connect - check your internet or the API url")
        except Timeout:
            print("Request timed out")
        except Exception as e:
            print(f"An error has occured: {e}")


if __name__ == "__main__":
    client = AdzunaClient()
    #page_data = client.get_page(page=1, location="gb")["results"]
    #category_data = client.get_categories("gb") 
    json_data = client.get_page_with_category(1, "gb", "it-jobs")

    with open("data/raw/results.json", "w") as f:
        json.dump(json_data, f)
    