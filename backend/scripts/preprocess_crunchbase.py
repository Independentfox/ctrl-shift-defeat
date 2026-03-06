"""Preprocess Crunchbase dataset into funding_patterns format."""
import csv
import json
import uuid
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent.parent / "data" / "raw"
OUT_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

docs = []

cb_files = list(RAW_DIR.glob("**/investments*.csv")) + list(RAW_DIR.glob("**/crunchbase*.csv")) + list(RAW_DIR.glob("**/*.csv"))
cb_files = [f for f in cb_files if "shark" not in f.name.lower()]

for f in cb_files[:1]:  # Take first matching file
    print(f"Processing {f.name}")
    with open(f, encoding="utf-8", errors="ignore") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            name = row.get("name", row.get("company_name", "Unknown"))
            category = row.get("category_list", row.get("market", "Other"))
            country = row.get("country_code", row.get("country", ""))
            status = row.get("status", row.get("operating_status", ""))
            funding = row.get("funding_total_usd", row.get("total_funding", "0"))
            founded = row.get("founded_year", row.get("founded_at", ""))

            try:
                funding_num = float(str(funding).replace(",", "").replace("$", ""))
            except (ValueError, TypeError):
                funding_num = 0

            industry = category.split("|")[0].strip() if category else "Other"
            founded_year = int(str(founded)[:4]) if str(founded)[:4].isdigit() else 2020

            docs.append({
                "id": f"cb_{uuid.uuid4().hex[:8]}",
                "company_name": name,
                "industry": industry,
                "geography": country if country else "Unknown",
                "founded_year": founded_year,
                "funding_rounds": int(row.get("funding_rounds", 1) or 1),
                "total_raised_usd": funding_num,
                "burn_rate_monthly": "",
                "runway_months": 0,
                "outcome": status or "Unknown",
                "b2b_or_b2c": "B2B" if any(x in industry.lower() for x in ["enterprise", "saas", "b2b"]) else "B2C",
                "revenue_model": "",
                "months_to_first_revenue": 0,
                "content": f"{name}: {industry} company in {country}. Founded {founded_year}. Raised ${funding_num:,.0f}. Status: {status}.",
            })

out_file = OUT_DIR / "funding_patterns.json"
json.dump(docs, open(out_file, "w"), indent=2)
print(f"\nSaved {len(docs)} funding patterns to {out_file}")
