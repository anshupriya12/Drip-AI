"""
recommender.py — rule-based outfit completion.

This is NOT retrieval-augmented generation and does not use vector search or
embeddings. Given the garment category detected in an uploaded photo, it:

  1. looks up which categories are missing from the outfit (COMPLETION_MAP),
  2. filters candidate products by persona, formality and indoor/outdoor tags,
  3. ranks the survivors with a hand-written colour-compatibility table
     (COLOR_COMPAT), and
  4. returns the top-ranked product per missing category.

All functions are pure so they can be unit-tested without Streamlit or MongoDB.
"""

# What to recommend for each detected category
COMPLETION_MAP = {
    "tops":        ["bottoms", "shoes", "bags", "accessories", "outerwear"],
    "bottoms":     ["tops", "shoes", "bags", "accessories", "outerwear"],
    "dresses":     ["shoes", "bags", "accessories", "outerwear"],
    "outerwear":   ["tops", "bottoms", "shoes", "bags"],
    "shoes":       ["tops", "bottoms", "bags", "accessories"],
    "bags":        ["tops", "bottoms", "shoes", "accessories"],
    "accessories": ["tops", "bottoms", "shoes", "bags"],
}

# -------------------------------------------------------
# Color compatibility
# -------------------------------------------------------
COLOR_COMPAT = {
    "black":    ["white","beige","cream","nude","red","pink","gold","silver","grey","blush","ivory"],
    "white":    ["black","navy","blue","red","pink","beige","grey","gold","coral","camel"],
    "beige":    ["black","white","brown","camel","navy","olive","burgundy","cream"],
    "navy":     ["white","beige","cream","gold","red","pink","grey","camel"],
    "grey":     ["black","white","pink","blush","navy","burgundy","yellow","camel"],
    "pink":     ["black","white","grey","nude","gold","blush","navy","beige"],
    "red":      ["black","white","navy","gold","beige","cream"],
    "blue":     ["white","beige","navy","gold","grey","brown","camel"],
    "green":    ["white","beige","brown","camel","gold","black","cream"],
    "brown":    ["beige","cream","white","olive","camel","gold","burgundy"],
    "camel":    ["black","white","beige","brown","navy","olive","cream","gold"],
    "burgundy": ["beige","grey","black","gold","cream","blush","camel"],
    "olive":    ["white","beige","brown","camel","black","cream"],
    "gold":     ["black","white","navy","burgundy","brown","beige"],
    "nude":     ["black","white","beige","camel","gold","blush"],
    "blush":    ["black","white","grey","gold","navy","beige"],
    "ivory":    ["black","brown","navy","camel","burgundy","gold"],
    "cream":    ["black","brown","navy","camel","burgundy","olive"],
}


def color_score(c1: str, c2: str) -> int:
    """2 = same colour, 1 = listed as compatible, 0 = no known match."""
    c1, c2 = c1.lower(), c2.lower()
    if c1 == c2:
        return 2
    return 1 if c2 in COLOR_COMPAT.get(c1, []) else 0


# -------------------------------------------------------
# Persona preferences
# -------------------------------------------------------
PERSONA_PREFS = {
    "Gen-Z":      ["crop top","cargo","wide leg","mini skirt","hoodie","sneakers","platform","ankle boots","corset","backpack","chunky"],
    "Millennial": ["blouse","shirt","trousers","midi skirt","dress","blazer","coat","loafers","flats","heels","handbag","tote","cardigan"],
    "Aesthetic":  ["dress","maxi","skirt","midi","blouse","cardigan","flats","sandals","handbag","clutch","scarf","lace","floral"],
    "All":        [],
}


def ok_persona(item_type: str, persona: str) -> bool:
    if persona == "All":
        return True
    prefs = PERSONA_PREFS.get(persona, [])
    return not prefs or any(p in item_type.lower() for p in prefs)


CATEGORY_KEYWORDS = {
    "tops":        ["top","blouse","shirt","t-shirt","tshirt","tank","crop","sweater","cardigan","hoodie","corset","sweatshirt","tunic","camisole","vest","kurti","pullover"],
    "bottoms":     ["jean","pant","trouser","legging","skirt","shorts","capri","cargo","palazzo","jogger","culotte"],
    "dresses":     ["dress","gown","jumpsuit","romper","coord","playsuit","saree","kurta"],
    "outerwear":   ["jacket","blazer","coat","shrug","cape","bomber","windbreaker","trench"],
    "shoes":       ["heel","pump","stiletto","wedge","sneaker","trainer","boot","sandal","loafer","flat","mule","shoe","footwear"],
    "bags":        ["bag","purse","tote","clutch","sling","backpack","crossbody","satchel","hobo","wallet"],
    "accessories": ["earring","necklace","bracelet","ring","jewel","sunglass","goggle","scarf","stole","hair","belt","watch"],
}


def get_cat(item_type: str) -> str:
    """Map a free-text item type to a coarse category by keyword match."""
    it = item_type.lower()
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(k in it for k in kws):
            return cat
    return "other"


def build_smart_outfit(
    items: list,
    uploaded_color: str,
    detected_category: str,
    persona: str,
    formality: str,
    location: str,
) -> dict:
    """
    Complete an outfit around an uploaded garment.

    For each category listed in COMPLETION_MAP[detected_category], keep the
    candidates that pass the persona / formality / location filters and pick
    the one whose colour scores highest against `uploaded_color`.
    """
    completion_cats = COMPLETION_MAP.get(detected_category, list(COMPLETION_MAP.keys()))
    outfit = {}

    for cat in completion_cats:
        candidates = []
        for item in items:
            item_cat = item.get("category_group") or item.get("category") or get_cat(item.get("item_type", ""))
            if item_cat != cat:
                continue
            if location == "Outdoor" and item.get("indoor_outdoor", "").lower() == "indoor":
                continue
            if formality == "Formal" and item.get("formality", "").lower() == "casual":
                continue
            if formality == "Casual" and item.get("formality", "").lower() == "formal":
                continue
            ip = item.get("style_persona", "")
            if persona != "All" and ip and ip != persona:
                continue
            if not ok_persona(item.get("item_type", ""), persona):
                continue
            candidates.append(item)

        if not candidates:
            continue

        scored = sorted(
            candidates,
            key=lambda i: color_score(uploaded_color, i.get("color", "").lower()),
            reverse=True,
        )
        outfit[cat] = scored[0]

    return outfit
