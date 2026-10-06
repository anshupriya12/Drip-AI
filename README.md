# Drip.AI — Women's AI Fashion Stylist

Upload a photo of an outfit and get a candid critique with a score and a style persona (Gen-Z, Millennial or Aesthetic). Upload a single garment and get complementary pieces from a product catalogue to complete the look.

[![Drip.AI Demo](https://img.youtube.com/vi/_hY9Hhaz1l8/0.jpg)](https://www.youtube.com/watch?v=_hY9Hhaz1l8)

> Click the thumbnail to watch the demo.

---

## What it actually does

| Feature | Page | How it works |
|---|---|---|
| **Outfit critique** | `Fashion AI Advisor.py` (home) | A vision-language model, **Qwen2.5-VL-3B-Instruct**, is prompted to return a style breakdown, a 0–100 rating, a one-line comment and a persona. Critiques are cached in MongoDB by perceptual image hash. |
| **Wardrobe tagging** | `pages/1_Add_to_Inventory.py` | **OpenAI CLIP ViT-B/32** (`openai/clip-vit-base-patch32`) scores each uploaded item against text labels (item type, colour, formality, indoor/outdoor, persona) and keeps the best match. Tags are saved to MongoDB. |
| **Outfit completion** | `pages/2_Get_Outfit_Suggestion.py` | CLIP detects the uploaded garment's category and colour; a **rule-based recommender** (`Drip/recommender.py`) picks products for the missing categories. See below. |

### Models — and what is *not* used

- **Qwen2.5-VL-3B-Instruct** — outfit critique (CPU, float32, inference only).
- **CLIP ViT-B/32 (`openai/clip-vit-base-patch32`)** — zero-shot garment detection, colour and persona tagging.
- This is the generic CLIP checkpoint. **It is not FashionCLIP**, and nothing is fine-tuned or trained in this repository; both models are used as-is for zero-shot inference.

### Recommendation logic — not RAG

The outfit recommender does **not** use embeddings, a vector index, vector search or an LLM. Per request it:

1. loads women's items from MongoDB (`find({"gender": "Women's"})`, cached for 5 minutes);
2. looks up which categories are missing from the outfit (`COMPLETION_MAP`, e.g. a top → bottoms, shoes, bags, accessories, outerwear);
3. filters candidates in Python by style persona, formality and indoor/outdoor tags;
4. ranks them with a hand-written colour-compatibility table (`COLOR_COMPAT`);
5. returns the top-scoring product per missing category.

CLIP is used only to understand the *uploaded* photo, not to retrieve products. There is no quantitative evaluation of recommendation quality yet.

### Catalogue

`Scripts/load_myntra_to_mongodb.py` downloads the [Myntra fashion product dataset](https://www.kaggle.com/datasets/djagatiya/myntra-fashion-product-dataset) from Kaggle, keeps women's items, assigns persona tags with keyword rules and loads them into MongoDB. The number of products depends on the dataset version and the script's filters; the home page of the app shows the live count.

---

## Project structure

```
Drip-AI/
├── Drip/                          Streamlit app
│   ├── Fashion AI Advisor.py      home page: outfit critique (entry point)
│   ├── analyze_outfit.py          Qwen2.5-VL critique engine + output parsers
│   ├── tagging.py                 CLIP zero-shot tagger / garment detector
│   ├── recommender.py             rule-based outfit completion (pure Python)
│   ├── db.py                      MongoDB connection (reads MONGO_URI from env)
│   ├── testmongoconnection.py     connectivity check
│   └── pages/
│       ├── 1_Add_to_Inventory.py
│       └── 2_Get_Outfit_Suggestion.py
├── Scripts/                       one-off data tooling
│   ├── load_myntra_to_mongodb.py
│   ├── upload_closet_to_mongodb.py
│   ├── bulk_tag_images.py
│   └── download_fashion_images.py
├── tests/                         pytest suite (no GPU / model downloads needed)
├── Dockerfile
├── requirements.txt
├── requirements-test.txt
└── .env.example
```

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/anshupriya12/Drip-AI.git
cd Drip-AI
python -m venv venv
# Windows: venv\Scripts\activate      macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment variables

Credentials are read from environment variables (or a local `.env` file). **Never commit real secrets** — `.env` is git-ignored.

```bash
cp .env.example .env     # Windows: copy .env.example .env
```

| Variable | Required | Used by | Description |
|---|---|---|---|
| `MONGO_URI` | **yes** | app + Scripts | MongoDB Atlas connection string |
| `MONGO_DB_NAME` | no | app + Scripts | database name (default `fitcheck_women`) |
| `PIXABAY_API_KEY` | no | `Scripts/download_fashion_images.py` | free key from <https://pixabay.com/api/docs/> |

If `MONGO_URI` is missing, the pages show a clear configuration error instead of connecting to an unintended database.

**MongoDB Atlas:** create a free cluster, add a dedicated database user with only the access it needs (readWrite on one database), and allow only your own IP (or your host's egress IPs) under *Network Access*. Avoid `0.0.0.0/0`.

### 3. Load the product catalogue (once)

```bash
python Scripts/load_myntra_to_mongodb.py      # needs a Kaggle API token (~/.kaggle/kaggle.json)
```

### 4. Run the app

```bash
streamlit run "Drip/Fashion AI Advisor.py"
```

Open <http://localhost:8501>. The first run downloads the models from Hugging Face (Qwen2.5-VL-3B is several GB) and they load lazily on first use. Critique runs on CPU and takes roughly 30–60 s per image.

---

## Docker

The image packages the Streamlit app in `Drip/` (CPU-only PyTorch). Secrets are **not** baked into the image — pass them at runtime.

```bash
docker build -t drip-ai .

docker run --rm -p 8501:8501 \
  --env-file .env \
  -v drip_hf_cache:/app/.cache/huggingface \
  drip-ai
```

- The named volume `drip_hf_cache` keeps downloaded model weights between runs.
- The container runs as a non-root user and exposes a Streamlit health check at `/_stcore/health`.
- Load the catalogue from inside the container with `docker exec -it <container> python Scripts/load_myntra_to_mongodb.py`.
- Give Docker enough memory for the 3B model (≈ 12 GB RAM, since it runs in float32 on CPU).

---

## Tests

```bash
pip install -r requirements-test.txt
pytest
```

The suite covers the recommender, the output parsers, the DB helper, a guard that fails if credential-looking strings are committed, and smoke tests that render every Streamlit page against an in-memory fake database. It does not download models.

---

## Security notes

- All credentials come from environment variables; `.env.example` contains placeholders only.
- MongoDB TLS certificate validation is enabled.
- Uploaded filenames are never used to build filesystem paths on the critique page (a random name is used), and the inventory page strips directory components.
- If you ever commit a secret, rotate it immediately — deleting it from the latest commit does not remove it from git history.

---

## Known limitations

- No quantitative evaluation of critique quality, tagging accuracy or recommendation quality.
- Critique scores come from an LLM prompt and are not calibrated.
- Persona filtering uses keyword rules, so some plain items (e.g. "jeans") never match the *Gen-Z* keyword list.

---

## Author

**Anshu Priya** · [GitHub](https://github.com/anshupriya12)

## License

For educational and non-commercial use.
