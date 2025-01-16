import os
from urllib.request import urlretrieve

FILE_OUTPUT_DIR: str = ".data"
URL_BASE = "https://data.pierrevf.consulting/oss4climate"

FILE_LISTING_FEATHER = f"{FILE_OUTPUT_DIR}/listing_data.feather"
URL_LISTING_FEATHER = f"{URL_BASE}/listing_data.feather"


def download_data(force_refresh: bool = False):
    os.makedirs(FILE_OUTPUT_DIR, exist_ok=True)
    if force_refresh or (not os.path.exists(FILE_LISTING_FEATHER)):
        print("Fetching feather data")
        urlretrieve(URL_LISTING_FEATHER, FILE_LISTING_FEATHER)
        print("Fetching completed")
