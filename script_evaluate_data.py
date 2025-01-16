import json
import os

import pandas as pd
from dotenv import load_dotenv

from oss4climate_ai_enhanced.data import FILE_LISTING_FEATHER, download_data

load_dotenv()
download_data()
df = pd.read_feather(FILE_LISTING_FEATHER).dropna()

TARGET_JSON_FILE = "data/topic_and_use_cases.json"
N_REPOSITORIES_TO_ASSESS = 200

if os.path.exists(TARGET_JSON_FILE):
    with open(TARGET_JSON_FILE, mode="r") as f:
        augmented_context = json.load(f)
else:
    raise RuntimeError("No data available")


topics = []
use_cases = []

cleaned_augmented_context = {}

reverse_dict_topics = {}
reverse_dict_use_cases = {}

for k, v in augmented_context.items():
    v_k = {i: [j.lower() for j in v.get(i)] for i in ["topics", "use_cases"]}
    topics += v_k.get("topics")
    use_cases += v_k.get("use_cases")
    cleaned_augmented_context[k] = v_k

    for i in v_k.get("topics"):
        if i in reverse_dict_topics:
            reverse_dict_topics[i].append(k)
        else:
            reverse_dict_topics[i] = [k]

    for i in v_k.get("use_cases"):
        if i in reverse_dict_use_cases:
            reverse_dict_use_cases[i].append(k)
        else:
            reverse_dict_use_cases[i] = [k]


def _keep_unique(x):
    y = pd.Series(x).unique()
    y.sort()
    return y


topics = _keep_unique(topics)
use_cases = _keep_unique(use_cases)

print("Topics:")
[print(f" - {k}: {reverse_dict_topics[k]}") for k in topics]
print(" ")
print("Use cases:")
[print(f" - {k}: {reverse_dict_use_cases[k]}") for k in use_cases]


print("DoNE")
