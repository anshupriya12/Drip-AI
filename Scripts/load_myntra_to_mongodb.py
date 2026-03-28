r"""
Scripts/load_myntra_to_mongodb.py

Downloads Myntra Fashion Product Dataset from Kaggle,
filters ~6,000 women's items across your 12 categories,
assigns style personas, and loads into MongoDB.

Dataset: djagatiya/myntra-fashion-product-dataset
Columns: p_id, name, brand, price, rating, description,
         colour, img, alink (product URL)

Setup:
    1. Install kaggle: pip install kaggle
    2. Get Kaggle API key:
       - Go to kaggle.com → Account → Create API Token
       - Download kaggle.json
       - Place it at: C:\Users\Asus\.kaggle\kaggle.json
    3. Run: python Scripts/load_myntra_to_mongodb.py
"""

import os
import json
import pandas as pd
from pathlib import Path
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
from collections import Counter
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------------
# Config
# -------------------------------------------------------
MONGO_URI = os.environ.get("MONGO_URI")
DATASET_DIR = Path("data/myntra")
DATASET_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------------------------------------
# MongoDB Setup
# -------------------------------------------------------
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["fitcheck_women"]
collection = db["wardrobe_inventory"]

# -------------------------------------------------------
# Your 12 Category Mappings
# Maps Myntra product name keywords → your category groups
# -------------------------------------------------------
CATEGORY_MAP = {
    "tops": [
        "top", "blouse", "shirt", "tshirt", "t-shirt", "tank",
        "crop", "kurti", "tunic", "camisole", "corset",
        "sweatshirt", "pullover", "sweater", "cardigan",
        "hoodie", "vest", "tube"
    ],
    "jeans_pants": [
        "jeans", "jean", "pant", "trouser", "legging",
        "palazzo", "culotte", "jogger", "cargo", "capri",
        "shorts", "short", "skort"
    ],
    "dresses": [
        "dress", "gown", "jumpsuit", "romper", "co-ord",
        "coord", "playsuit", "maxi", "mini dress", "midi dress"
    ],
    "skirts": [
        "skirt", "lehnga", "lehenga", "sarong"
    ],
    "jackets": [
        "jacket", "blazer", "coat", "shrug", "cape",
        "overcoat", "trench", "bomber", "windbreaker"
    ],
    "sneakers": [
        "sneaker", "trainer", "sport shoe", "canvas shoe",
        "running shoe", "casual shoe", "athletic"
    ],
    "heels": [
        "heel", "pump", "stiletto", "wedge", "platform shoe",
        "court shoe", "block heel", "kitten heel"
    ],
    "boots": [
        "boot", "ankle boot", "knee boot", "chelsea",
        "combat boot", "western boot"
    ],
    "handbags": [
        "handbag", "bag", "purse", "tote", "satchel",
        "clutch", "sling", "backpack", "crossbody",
        "shoulder bag", "hobo", "bucket bag"
    ],
    "earrings": [
        "earring", "ear ring", "stud", "hoop", "drop earring",
        "jhumka", "chandbali", "ear cuff"
    ],
    "sunglasses": [
        "sunglass", "sunglasses", "eyewear", "goggle",
        "shades", "cat eye", "aviator", "wayf"
    ],
    "cardigans": [
        "cardigan", "shawl", "stole", "poncho", "wrap",
        "scarf", "muffler", "dupatta"
    ],
}

# -------------------------------------------------------
# Style Persona Assignment
# Based on product name + description keywords
# -------------------------------------------------------
PERSONA_KEYWORDS = {
    "Gen-Z": [
        "oversized", "crop", "cargo", "streetwear", "graphic",
        "y2k", "chunky", "platform", "grunge", "aesthetic",
        "tie dye", "neon", "bold", "statement", "corset",
        "mini", "baggy", "wide leg", "hoodie", "jogger"
    ],
    "Aesthetic": [
        "floral", "lace", "vintage", "boho", "bohemian",
        "cottagecore", "ruffle", "frill", "embroidered",
        "printed", "ethnic", "fusion", "embellished",
        "pearl", "velvet", "satin", "romantic", "feminine",
        "delicate", "pastel", "paisley", "mirror work"
    ],
    "Millennial": [
        "formal", "blazer", "tailored", "classic", "minimal",
        "office", "workwear", "business", "structured",
        "neutral", "solid", "basic", "smart", "professional",
        "elegant", "sophisticated", "midi", "capsule"
    ],
}

def assign_persona(name: str, description: str = "") -> str:
    """Assign style persona based on product name and description."""
    text = f"{name} {description}".lower()

    scores = {"Gen-Z": 0, "Aesthetic": 0, "Millennial": 0}
    for persona, keywords in PERSONA_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[persona] += 1

    best = max(scores, key=scores.get)
    # If no keywords matched, default based on category
    if scores[best] == 0:
        return "Millennial"
    return best


def get_category(product_name: str) -> str | None:
    """Map product name to one of your 12 categories."""
    name_lower = product_name.lower()
    for category, keywords in CATEGORY_MAP.items():
        if any(kw in name_lower for kw in keywords):
            return category
    return None


def get_color(colour_str: str) -> str:
    """Clean and normalize color string."""
    if not colour_str or pd.isna(colour_str):
        return "multicolor"
    # Take first color if multiple listed
    color = str(colour_str).split("/")[0].split(",")[0].strip().lower()
    return color if color else "multicolor"


def generate_myntra_url(product_name: str, p_id: str = "") -> str:
    """Generate Myntra search URL for a product."""
    query = product_name.replace(" ", "-").lower()
    if p_id:
        return f"https://www.myntra.com/{p_id}"
    return f"https://www.myntra.com/{query}"


# -------------------------------------------------------
# Step 1: Download Dataset
# -------------------------------------------------------
def download_dataset():
    """Download Myntra dataset from Kaggle."""
    csv_path = DATASET_DIR / "Fashion Dataset v2.csv"

    if csv_path.exists():
        print(f"✅ Dataset already downloaded at {csv_path}")
        return csv_path

    print("📥 Downloading Myntra dataset from Kaggle...")
    print("   Dataset: djagatiya/myntra-fashion-product-dataset")

    try:
        import kaggle
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(
            "djagatiya/myntra-fashion-product-dataset",
            path=str(DATASET_DIR),
            unzip=True
        )
        print(f"✅ Downloaded to {DATASET_DIR}")
    except Exception as e:
        print(f"❌ Kaggle download failed: {e}")
        print("\n📋 Manual download steps:")
        print("   1. Go to: https://www.kaggle.com/datasets/djagatiya/myntra-fashion-product-dataset")
        print("   2. Click Download")
        print(f"   3. Extract ZIP to: {DATASET_DIR.absolute()}")
        print("   4. Re-run this script")
        return None

    # Find the CSV file
    for f in DATASET_DIR.rglob("*.csv"):
        print(f"✅ Found CSV: {f}")
        return f

    return None


# -------------------------------------------------------
# Step 2: Process and Filter Women's Items
# -------------------------------------------------------
def process_dataset(csv_path: Path) -> list[dict]:
    """
    Load CSV, filter women's items across 12 categories,
    assign style personas, return list of item dicts.
    """
    print(f"\n📂 Loading dataset: {csv_path}")

    # Try different encodings
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(csv_path, encoding=encoding)
            print(f"✅ Loaded {len(df)} rows with {encoding} encoding")
            break
        except Exception:
            continue

    print(f"📊 Columns: {list(df.columns)}")
    print(f"📊 Sample row:\n{df.iloc[0]}\n")

    # Normalize column names to lowercase
    df.columns = df.columns.str.lower().str.strip()

    # Map common column name variants
    col_map = {}
    for col in df.columns:
        if "name" in col or "title" in col:
            col_map["name"] = col
        elif "price" in col or "mrp" in col or "cost" in col:
            col_map["price"] = col
        elif "brand" in col:
            col_map["brand"] = col
        elif "rating" in col:
            col_map["rating"] = col
        elif "colour" in col or "color" in col:
            col_map["colour"] = col
        elif "img" in col or "image" in col or "img_url" in col:
            col_map["img"] = col
        elif "link" in col or "url" in col or "alink" in col:
            col_map["alink"] = col
        elif "desc" in col or "description" in col:
            col_map["description"] = col
        elif "p_id" in col or "id" in col or "sku" in col:
            col_map["p_id"] = col
        elif "gender" in col:
            col_map["gender"] = col

    print(f"📊 Detected columns: {col_map}")

    # Filter women's items if gender column exists
    if "gender" in col_map:
        gender_col = col_map["gender"]
        women_keywords = ["women", "woman", "female", "girl", "ladies", "her"]
        women_mask = df[gender_col].str.lower().str.contains(
            "|".join(women_keywords), na=False
        )
        df_women = df[women_mask].copy()
        print(f"✅ After gender filter: {len(df_women)} women's items")
    else:
        # No gender column — filter by product name keywords
        print("⚠️  No gender column found — filtering by product name")
        women_name_keywords = [
            "women", "woman", "ladies", "female", "girl",
            "her ", "she ", "feminine"
        ]
        name_col = col_map.get("name", "name")
        women_mask = df[name_col].str.lower().str.contains(
            "|".join(women_name_keywords), na=False
        )
        df_women = df[women_mask].copy()
        if len(df_women) < 100:
            # Very few women-specific items found — use all items
            print("⚠️  Too few results — using full dataset")
            df_women = df.copy()

    items = []
    skipped = 0
    category_counts = Counter()

    for _, row in df_women.iterrows():
        # Get product name
        name_col = col_map.get("name", "name")
        name = str(row.get(name_col, "")).strip()
        if not name or name == "nan":
            skipped += 1
            continue

        # Map to your category
        category = get_category(name)
        if not category:
            skipped += 1
            continue

        # Get other fields safely
        price_col = col_map.get("price", "price")
        brand_col = col_map.get("brand", "brand")
        rating_col = col_map.get("rating", "rating")
        colour_col = col_map.get("colour", "colour")
        img_col = col_map.get("img", "img")
        link_col = col_map.get("alink", "alink")
        desc_col = col_map.get("description", "description")
        pid_col = col_map.get("p_id", "p_id")

        price = str(row.get(price_col, "")).strip()
        brand = str(row.get(brand_col, "")).strip()
        rating = str(row.get(rating_col, "")).strip()
        colour = get_color(row.get(colour_col, ""))
        img_url = str(row.get(img_col, "")).strip()
        product_url = str(row.get(link_col, "")).strip()
        description = str(row.get(desc_col, "")).strip()
        p_id = str(row.get(pid_col, "")).strip()

        # Clean up nan values
        for field in [price, brand, rating, img_url, product_url, description, p_id]:
            if field == "nan":
                field = ""

        # Assign style persona
        persona = assign_persona(name, description)

        # Generate Myntra buy link
        if not product_url or product_url == "nan":
            product_url = generate_myntra_url(name, p_id)

        # Determine formality from category + keywords
        formality_keywords = {
            "Formal": ["formal", "office", "business", "blazer", "suit"],
            "Party": ["party", "cocktail", "evening", "night", "festive"],
            "Casual": ["casual", "everyday", "basic", "comfort"],
        }
        formality = "Casual"
        name_lower = name.lower()
        for f, kws in formality_keywords.items():
            if any(kw in name_lower for kw in kws):
                formality = f
                break

        item = {
            "image_id":      f"myntra_{p_id}" if p_id else f"myntra_{hash(name)}",
            "item_type":     category.replace("_", " ").title(),
            "name":          name,
            "brand":         brand if brand != "nan" else "",
            "color":         colour,
            "price":         price if price != "nan" else "",
            "rating":        rating if rating != "nan" else "",
            "indoor_outdoor": "Outdoor" if category in ["sneakers", "heels", "boots"] else "Indoor",
            "formality":     formality,
            "gender":        "Women's",
            "style_persona": persona,
            "category_group": category,
            "img_url":       img_url if img_url != "nan" else "",
            "product_url":   product_url,
            "description":   description[:200] if description != "nan" else "",
            "source":        "myntra_kaggle",
            "path":          img_url if img_url != "nan" else "",
            "folder":        "Myntra",
        }

        items.append(item)
        category_counts[category] += 1

    print(f"\n✅ Processed {len(items)} women's items")
    print(f"⏭️  Skipped {skipped} items (no category match)")
    print(f"\n📊 Category breakdown:")
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat}: {count} items")

    return items


# -------------------------------------------------------
# Step 3: Upload to MongoDB
# -------------------------------------------------------
def upload_to_mongodb(items: list[dict]):
    """Upload processed items to MongoDB."""

    print(f"\n🔗 Connecting to MongoDB...")
    try:
        client.admin.command('ping')
        print("✅ MongoDB connected!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return

    uploaded = 0
    skipped  = 0
    failed   = 0

    print(f"\n📤 Uploading {len(items)} items to MongoDB...")

    for item in items:
        try:
            image_id = item.get("image_id")

            # Skip duplicates
            if collection.find_one({"image_id": image_id}):
                skipped += 1
                continue

            item["uploaded_at"] = datetime.now(timezone.utc)
            collection.insert_one(item)
            uploaded += 1

            if uploaded % 100 == 0:
                print(f"  ✅ Uploaded {uploaded}/{len(items)}...")

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed += 1

    print(f"\n{'='*55}")
    print(f"✅ Uploaded : {uploaded} items")
    print(f"⏭️  Skipped  : {skipped} items (already existed)")
    print(f"❌ Failed   : {failed} items")
    print(f"📊 Total in MongoDB: {collection.count_documents({})} items")
    print(f"{'='*55}")

    # Show persona distribution
    all_items = list(collection.find({}, {"style_persona": 1, "category_group": 1, "_id": 0}))
    personas = Counter(i.get("style_persona", "Unknown") for i in all_items)
    print(f"\n📊 Style Persona Distribution:")
    for persona, count in personas.most_common():
        emoji = {"Gen-Z": "⚡", "Millennial": "✨", "Aesthetic": "🌿"}.get(persona, "❓")
        print(f"  {emoji} {persona}: {count}")


# -------------------------------------------------------
# Main
# -------------------------------------------------------
if __name__ == "__main__":
    print("🛍️  FitCheck.AI — Myntra Dataset Loader")
    print("=" * 55)

    # Step 1: Download
    csv_path = download_dataset()

    if not csv_path:
        print("\n❌ Dataset not found. Please download manually.")
        print("   URL: https://www.kaggle.com/datasets/djagatiya/myntra-fashion-product-dataset")
        exit(1)

    # Step 2: Process
    items = process_dataset(csv_path)

    if not items:
        print("❌ No items processed!")
        exit(1)

    # Step 3: Upload
    upload_to_mongodb(items)

    print("\n✅ Done! Your MongoDB now has real Myntra products.")
    print("Run the app: streamlit run 'fitcheck/Fashion AI Advisor.py'")
    print("Try Get Outfit Suggestion — it will now use Myntra products! 🎉")
