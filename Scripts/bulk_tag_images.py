"""
scripts/bulk_tag_images.py

Automatically tags all images in Closet_Images/ folder using CLIP.
Creates one JSON file per image in Closet/ folder.
No manual uploading needed!

Usage:
    python Scripts/bulk_tag_images.py
"""

import os
import sys
import json
import torch
from pathlib import Path
from PIL import Image
import imagehash
from transformers import CLIPProcessor, CLIPModel

# -------------------------------------------------------
# Add fitcheck to path so we can import tagging.py
# -------------------------------------------------------
sys.path.insert(0, str(Path("fitcheck")))

# -------------------------------------------------------
# Device setup
# -------------------------------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"🔧 Using device: {device}")

# -------------------------------------------------------
# Load CLIP model
# -------------------------------------------------------
print("⏳ Loading CLIP model...")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
print("✅ CLIP model loaded!\n")

# -------------------------------------------------------
# Women's Label Sets
# -------------------------------------------------------
ITEM_LABELS = [
    "crop top", "blouse", "tank top", "shirt", "t-shirt",
    "sweater", "cardigan", "hoodie", "corset top",
    "jeans", "leggings", "skirt", "mini skirt", "midi skirt",
    "shorts", "trousers", "wide leg pants", "cargo pants",
    "dress", "mini dress", "maxi dress", "jumpsuit",
    "jacket", "blazer", "coat", "denim jacket", "leather jacket",
    "heels", "sneakers", "sandals", "boots", "ankle boots",
    "flats", "loafers", "platform shoes", "mules",
    "handbag", "tote bag", "clutch", "crossbody bag", "backpack",
    "earrings", "necklace", "bracelet", "sunglasses",
    "hair accessory", "belt", "scarf"
]

COLOR_LABELS = [
    "black", "white", "grey", "beige", "cream", "nude",
    "pink", "hot pink", "blush", "rose", "red", "burgundy",
    "blue", "navy", "baby blue", "cobalt",
    "green", "olive", "sage", "mint",
    "yellow", "mustard", "gold", "orange", "peach",
    "purple", "lavender", "lilac",
    "brown", "camel", "tan",
    "silver", "multicolor", "printed", "floral"
]

LOCATION_LABELS = ["Indoor", "Outdoor"]

FORMALITY_LABELS = [
    "Casual", "Formal", "Smart Casual",
    "Party", "Streetwear", "Athleisure"
]

STYLE_PERSONA_LABELS = [
    "Gen-Z streetwear style",
    "Millennial minimalist style",
    "Aesthetic cottagecore style"
]

PERSONA_MAP = {
    "Gen-Z streetwear style": "Gen-Z",
    "Millennial minimalist style": "Millennial",
    "Aesthetic cottagecore style": "Aesthetic"
}

SHOE_KEYWORDS = [
    "heel", "sneaker", "boot", "sandal",
    "loafer", "flat", "mule", "platform"
]

# -------------------------------------------------------
# CLIP classify helper
# -------------------------------------------------------
def classify(image: Image.Image, labels: list) -> str:
    """Return label with highest CLIP similarity score."""
    inputs = processor(
        text=labels,
        images=image,
        return_tensors="pt",
        padding=True
    ).to(device)
    outputs = model(**inputs)
    probs = outputs.logits_per_image.softmax(dim=1)
    return labels[probs.argmax().item()]

# -------------------------------------------------------
# Tag single image
# -------------------------------------------------------
def tag_image(image_path: Path) -> dict:
    """Tag a single clothing image with CLIP."""
    try:
        image = Image.open(image_path).convert("RGB")
        phash = str(imagehash.phash(image))

        item_type  = classify(image, ITEM_LABELS).capitalize()
        color      = classify(image, COLOR_LABELS).capitalize()

        # Shoes are always outdoor
        if any(kw in item_type.lower() for kw in SHOE_KEYWORDS):
            indoor_outdoor = "Outdoor"
        else:
            indoor_outdoor = classify(image, LOCATION_LABELS)

        formality    = classify(image, FORMALITY_LABELS)
        raw_persona  = classify(image, STYLE_PERSONA_LABELS)
        style_persona = PERSONA_MAP.get(raw_persona, "Millennial")

        return {
            "image_id":      phash,
            "item_type":     item_type,
            "color":         color,
            "indoor_outdoor": indoor_outdoor,
            "formality":     formality,
            "gender":        "Women's",
            "style_persona": style_persona,
            "path":          str(image_path),
            "folder":        "Closet"
        }

    except Exception as e:
        return {"error": str(e), "path": str(image_path)}

# -------------------------------------------------------
# Bulk tag all images
# -------------------------------------------------------
def bulk_tag():
    """Tag all images in Closet_Images/ and save JSONs to Closet/."""

    source_dir = Path("Closet_Images")
    closet_dir = Path("Closet")
    closet_dir.mkdir(exist_ok=True)

    if not source_dir.exists():
        print("❌ Closet_Images/ folder not found!")
        print("   Run: python Scripts/download_fashion_images.py first")
        return

    # Collect all images
    all_images = []
    for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
        all_images.extend(source_dir.rglob(ext))

    if not all_images:
        print("❌ No images found in Closet_Images/")
        return

    print(f"📂 Found {len(all_images)} images to tag")
    print(f"💾 JSON files will be saved to: {closet_dir.absolute()}\n")

    # Stats
    success = 0
    failed  = 0
    skipped = 0

    for i, img_path in enumerate(all_images, 1):
        json_path = closet_dir / f"{img_path.stem}.json"

        # Skip if already tagged
        if json_path.exists():
            print(f"[{i:03d}/{len(all_images)}] ⏭️  {img_path.name} — already tagged")
            skipped += 1
            continue

        print(f"[{i:03d}/{len(all_images)}] 🏷️  Tagging: {img_path.name}")
        tags = tag_image(img_path)

        if "error" in tags:
            print(f"           ❌ Error: {tags['error']}")
            failed += 1
            continue

        # Save JSON
        with open(json_path, "w") as f:
            json.dump(tags, f, indent=2)

        print(
            f"           ✅ {tags['item_type']} | "
            f"{tags['color']} | "
            f"{tags['style_persona']}"
        )
        success += 1

    # Summary
    print(f"\n{'='*55}")
    print(f"✅ Tagged   : {success} images")
    print(f"⏭️  Skipped  : {skipped} images (already done)")
    print(f"❌ Failed   : {failed} images")
    print(f"\n📂 JSON files saved to: {closet_dir.absolute()}")
    print(f"\n{'='*55}")
    print("✅ Next step — upload to MongoDB:")
    print("   python Scripts/upload_closet_to_mongodb.py")
    print(f"{'='*55}")


if __name__ == "__main__":
    bulk_tag()
