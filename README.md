---
title: FitCheck AI
emoji: 👗
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: "1.41.0"
app_file: fitcheck/Fashion AI Advisor.py
app_port: 8501
python_version: "3.11"
pinned: false
---

# FitCheck.AI — *Where Gen-Z Streetwear, Millennial Minimalism & Aesthetic Romance Meet AI*

> **The only women's AI fashion stylist that understands your style persona.**
> Upload a clothing item → get a complete outfit in your aesthetic — *Gen-Z, Millennial, or Aesthetic.*

---

## 🌐 Live Demo

> **[→ Add Live Link Here ←](#)**
> Deployed on Hugging Face Spaces / Streamlit Cloud

---

## ✨ What Makes This Different

Every other fashion AI recommends outfits generically.
**FitCheck.AI is the first to classify your style DNA before recommending.**

| Feature | Other Projects | FitCheck.AI |
|---|---|---|
| Style persona filter (Gen-Z / Millennial / Aesthetic) | ✅ **Core feature** |
| Detects uploaded garment with CLIP before recommending | ✅ |
| Recommends *complementary* pieces, not random items | ✅ |
| Women-specific category pipeline (35 garment types) | ✅ |
| Real Myntra product catalog (~9,000 products) | ✅ |
| Buy Now links (Myntra / Amazon / Ajio) | ✅ |
| Outfit critique with AI score + savage one-liner | ✅ |
| Editorial luxury UI (not generic Streamlit) | ✅ |

---

## 🎭 The Three Style Personas

```
⚡ Gen-Z                    ✨ Millennial               🌿 Aesthetic
─────────────────────       ─────────────────────       ─────────────────────
Y2K revival                 Minimalist & tailored       Cottagecore
Streetwear & cargo          Neutral tones               Dark academia
Chunky platform shoes       Structured bags             Lace & floral
Corsets & crop tops         Pointed flats               Prairie dresses
Bold graphics               Silk blouses                Velvet & vintage
Oversized silhouettes       Capsule wardrobe            Mary Janes & bows
```

These personas drive *everything* in the app — detection, recommendation, and critique.

---

## 🧠 How It Works

### Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER INPUT                               │
│  Upload clothing item (top / jeans / dress / shoes / bag...)   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 1 — DETECTION                            │
│  FashionCLIP (zero-shot) detects:                              │
│    • Garment type  →  "tops" / "bottoms" / "shoes" / etc.     │
│    • Color         →  "blue" / "black" / "blush" / etc.       │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 2 — COMPLETION MAP                       │
│  Determines what categories are MISSING from the outfit        │
│                                                                 │
│  uploaded: tops  →  complete with: bottoms, shoes,             │
│                     bags, accessories, outerwear                │
│                                                                 │
│  uploaded: dress →  complete with: shoes, bags,                │
│                     accessories, outerwear                      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 3 — SMART RETRIEVAL                      │
│  Queries MongoDB (~9,000 women's items) filtered by:           │
│    • Style persona  (Gen-Z / Millennial / Aesthetic)           │
│    • Color compatibility  (colour theory rules)                │
│    • Formality  (casual / formal / party)                      │
│    • Location   (indoor / outdoor)                             │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 4 — RESULT                               │
│  Complete outfit displayed with:                               │
│    • Product image + name + brand + price                      │
│    • Style persona badge (⚡ / ✨ / 🌿)                        │
│    • Buy Now links → Myntra · Amazon · Ajio                    │
│    • Outfit summary with total pieces                          │
└─────────────────────────────────────────────────────────────────┘
```

### Outfit Critique Pipeline (Fashion AI Advisor page)

```
Upload full outfit photo
        │
        ▼
Perceptual hashing (imagehash)
→ Check MongoDB for duplicate
        │
        ▼ (new outfit)
Qwen2.5-VL-3B (Vision Language Model)
→ Women's fashion prompt
→ Structured output: Style + Rating + Comment + Persona
        │
        ▼
Parse with regex
→ Display: Score /100 · Style breakdown · Savage verdict
→ Save to MongoDB (outfit_critiques collection)
```

---

## 🗂️ Project Structure

```
FitCheck.AI/
├── fitcheck/                          ← Main Streamlit app
│   ├── Fashion AI Advisor.py          ← Home: Outfit critique
│   ├── analyze_outfit.py              ← Qwen2.5-VL critique engine
│   ├── tagging.py                     ← CLIP women's item tagger
│   ├── testmongoconnection.py         ← MongoDB health check
│   └── pages/
│       ├── 1_Add_to_Inventory.py      ← Upload + auto-tag clothes
│       └── 2_Get_Outfit_Suggestion.py ← Smart outfit recommender
│
├── Scripts/                           ← One-time setup scripts
│   ├── download_fashion_images.py     ← Downloads 130 images (Pixabay)
│   ├── bulk_tag_images.py             ← CLIP-tags all images → JSON
│   ├── upload_closet_to_mongodb.py    ← Syncs Closet/ → MongoDB
│   └── load_myntra_to_mongodb.py      ← Loads ~9k Myntra products
│
├── Closet/                            ← Tagged JSON files (local)
├── Closet_Images/                     ← Downloaded fashion images
│   ├── tops/  bottoms/  dresses/      ← 12 women's categories
│   ├── shoes/ bags/ earrings/ ...
├── data/myntra/                       ← Myntra Kaggle dataset
├── Images/                            ← Temp upload folder (auto-cleared)
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Vision AI** | CLIP (ViT-B/32) | Garment detection + item tagging |
| **Vision AI** | Qwen2.5-VL-3B | Outfit critique + persona detection |
| **Style Classification** | CLIP zero-shot | Gen-Z / Millennial / Aesthetic labeling |
| **Database** | MongoDB Atlas | Wardrobe inventory + outfit critiques |
| **Product Catalog** | Myntra Kaggle Dataset | ~9,000 real women's products |
| **Backend** | Streamlit | Python web framework |
| **Image Processing** | PIL + imagehash | Image handling + deduplication |
| **Deployment** | Hugging Face Spaces | Free cloud hosting |

---

## 📊 Data Sources

| Source | Items | Style Persona | Use |
|---|---|---|---|
| **Myntra Kaggle Dataset** | ~9,000 | Keyword-assigned | Main product catalog |
| **Pixabay Fashion Images** | 130 | CLIP-assigned | Supplementary catalog |

### Persona Assignment Logic

```python
# Example — item scored against all 3 personas
name = "oversized cargo pants women"

Gen-Z keywords:   ["cargo", "oversized"] → score: 2  ✅ WINNER
Millennial kws:   []                     → score: 0
Aesthetic kws:    []                     → score: 0

→ Assigned: Gen-Z
```

---

## 🚀 Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/anshupriya12/FitCheck.AI.git
cd FitCheck.AI
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux
```

### 3. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set up MongoDB
- Create free cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
- Update `MONGO_URI` in all Python files

### 5. Load the Myntra product catalog (one-time)
```bash
python Scripts/load_myntra_to_mongodb.py
```

### 6. Tag your fashion images (one-time)
```bash
python Scripts/bulk_tag_images.py
python Scripts/upload_closet_to_mongodb.py
```

### 7. Run the app
```bash
streamlit run "fitcheck/Fashion AI Advisor.py"
```

Opens at `http://localhost:8501`

---

## 📱 App Pages

### 🏠 Home — Outfit Critique
- Upload any outfit photo
- Qwen2.5-VL analyzes: silhouette, fabric, colour theory
- Returns: Style score /100 · Breakdown · Savage one-liner
- Auto-detects style persona: Gen-Z / Millennial / Aesthetic
- Saves to MongoDB for deduplication

### 👗 Add to Inventory
- Upload individual clothing items
- CLIP auto-tags: item type, colour, formality, style persona
- Saves to local `Closet/` folder AND MongoDB
- Wardrobe stats dashboard with persona breakdown

### ✨ Get Outfit Suggestion
- Upload what you're wearing → CLIP detects it automatically
- App determines what's *missing* from your outfit
- Queries MongoDB for complementary pieces
- Filtered by: Style persona · Color compatibility · Occasion
- Shows: Product images · Prices · Buy links (Myntra/Amazon/Ajio)

---

## 🔬 What Makes the Recommendation Smart

Most outfit recommenders just filter by category.
FitCheck.AI uses a **Completion Map** + **Color Theory**:

```python
# If you upload a DRESS:
completion_map["dresses"] = ["shoes", "bags", "accessories", "outerwear"]
# → never suggests another dress or separate top/bottom

# Color scoring (example: you uploaded a navy item):
black item → score 1  (compatible with navy)
gold item  → score 1  (compatible with navy)
red item   → score 1  (compatible with navy)
navy item  → score 2  (exact match)
neon green → score 0  (not compatible)

# → Returns highest-scoring items per category
```

---

## 🏆 Resume Line

> *"Built end-to-end women's AI fashion stylist — CLIP zero-shot garment detection, Qwen2.5-VL outfit critique with style persona classification (Gen-Z/Millennial/Aesthetic), ~9,000 Myntra products in MongoDB with color-theory-based complementary outfit completion, editorial luxury Streamlit UI with Buy Now integration (Myntra/Amazon/Ajio)"*

---

## 👩‍💻 Author

**Anshupriya** · [GitHub](https://github.com/anshupriya12)

Built as an end-to-end AI/ML portfolio project demonstrating:
Computer Vision · NLP · MLOps · Full-stack deployment · Product thinking

---

## 📄 License

This project is for educational and non-commercial use.
Original FitCheck.AI concept by daniel-mehta — extended and transformed for women's fashion with style personas.

---

<div align="center">

**⚡ Gen-Z · ✨ Millennial · 🌿 Aesthetic**

*FitCheck.AI — Because your outfit deserves an honest critic.*

</div>
