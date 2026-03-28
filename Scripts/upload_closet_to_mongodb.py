"""
scripts/upload_closet_to_mongodb.py

Bulk uploads all tagged closet items from the /Closet folder to MongoDB.
Run this once to sync your entire wardrobe inventory to the database.

Usage:
    python scripts/upload_closet_to_mongodb.py
"""

import json
import os
from pathlib import Path
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

# -------------------------------------------------------
# MongoDB Connection
# -------------------------------------------------------
MONGO_URI = os.environ.get("MONGO_URI")

client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
db = client["fitcheck_women"]
collection = db["wardrobe_inventory"]

# -------------------------------------------------------
# Config
# -------------------------------------------------------
CLOSET_DIR = Path("Closet")

# -------------------------------------------------------
# Main Upload Function
# -------------------------------------------------------
def upload_closet_to_mongodb():
    """
    Reads all JSON files from /Closet folder and uploads to MongoDB.
    Skips duplicates using image_id as unique key.
    """

    # Check closet exists
    if not CLOSET_DIR.exists():
        print("❌ Closet folder not found! Make sure you're running from project root.")
        return

    json_files = list(CLOSET_DIR.glob("*.json"))

    if not json_files:
        print("❌ No JSON files found in Closet/ folder.")
        print("   Add items via the 'Add to Inventory' page first.")
        return

    print(f"📂 Found {len(json_files)} items in Closet/")
    print(f"🔗 Connecting to MongoDB...")

    # Test connection
    try:
        client.admin.command('ping')
        print("✅ MongoDB connected!\n")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return

    # Upload stats
    uploaded  = 0
    skipped   = 0
    failed    = 0

    for json_file in json_files:
        try:
            with open(json_file) as f:
                item = json.load(f)

            # Skip items with errors
            if "error" in item:
                print(f"⚠️  Skipping {json_file.name} — has error tag")
                failed += 1
                continue

            # Use image_id as unique identifier
            image_id = item.get("image_id")
            if not image_id:
                print(f"⚠️  Skipping {json_file.name} — no image_id")
                failed += 1
                continue

            # Check if already exists
            existing = collection.find_one({"image_id": image_id})
            if existing:
                print(f"⏭️  Skipping {json_file.name} — already in database")
                skipped += 1
                continue

            # Add metadata before uploading
            item["filename"]   = json_file.name
            item["uploaded_at"] = datetime.now(timezone.utc)
            item["source"]     = "closet_bulk_upload"

            # Insert into MongoDB
            collection.insert_one(item)
            print(f"✅ Uploaded: {json_file.name} "
                  f"| {item.get('item_type', '?')} "
                  f"| {item.get('color', '?')} "
                  f"| {item.get('style_persona', '?')}")
            uploaded += 1

        except Exception as e:
            print(f"❌ Failed {json_file.name}: {e}")
            failed += 1

    # Summary
    print(f"\n{'='*50}")
    print(f"✅ Uploaded : {uploaded} items")
    print(f"⏭️  Skipped  : {skipped} items (already existed)")
    print(f"❌ Failed   : {failed} items")
    print(f"📊 Total    : {collection.count_documents({})} items in MongoDB")
    print(f"{'='*50}")


# -------------------------------------------------------
# View what's in MongoDB
# -------------------------------------------------------
def view_mongodb_inventory():
    """Print a summary of what's currently in MongoDB."""

    print("\n📊 Current MongoDB Inventory:")
    print(f"{'='*50}")

    total = collection.count_documents({})
    print(f"Total items: {total}\n")

    if total == 0:
        print("Database is empty!")
        return

    # Count by item type
    from collections import Counter
    all_items = list(collection.find({}, {"item_type": 1, "color": 1, "style_persona": 1, "_id": 0}))

    types    = Counter(i.get("item_type", "Unknown") for i in all_items)
    personas = Counter(i.get("style_persona", "Unknown") for i in all_items)
    colors   = Counter(i.get("color", "Unknown") for i in all_items)

    print("By Item Type:")
    for item_type, count in types.most_common(10):
        print(f"  {item_type}: {count}")

    print("\nBy Style Persona:")
    for persona, count in personas.most_common():
        emoji = {"Gen-Z": "⚡", "Millennial": "✨", "Aesthetic": "🌿"}.get(persona, "❓")
        print(f"  {emoji} {persona}: {count}")

    print("\nTop Colors:")
    for color, count in colors.most_common(5):
        print(f"  {color}: {count}")

    print(f"{'='*50}")


# -------------------------------------------------------
# Clear MongoDB inventory (use with caution)
# -------------------------------------------------------
def clear_mongodb_inventory():
    """Delete all items from MongoDB inventory. Use with caution!"""
    confirm = input("⚠️  Are you sure you want to delete ALL items from MongoDB? (yes/no): ")
    if confirm.lower() == "yes":
        result = collection.delete_many({})
        print(f"🗑️  Deleted {result.deleted_count} items from MongoDB")
    else:
        print("❌ Cancelled")


# -------------------------------------------------------
# Run
# -------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "view":
            # python scripts/upload_closet_to_mongodb.py view
            client.admin.command('ping')
            view_mongodb_inventory()
        elif sys.argv[1] == "clear":
            # python scripts/upload_closet_to_mongodb.py clear
            client.admin.command('ping')
            clear_mongodb_inventory()
    else:
        # Default: upload
        upload_closet_to_mongodb()
        view_mongodb_inventory()