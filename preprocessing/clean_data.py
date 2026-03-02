import json

def clean_data():
    with open("data/raw/shl_catalog_raw.json") as f:
        data = json.load(f)

    cleaned = []
    for item in data:
        if item["name"] != "N/A":
            cleaned.append({
                "name": item["name"],
                "url": item["url"],
                "description": item["description"]
            })

    with open("data/processed/shl_catalog_cleaned.json", "w") as f:
        json.dump(cleaned, f, indent=4)


if __name__ == "__main__":
    clean_data()