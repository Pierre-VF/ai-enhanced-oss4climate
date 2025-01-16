import json
import os
from datetime import date

import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

from oss4climate_ai_enhanced.data import FILE_LISTING_FEATHER, download_data
from oss4climate_ai_enhanced.src.llm_adapters.anthropic import AnthropicLlmAdapter

load_dotenv()
download_data()
df = pd.read_feather(FILE_LISTING_FEATHER).dropna()

TARGET_JSON_FILE = "data/topic_and_use_cases.json"
N_REPOSITORIES_TO_ASSESS = 50

if os.path.exists(TARGET_JSON_FILE):
    with open(TARGET_JSON_FILE, mode="r") as f:
        augmented_context = json.load(f)
else:
    augmented_context = {}

# Adding date of scraping for traceability
today_str = str(date.today())

client = AnthropicLlmAdapter()

for i, r in tqdm(df.head(N_REPOSITORIES_TO_ASSESS).iterrows()):
    url = r["url"]
    if url not in augmented_context.keys():
        print(f"Processing url={url}")
        # Truncating to avoid exploding credits
        truncated_readme = r["readme"][:30000]
        try:
            use_cases_i = client.extract_use_cases(readme_str=truncated_readme)
            topics_i = client.extract_topics(readme_str=truncated_readme)
            augmented_context[url] = {
                "use_cases": use_cases_i,
                "topics": topics_i,
                "date": today_str,
            }
        except Exception:
            print("Error with URL={url} ({e})")
    else:
        augmented_context[url]["date"] = today_str
        print(f"Skipping reprocessing of url={url}")


with open(TARGET_JSON_FILE, mode="w") as f:
    json.dump(
        augmented_context,
        f,
        indent=3,
    )


print("DoNE")
