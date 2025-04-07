import hashlib
import requests
from datetime import datetime, timedelta
import json
import os

SAVE_PATH = "hugewood_hash_output.json"
PREVIOUS_PATH = "hugewood_hash_prev.json"
DIFF_PATH = "hugewood_hash_diff.json"
COURTLISTENER_API = "https://www.courtlistener.com/api/rest/v3/opinions/"
GOVINFO_API_BASE = "https://api.govinfo.gov"
GOVINFO_API_KEY = "INSERT_YOUR_KEY_HERE"  # Replace with your govinfo.gov API key

def fetch_recent_scotus_opinions():
    try:
        params = {"court": "scotus", "date_filed_min": (datetime.utcnow() - timedelta(days=7)).date()}
        response = requests.get(COURTLISTENER_API, params=params)
        data = response.json()
        return [item['absolute_url'] for item in data.get('results', [])]
    except Exception as e:
        return [f"Error fetching SCOTUS opinions: {str(e)}"]

def fetch_recent_register_entries():
    try:
        url = f"{GOVINFO_API_BASE}/collections/FR/latest?api_key={GOVINFO_API_KEY}"
        response = requests.get(url)
        data = response.json()
        return [data.get("packageId", "Unknown FR Entry")]
    except Exception as e:
        return [f"Error fetching Federal Register: {str(e)}"]

def build_canonical_input():
    input_tree = {
        "timestamp": datetime.utcnow().isoformat(),
        "scotus_opinions": fetch_recent_scotus_opinions(),
        "circuit_splits": [
            "Qualified Immunity Standard (9th vs. 5th)",
            "Compelled Decryption (2nd vs. 11th)"
        ],
        "us_code_titles": {
            "Title_18": "Crimes and Criminal Procedure [live ref]",
            "Title_26": "Internal Revenue Code [live ref]"
        },
        "case_filings": {
            "date_range": "AUTO-LAST-7-DAYS",
            "estimated_count": "Use RECAP/PACER integration for full data"
        },
        "federal_register_updates": fetch_recent_register_entries(),
        "doctrine_vector": [
            "Katz v. US", "Carpenter v. US",
            "Dobbs v. Jackson", "Obergefell v. Hodges",
            "Chevron Doctrine", "Major Questions Doctrine"
        ]
    }
    return input_tree

def compute_hugewood_hash(input_tree: dict) -> str:
    serialized = json.dumps(input_tree, sort_keys=True)
    return hashlib.sha512(serialized.encode('utf-8')).hexdigest()

def compute_diff(new_tree: dict, old_tree: dict) -> dict:
    diff = {"added": {}, "removed": {}, "changed": {}}
    for key in new_tree:
        if key not in old_tree:
            diff["added"][key] = new_tree[key]
        elif new_tree[key] != old_tree[key]:
            diff["changed"][key] = {"from": old_tree[key], "to": new_tree[key]}
    for key in old_tree:
        if key not in new_tree:
            diff["removed"][key] = old_tree[key]
    return diff
