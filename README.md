# Drip.AI — *Where Gen-Z Streetwear, Millennial Minimalism & Aesthetic Romance Meet AI*

> **The only women's AI fashion stylist that understands your style persona.**
> Upload a clothing item → get a complete outfit in your aesthetic — *Gen-Z, Millennial, or Aesthetic.*

---

## ✨ What Makes This Different

Every other fashion AI recommends outfits generically.
**Drip.AI is the first to classify your style DNA before recommending.**

| Feature | Drip.AI |
|---|---|
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
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 3 — SMART RETRIEVAL                      │
│  Queries MongoDB (~9,000 women's items) filtered by:           │
│    • Style persona  (Gen-Z / Millennial / Aesthetic)           │
│    • Color compatibility  (colour theory rules)                │
│    • Formality  (casual / formal / party)                      │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STEP 4 — RESULT                               │
│  Complete outfit with Buy Now links → Myntra · Amazon · Ajio  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure
```
Drip.AI/
├── Drip/                              ← Main Streamlit app
│   ├── Fashion AI Advisor.py          ← Home: Outfit critique
│   ├── analyze_outfit.py              ← Qwen2.5-VL critique engine
│   ├── tagging.py                     ← CLIP women's item tagger
│   └── pages/
│       ├── 1_Add_to_Inventory.py      ← Upload + auto-tag clothes
│       └── 2_Get_Outfit_Suggestion.py ← Smart outfit recommender
│
├── Scripts/                           ← One-time setup scripts
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Vision AI** | CLIP (ViT-B/32) | Garment detection + item tagging |
| **Vision AI** | Qwen2.5-VL-3B-Instruct | Outfit critique + persona detection |
| **Style Classification** | CLIP zero-shot | Gen-Z / Millennial / Aesthetic labeling |
| **Database** | MongoDB Atlas | Wardrobe inventory + outfit critiques |
| **Product Catalog** | Myntra Kaggle Dataset | ~9,000 real women's products |
| **Backend** | Streamlit | Python web framework |
| **Deployment** | Hugging Face Spaces | Free cloud hosting |

---

## 🚀 Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/anshupriya12/Drip-AI.git
cd Drip-AI
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up MongoDB
- Create free cluster at [mongodb.com/atlas](https://mongodb.com/atlas)
- Update `MONGO_URI` in all Python files
- Add `0.0.0.0/0` to Network Access

### 5. Run the app
```bash
streamlit run "Drip/Fashion AI Advisor.py"
```

---

## 👩‍💻 Author

**Anshupriya** · [GitHub](https://github.com/anshupriya12)

Built as an end-to-end AI/ML portfolio project demonstrating:
Computer Vision · NLP · MLOps · Full-stack deployment · Product thinking

---

## 📄 License

This project is for educational and non-commercial use.

---

<div align="center">

**⚡ Gen-Z · ✨ Millennial · 🌿 Aesthetic**

*Drip.AI — Because your outfit deserves an honest critic.*

</div>
