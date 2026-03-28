"""
Fixed download script using Pixabay free API
"""
import os, time, requests
from pathlib import Path
from PIL import Image
from io import BytesIO

PIXABAY_API_KEY = "55145021-509f10b32ffc1dee18fd54bf6"
SAVE_DIR = Path("Closet_Images")
SAVE_DIR.mkdir(exist_ok=True)

CATEGORIES = {
    "tops":        {"queries": ["women crop top", "women blouse fashion", "women tank top", "women shirt fashion", "women fashion top"], "count": 15},
    "jeans_pants": {"queries": ["women jeans fashion", "women wide leg pants", "women cargo pants", "women trousers"], "count": 12},
    "dresses":     {"queries": ["women summer dress", "women maxi dress", "women mini dress", "women floral dress", "women cocktail dress"], "count": 15},
    "skirts":      {"queries": ["women mini skirt", "women midi skirt", "women pleated skirt", "women denim skirt"], "count": 10},
    "jackets":     {"queries": ["women denim jacket", "women leather jacket", "women blazer", "women coat fashion"], "count": 10},
    "sneakers":    {"queries": ["women sneakers fashion", "women white sneakers", "women chunky sneakers"], "count": 12},
    "heels":       {"queries": ["women high heels", "women stiletto", "women block heels", "women pumps"], "count": 12},
    "boots":       {"queries": ["women ankle boots", "women knee boots", "women combat boots"], "count": 10},
    "handbags":    {"queries": ["women handbag", "women tote bag", "women shoulder bag", "women clutch"], "count": 12},
    "earrings":    {"queries": ["women earrings jewelry", "women hoop earrings", "women gold earrings"], "count": 10},
    "sunglasses":  {"queries": ["women sunglasses fashion", "women cat eye sunglasses"], "count": 10},
    "cardigans":   {"queries": ["women cardigan outfit", "women knit sweater", "women oversized cardigan"], "count": 12},
}

def get_urls(query, count):
    try:
        r = requests.get("https://pixabay.com/api/", params={"key": PIXABAY_API_KEY, "q": query, "image_type": "photo", "per_page": count, "safesearch": "true", "orientation": "vertical"}, timeout=10)
        return [h["webformatURL"] for h in r.json().get("hits", [])]
    except:
        return []

def save_img(url, path):
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content)).convert("RGB").resize((400, 500), Image.LANCZOS)
            img.save(path, "JPEG", quality=90)
            return True
    except:
        pass
    return False

def main():
    if PIXABAY_API_KEY == "YOUR_PIXABAY_API_KEY":
        print("❌ Set your Pixabay API key first!")
        print("   1. Go to: https://pixabay.com/api/docs/")
        print("   2. Sign up free")
        print("   3. Replace YOUR_PIXABAY_API_KEY in this script")
        return

    total = 0
    for cat, cfg in CATEGORIES.items():
        cat_dir = SAVE_DIR / cat
        cat_dir.mkdir(exist_ok=True)
        print(f"\n📂 {cat.upper()}")
        done, idx = 0, 1
        for q in cfg["queries"]:
            if done >= cfg["count"]: break
            for url in get_urls(q, min(5, cfg["count"]-done)):
                if done >= cfg["count"]: break
                p = cat_dir / f"{cat}_{idx:03d}.jpg"
                if not p.exists() and save_img(url, p):
                    print(f"  ✅ {p.name}")
                    done += 1; idx += 1; total += 1
                time.sleep(0.3)
        print(f"  → {done}/{cfg['count']} downloaded")

    print(f"\n✅ Total downloaded: {total}")
    print("Next: run streamlit app → Add to Inventory → upload images")

if __name__ == "__main__":
    main()
