"""Preprocess YC companies dataset. Place yc_companies.csv in data/raw/"""
import csv
import json
import uuid
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

docs = []

yc_files = list(RAW_DIR.glob("**/yc*.csv")) + list(RAW_DIR.glob("**/YC*.csv")) + list(RAW_DIR.glob("**/ycombinator*.csv"))

for f in yc_files[:1]:
    print(f"Processing {f.name}")
    with open(f, encoding="utf-8", errors="ignore") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            name = row.get("name", row.get("Company", "Unknown"))
            batch = row.get("batch", row.get("Batch", ""))
            desc = row.get("description", row.get("one_liner", row.get("Description", "")))
            industry = row.get("industry", row.get("tags", row.get("Industry", "Other")))
            status = row.get("status", row.get("Status", "Active"))

            docs.append({
                "id": f"yc_{uuid.uuid4().hex[:8]}",
                "company_name": name,
                "batch": batch,
                "industry": industry.split(",")[0].strip() if industry else "Other",
                "b2b_or_b2c": "B2B" if any(x in str(desc).lower() for x in ["enterprise", "business", "b2b"]) else "B2C",
                "stage_at_application": "Idea",
                "status": status,
                "team_size": 2,
                "has_technical_cofounder": True,
                "funding_raised_usd": 0,
                "description": desc,
                "key_success_factors": [],
                "geography": "Global",
                "content": f"YC {batch}: {name}. {desc}. Industry: {industry}. Status: {status}.",
            })

out_file = OUT_DIR / "yc_companies.json"
json.dump(docs, open(out_file, "w"), indent=2)
print(f"\nSaved {len(docs)} YC companies to {out_file}")
