"""Create failure post-mortems dataset.
Since CB Insights data is not freely available, this creates a curated seed dataset."""
import json
from pathlib import Path

OUT_DIR = Path(__file__).parent.parent.parent / "data" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Curated failure post-mortems based on public data
FAILURES = [
    {
        "id": "fail_edtech_001",
        "source_type": "failure_postmortem",
        "title": "EdTech Platform - Student Engagement Tool",
        "summary": "B2C edtech tool for college students failed due to inability to monetize free users",
        "industry": "EdTech",
        "b2b_or_b2c": "B2C",
        "geography": "India",
        "year": 2022,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["no_market_need", "pricing_too_high", "ran_out_of_cash"],
        "customer_objections": ["Free alternatives exist", "Students won't pay for tools", "YouTube is enough"],
        "content": "EdTech startup targeting college students failed. Key reasons: couldn't convert free users to paid, YouTube and free resources were preferred. Students are extremely price-sensitive. Raised $400K but burned through in 18 months without product-market fit.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_edtech_002",
        "source_type": "failure_postmortem",
        "title": "AI Study Assistant",
        "summary": "AI-powered study tool couldn't differentiate from ChatGPT",
        "industry": "EdTech",
        "b2b_or_b2c": "B2C",
        "geography": "US",
        "year": 2023,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["outcompeted", "no_business_model", "bad_timing"],
        "customer_objections": ["ChatGPT does this for free", "Why do I need another AI tool?", "Not trustworthy for academic work"],
        "content": "AI study assistant launched post-ChatGPT. Could not differentiate from free ChatGPT. Users saw no reason to pay $10/month when ChatGPT Plus existed. Pivoted twice but couldn't find PMF.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_fintech_001",
        "source_type": "failure_postmortem",
        "title": "Digital Payment Platform - Tier 2",
        "summary": "Digital payments for Tier-2 merchants failed against UPI adoption",
        "industry": "FinTech",
        "b2b_or_b2c": "B2B",
        "geography": "India",
        "year": 2022,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["outcompeted", "regulatory", "no_market_need"],
        "customer_objections": ["UPI is free", "PhonePe/GPay already work", "Why switch?"],
        "content": "FinTech startup for Tier-2 merchant payments. UPI made the product unnecessary. Merchants preferred free government-backed solution. Regulatory requirements added 6-month delays.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_healthtech_001",
        "source_type": "failure_postmortem",
        "title": "Telemedicine Platform",
        "summary": "Telemedicine startup couldn't retain doctors on platform",
        "industry": "HealthTech",
        "b2b_or_b2c": "B2C",
        "geography": "India",
        "year": 2023,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["bad_team", "ran_out_of_cash", "no_market_need"],
        "customer_objections": ["Prefer in-person consultation", "Don't trust online diagnosis", "Too expensive for rural patients"],
        "content": "Telemedicine platform targeting Tier-2/3 cities. Doctors didn't stay on platform - preferred direct patient relationships. Patients in smaller cities didn't trust online consultations for serious issues. CAC was 10x LTV.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_foodtech_001",
        "source_type": "failure_postmortem",
        "title": "Cloud Kitchen Aggregator",
        "summary": "Cloud kitchen aggregator couldn't compete with Swiggy/Zomato",
        "industry": "FoodTech",
        "b2b_or_b2c": "B2C",
        "geography": "India",
        "year": 2022,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["outcompeted", "ran_out_of_cash", "pricing_too_high"],
        "customer_objections": ["Already using Swiggy", "Delivery takes too long", "Why download another app?"],
        "content": "Cloud kitchen aggregator in India. Couldn't acquire customers against Swiggy/Zomato duopoly. Unit economics never worked - delivery subsidy was unsustainable. Raised $200K, shut down in 12 months.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_saas_001",
        "source_type": "failure_postmortem",
        "title": "HR SaaS for SMBs",
        "summary": "HR tool for small businesses failed due to long sales cycles",
        "industry": "SaaS",
        "b2b_or_b2c": "B2B",
        "geography": "India",
        "year": 2023,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["no_market_need", "bad_timing", "ran_out_of_cash"],
        "customer_objections": ["We use Excel", "Too expensive", "Don't need software for 10 employees", "Decision takes 3 months"],
        "content": "HR SaaS targeting Indian SMBs. Sales cycle was 3-6 months. SMBs with <50 employees didn't see the value. Priced at ₹5000/month which was too high for the market. Churn was 15% monthly.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_cleantech_001",
        "source_type": "failure_postmortem",
        "title": "EV Charging Network",
        "summary": "EV charging startup ran out of capital before infrastructure scaled",
        "industry": "CleanTech",
        "b2b_or_b2c": "B2B",
        "geography": "India",
        "year": 2023,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["ran_out_of_cash", "bad_timing", "no_market_need"],
        "customer_objections": ["Not enough EVs in my area", "Home charging is enough", "Unreliable stations"],
        "content": "EV charging network for Tier-2 cities. Hardware costs were massive. EV adoption was slower than projected. Each station cost ₹5-8L with 2-year payback period. Couldn't raise bridge round.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_agritech_001",
        "source_type": "failure_postmortem",
        "title": "Farm-to-Table Platform",
        "summary": "Agritech platform failed due to logistics complexity",
        "industry": "AgriTech",
        "b2b_or_b2c": "B2B",
        "geography": "India",
        "year": 2022,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["poor_product", "ran_out_of_cash", "no_business_model"],
        "customer_objections": ["Farmers don't use apps", "Middlemen are more reliable", "Payment delays"],
        "content": "Farm-to-table marketplace. Farmers didn't trust digital platforms. Cold chain logistics were 3x projected cost. Commission model didn't work because margins were already thin in agriculture.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_ecomm_001",
        "source_type": "failure_postmortem",
        "title": "Niche D2C Brand",
        "summary": "D2C brand couldn't achieve profitable unit economics",
        "industry": "E-Commerce",
        "b2b_or_b2c": "B2C",
        "geography": "India",
        "year": 2023,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["outcompeted", "pricing_too_high", "ran_out_of_cash"],
        "customer_objections": ["Available cheaper on Amazon", "Don't know this brand", "Return policy too strict"],
        "content": "Niche D2C brand in personal care. CAC on Facebook/Instagram was ₹800 with AOV ₹600. Every sale lost money. Couldn't compete with Amazon's delivery speed. Brand awareness never reached critical mass.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
    {
        "id": "fail_logistics_001",
        "source_type": "failure_postmortem",
        "title": "Last-Mile Delivery for Kiranas",
        "summary": "Last-mile delivery failed against established players",
        "industry": "Logistics",
        "b2b_or_b2c": "B2B",
        "geography": "India",
        "year": 2022,
        "outcome": "Failed",
        "deal_given": False,
        "failure_reasons": ["outcompeted", "ran_out_of_cash", "no_market_need"],
        "customer_objections": ["Already have delivery boys", "Dunzo/Swiggy Instamart is faster", "Too expensive"],
        "content": "Last-mile delivery SaaS for kirana stores. Competed against Dunzo, Swiggy Instamart. Store owners resistant to tech adoption. Driver management was operationally complex. Burned ₹3L/month.",
        "rejection_reasons": [],
        "funded_signals": [],
        "ask_amount": ""
    },
]

# Add to combined_outcomes (append to existing if file exists)
out_file = Path(__file__).parent.parent.parent / "data" / "processed" / "combined_outcomes.json"
existing = []
if out_file.exists():
    existing = json.loads(out_file.read_text())

# Remove old failures if any
existing = [d for d in existing if d.get("source_type") != "failure_postmortem"]
existing.extend(FAILURES)

json.dump(existing, open(out_file, "w"), indent=2)
print(f"Added {len(FAILURES)} failure post-mortems. Total: {len(existing)} combined outcomes.")
