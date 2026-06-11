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
    
    
    



def transform_search_data(file_name: str):
    data = injest_data(file_name)
    jobs = []
    
    data = data["results"]
    
    for i, job_listing in enumerate(data):
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

job_data = transform_search_data("results.json")
export_cleaned_data(job_data, "jobs.json")