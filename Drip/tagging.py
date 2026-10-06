"""
tagging.py — Women's Fashion Tagger
Zero-shot tagging with OpenAI CLIP (ViT-B/32): the image and a list of text
labels are embedded in the same space and the best-matching label wins.

Note: this is the generic `openai/clip-vit-base-patch32` checkpoint, not
FashionCLIP and not fine-tuned on fashion data. No model is trained here.
"""

from functools import lru_cache

from PIL import Image
import imagehash

CLIP_MODEL_ID = "openai/clip-vit-base-patch32"


@lru_cache(maxsize=1)
def get_clip():
    """Load CLIP once per process (lazily, so importing this module is cheap)."""
    import torch
    from transformers import CLIPModel, CLIPProcessor

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    processor = CLIPProcessor.from_pretrained(CLIP_MODEL_ID)
    model = CLIPModel.from_pretrained(CLIP_MODEL_ID).to(device).eval()
    return processor, model, device

# -------------------------------------------------------
# Women's Label Sets
# -------------------------------------------------------

ITEM_LABELS = [
    # Tops
    "crop top", "blouse", "tank top", "shirt", "t-shirt",
    "sweater", "cardigan", "hoodie", "corset top",
    # Bottoms
    "jeans", "leggings", "skirt", "mini skirt", "midi skirt",
    "shorts", "trousers", "wide leg pants", "cargo pants",
    # Dresses & Jumpsuits
    "dress", "mini dress", "maxi dress", "jumpsuit", "co-ord set",
    # Outerwear
    "jacket", "blazer", "coat", "denim jacket", "leather jacket",
    # Shoes
    "heels", "sneakers", "sandals", "boots", "ankle boots",
    "flats", "loafers", "platform shoes", "mules",
    # Bags
    "handbag", "tote bag", "clutch", "crossbody bag", "backpack",
    # Accessories
    "earrings", "necklace", "bracelet", "sunglasses",
    "hair accessory", "belt", "scarf"
]

COLOR_LABELS = [
    # Neutrals
    "black", "white", "grey", "beige", "cream", "nude", "ivory",
    # Pinks & Reds
    "pink", "hot pink", "blush", "rose", "red", "burgundy", "maroon", "coral",
    # Blues
    "blue", "navy", "baby blue", "cobalt", "denim blue", "sky blue",
    # Greens
    "green", "olive", "sage", "mint", "forest green", "emerald",
    # Yellows & Oranges
    "yellow", "mustard", "gold", "orange", "peach",
    # Purples
    "purple", "lavender", "lilac", "mauve",
    # Browns
    "brown", "camel", "tan", "chocolate",
    # Metallics & Special
    "silver", "multicolor", "printed", "floral", "striped", "checkered"
]

LOCATION_LABELS = ["Indoor", "Outdoor"]

FORMALITY_LABELS = [
    "Casual", "Formal", "Smart Casual",
    "Party", "Streetwear", "Athleisure"
]

# Fixed to Women's only — no more misclassification
GENDER_LABELS = ["Women's"]

# -------------------------------------------------------
# Style Persona Labels (YOUR ORIGINALITY)
# -------------------------------------------------------
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

# -------------------------------------------------------
# Helper: classify
# -------------------------------------------------------
def classify_with_confidence(image, labels):
    """Return (best_label, softmax_probability) for the CLIP zero-shot match."""
    import torch

    processor, model, device = get_clip()
    inputs = processor(
        text=labels,
        images=image,
        return_tensors="pt",
        padding=True
    ).to(device)
    with torch.no_grad():
        probs = model(**inputs).logits_per_image.softmax(dim=1)[0]
    best_idx = int(probs.argmax().item())
    return labels[best_idx], float(probs[best_idx].item())


def classify(image, labels):
    """Return label with highest CLIP similarity."""
    return classify_with_confidence(image, labels)[0]


# Prompts used to detect what kind of garment was uploaded (zero-shot)
CATEGORY_LABELS = {
    "tops":        "a women's top, blouse, shirt, crop top, tank top or sweater",
    "bottoms":     "women's jeans, pants, trousers, shorts, leggings or skirt",
    "dresses":     "a women's dress, jumpsuit, maxi dress or mini dress",
    "outerwear":   "a women's jacket, coat, blazer or cardigan",
    "shoes":       "women's shoes, heels, sneakers, boots or sandals",
    "bags":        "a women's handbag, tote bag, clutch or purse",
    "accessories": "women's jewellery, earrings, necklace, sunglasses or scarf",
}


def detect_garment_type(image):
    """Zero-shot CLIP: which garment category was uploaded? -> (category, confidence)."""
    keys = list(CATEGORY_LABELS.keys())
    label, conf = classify_with_confidence(image, list(CATEGORY_LABELS.values()))
    best_cat = keys[list(CATEGORY_LABELS.values()).index(label)]
    return best_cat, conf

# -------------------------------------------------------
# Main: tag_closet_item
# -------------------------------------------------------
def tag_closet_item(image_path: str) -> dict:
    """
    Tag a women's clothing item with:
    - item type (women's specific)
    - color (expanded women's palette)
    - indoor/outdoor
    - formality
    - style persona (Gen-Z / Millennial / Aesthetic)
    - gender (always Women's)
    """
    try:
        image = Image.open(image_path).convert("RGB")
        phash = str(imagehash.phash(image))

        item_type = classify(image, ITEM_LABELS).capitalize()
        color = classify(image, COLOR_LABELS).capitalize()

        # Shoes are always outdoor
        if any(shoe in item_type.lower() for shoe in ["heel", "sneaker", "boot", "sandal", "loafer", "flat", "mule", "platform"]):
            indoor_outdoor = "Outdoor"
        else:
            indoor_outdoor = classify(image, LOCATION_LABELS)

        formality = classify(image, FORMALITY_LABELS)

        # Always Women's — no misclassification
        gender = "Women's"

        # Style persona classification (your originality)
        raw_persona = classify(image, STYLE_PERSONA_LABELS)
        style_persona = PERSONA_MAP.get(raw_persona, "Millennial")

        return {
            "image_id": phash,
            "item_type": item_type,
            "color": color,
            "indoor_outdoor": indoor_outdoor,
            "formality": formality,
            "gender": gender,
            "style_persona": style_persona,
            "path": image_path,
            "folder": "Closet"
        }

    except Exception as e:
        return {"error": str(e)}
