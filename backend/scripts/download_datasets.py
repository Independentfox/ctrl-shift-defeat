"""Download datasets from Kaggle. Requires kaggle CLI: pip install kaggle"""
import subprocess
import os
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

DATASETS = [
    ("thirumani/shark-tank-us-dataset", "shark_tank_us"),
    ("arindam235/startup-investments-crunchbase", "crunchbase"),
]

# Note: For Shark Tank India and YC, search Kaggle for latest versions
# "shivavashishtha/shark-tank-india-dataset"
# YCombinator company dataset

for dataset_id, folder_name in DATASETS:
    out_dir = DATA_DIR / folder_name
    out_dir.mkdir(exist_ok=True)
    print(f"Downloading {dataset_id}...")
    subprocess.run(
        ["kaggle", "datasets", "download", "-d", dataset_id, "-p", str(out_dir), "--unzip"],
        check=True,
    )
    print(f"  -> Saved to {out_dir}")

print("\nDone! Now run the preprocessing scripts.")
print("NOTE: For CB Insights failure data, manually place cb_insights_failures.json in data/raw/")
