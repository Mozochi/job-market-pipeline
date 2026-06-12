import json
from pathlib import Path
from typing import Any

RAW_DATA_PATH = Path(__file__).parent.parent / "data" / "raw"
SILVER_DATA_PATH = Path(__file__).parent.parent / "data" / "silver"

def export_cleaned_data(data: Any, file_name: str):
    try:
        with open(f"{SILVER_DATA_PATH}/{file_name}", "w") as f:
            json.dump(data, f)
    except Exception as e:
        print(f"An error has occured: {e}")

def injest_data(file_name: str) -> Any:
    try:
        with open(f"{RAW_DATA_PATH}/{file_name}") as f:
            json_data = json.load(f)
            return json_data
            
    except FileNotFoundError as e:
        print(f"File {RAW_DATA_PATH}/{file_name} cannot be found: {e}")
        return 0
    except Exception as e:
        print(f"An error has occured: {e}")
        return 0
    
    

def transform_search(file_name: str) -> list:
    """Transforms the job search data pulled from the Adzuna API

    Args:
        file_name (str): File name of the .json file containing the raw api data

    Returns:
        jobs (list): returns a cleaned version of the raw api data, removing unnecessary columns
    """
    data = injest_data(file_name)
    jobs = []
    
    # Checking if data is empty
    if data == 0:
        print("An error has occured: No Data Found!")
        return jobs # Returns an empty list
    
    try: 
        data = data["results"]
    except Exception as e:
        print(f"Results column not found: {e}")
    
    for job_listing in data:
        jobs_dict = {
            "job_title": job_listing.get("title"),
            "location": job_listing.get("location"),
            "description": job_listing.get("description"),
            "company": job_listing.get("company", {}).get("display_name"),
            "category": job_listing.get("category", {}).get("label"),
            "job_link": job_listing.get("redirect_url")
        }
        jobs.append(jobs_dict)
    return jobs


def transform_category(file_name: str) -> list[tuple]:
    data = injest_data(file_name)
    categories = [] 
    
    # Checking if data is empty
    if data == 0:
        print("An error has occured: No Data Found!")
        return categories # Returns an empty list
    
    try:
        data = data["results"]
    except Exception as e:
        print(f"Results column not found: {e}")
        
    for category in data:
        category_dict = {
            "tag": category.get("tag"),
            "label": category.get("label")
        }
        categories.append(category_dict)
    return categories
    


#job_data = transform_search("results.json")
#export_cleaned_data(job_data, "jobs.json")

category_data = transform_category("categories.json")
export_cleaned_data(category_data, "categories_silver.json")