"""Preprocess Shark Tank datasets into combined_outcomes format."""
import csv
import json
import uuid
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

docs = []

# Process Shark Tank India (if available)
sti_files = list(RAW_DIR.glob("**/Shark Tank India*.csv")) + list(RAW_DIR.glob("**/shark_tank_india*.csv"))
for f in sti_files:
    print(f"Processing {f.name}")
    with open(f, encoding="utf-8", errors="ignore") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            brand = row.get("Brand Name", row.get("brand", "Unknown"))
            industry = row.get("Industry", row.get("industry", "Other"))
            deal = row.get("Deal", row.get("deal", "")).lower() in ("yes", "1", "true")
            season = row.get("Season Number", row.get("season", "1"))
            episode = row.get("Episode Number", row.get("episode", "1"))

            docs.append({
                "id": f"sti_s{season}_e{episode}_{uuid.uuid4().hex[:6]}",
                "source_type": "pitch_outcome",
                "title": brand,
                "summary": f"{brand} - {industry} startup pitched on Shark Tank India S{season}",
                "industry": industry,
                "b2b_or_b2c": "B2C",
                "geography": "India",
                "year": 2022 + int(str(season)) - 1 if str(season).isdigit() else 2022,
                "outcome": "Funded" if deal else "Rejected",
                "deal_given": deal,
                "ask_amount": row.get("Original Ask Amount", row.get("ask_amount", "")),
                "rejection_reasons": [],
                "funded_signals": [],
                "failure_reasons": [],
                "customer_objections": [],
                "content": f"Shark Tank India pitch: {brand}. Industry: {industry}. Deal: {'Yes' if deal else 'No'}. "
                          f"Ask: {row.get('Original Ask Amount', 'N/A')}. Remarks: {row.get('Remarks', 'N/A')}",
            })

# Process Shark Tank US (if available)
stu_files = list(RAW_DIR.glob("**/Shark Tank US*.csv")) + list(RAW_DIR.glob("**/shark_tank_us*.csv"))
for f in stu_files:
    print(f"Processing {f.name}")
    with open(f, encoding="utf-8", errors="ignore") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            title = row.get("title", row.get("company", "Unknown"))
            category = row.get("category", row.get("industry", "Other"))
            deal = row.get("deal", row.get("got_deal", "")).lower() in ("yes", "1", "true")
            season = row.get("season", "1")
            episode = row.get("episode", "1")

            docs.append({
                "id": f"stu_s{season}_e{episode}_{uuid.uuid4().hex[:6]}",
                "source_type": "pitch_outcome",
                "title": title,
                "summary": f"{title} - {category} pitched on Shark Tank US S{season}",
                "industry": category,
                "b2b_or_b2c": "B2C",
                "geography": "US",
                "year": 2009 + int(str(season)) - 1 if str(season).isdigit() else 2020,
                "outcome": "Funded" if deal else "Rejected",
                "deal_given": deal,
                "ask_amount": row.get("ask", row.get("askedFor", "")),
                "rejection_reasons": [],
                "funded_signals": [],
                "failure_reasons": [],
                "customer_objections": [],
                "content": f"Shark Tank US pitch: {title}. Category: {category}. Deal: {'Yes' if deal else 'No'}.",
            })

# Save
out_file = OUT_DIR / "combined_outcomes.json"
json.dump(docs, open(out_file, "w"), indent=2)
print(f"\nSaved {len(docs)} pitch outcomes to {out_file}")
