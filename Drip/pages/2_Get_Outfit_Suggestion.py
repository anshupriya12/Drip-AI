"""
2_Get_Outfit_Suggestion.py — Smart Women's Outfit Recommender
KEY FEATURE: Upload a clothing item → CLIP detects what it is
→ recommends COMPLEMENTARY pieces from MongoDB to complete the outfit.
This is the originality: the system understands what you have
and finds what you need — not just random filtering.
"""

import os
import sys
from pathlib import Path

import streamlit as st
from PIL import Image

# -------------------------------------------------------
# Make sibling modules (db, recommender, tagging) importable
# -------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent))
from db import MissingConfigError, get_collection
from recommender import build_smart_outfit
from tagging import COLOR_LABELS, classify as clip_classify, detect_garment_type

st.set_page_config(page_title="Outfit Recommender", page_icon="✨", layout="centered")

# -------------------------------------------------------
# Authentic Fashion CSS — same editorial palette
# -------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');
    html, body, [class*="css"] { font-family: 'Jost', sans-serif; font-weight: 300; letter-spacing: 0.02em; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 900px; }
    .page-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 2.8rem;
        font-weight: 300;
        font-style: italic;
        color: #f5f0eb;
        margin-bottom: 0.3rem;
    }
    .section-label {
        font-size: 0.62rem; font-weight: 400; letter-spacing: 0.3em;
        text-transform: uppercase; color: #D4AF37; margin: 1.5rem 0 0.8rem;
        display: flex; align-items: center; gap: 12px;
    }
    .section-label::after { content: ''; flex: 1; height: 1px; background: rgba(212,175,55,0.2); }
    /* Upload zone */
    [data-testid="stFileUploader"] {
        border: 1px solid rgba(212,175,55,0.2) !important;
        border-radius: 0 !important;
        background: rgba(212,175,55,0.02) !important;
    }
    /* Detected item banner */
    .detected-banner {
        background: rgba(212,175,55,0.06);
        border: 1px solid rgba(212,175,55,0.2);
        padding: 1rem 1.2rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .detected-icon { font-size: 1.4rem; }
    .detected-label { font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(245,240,235,0.4); }
    .detected-value { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; font-style: italic; color: #D4AF37; }
    /* Preference selects */
    .stSelectbox label {
        font-size: 0.62rem !important; letter-spacing: 0.2em !important;
        text-transform: uppercase !important; color: rgba(245,240,235,0.45) !important;
    }
    [data-baseweb="select"] > div {
        border-radius: 0 !important;
        border-color: rgba(212,175,55,0.2) !important;
        background: rgba(212,175,55,0.02) !important;
    }
    /* Recommend button */
    .stButton > button {
        background: transparent !important; color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important; border-radius: 0 !important;
        padding: 0.75rem !important; font-family: 'Jost', sans-serif !important;
        font-size: 0.68rem !important; letter-spacing: 0.3em !important;
        text-transform: uppercase !important; width: 100% !important;
        transition: all 0.3s !important;
    }
    .stButton > button:hover { background: #D4AF37 !important; color: #0d0d0d !important; }
    /* Outfit grid cards */
    .outfit-category {
        font-size: 0.58rem; letter-spacing: 0.25em; text-transform: uppercase;
        color: rgba(245,240,235,0.35); margin-bottom: 0.5rem; text-align: center;
    }
    .product-info {
        background: rgba(212,175,55,0.03);
        border-top: 1px solid rgba(212,175,55,0.1);
        padding: 0.6rem;
        text-align: center;
    }
    .product-name-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 0.85rem; font-style: italic; color: #f5f0eb;
        margin-bottom: 2px; line-height: 1.3;
    }
    .product-brand-text { font-size: 0.62rem; color: rgba(245,240,235,0.35); letter-spacing: 0.1em; text-transform: uppercase; }
    .product-price-text { font-size: 0.78rem; color: #D4AF37; font-weight: 400; margin: 3px 0; }
    .persona-pill {
        display: inline-block; padding: 2px 8px; border: 1px solid;
        font-size: 0.58rem; letter-spacing: 0.12em; text-transform: uppercase;
        margin-top: 4px;
    }
    .pill-genz { border-color: #ff6b9d; color: #ff6b9d; }
    .pill-millennial { border-color: #D4AF37; color: #D4AF37; }
    .pill-aesthetic { border-color: #9caf88; color: #9caf88; }
    /* Buy links */
    .buy-links { display: flex; gap: 4px; justify-content: center; margin-top: 6px; flex-wrap: wrap; }
    .buy-link {
        font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase;
        padding: 3px 8px; border: 1px solid rgba(212,175,55,0.3);
        color: rgba(245,240,235,0.5) !important; text-decoration: none !important;
        transition: all 0.2s;
    }
    .buy-link:hover { border-color: #D4AF37; color: #D4AF37 !important; }
    /* Summary table */
    .summary-row {
        display: flex; justify-content: space-between; align-items: baseline;
        padding: 0.6rem 0; border-bottom: 1px solid rgba(212,175,55,0.08);
        font-size: 0.78rem;
    }
    .summary-cat { color: rgba(245,240,235,0.4); letter-spacing: 0.1em; text-transform: uppercase; font-size: 0.62rem; }
    .summary-item { font-family: 'Cormorant Garamond', serif; font-style: italic; color: #f5f0eb; }
    .summary-price { color: #D4AF37; font-size: 0.72rem; }
    hr { border-color: rgba(212,175,55,0.12) !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# MongoDB
# -------------------------------------------------------
@st.cache_resource
def get_db():
    return get_collection("wardrobe_inventory")


try:
    collection = get_db()
except MissingConfigError as e:
    st.error(str(e))
    st.stop()

# -------------------------------------------------------
# Wardrobe items (cached for 5 minutes)
# -------------------------------------------------------
@st.cache_data(ttl=300)
def load_items():
    return list(collection.find({"gender": "Women's"}, {"_id": 0}))


# -------------------------------------------------------
# Display card
# -------------------------------------------------------
def show_card(item: dict, category: str):
    path    = item.get("path","")
    img_url = item.get("img_url") or item.get("image_url","")

    if path and os.path.exists(path):
        st.image(Image.open(path).convert("RGB"), use_container_width=True)
    elif img_url and img_url.startswith("http"):
        try:
            st.image(img_url, use_container_width=True)
        except Exception:
            st.markdown("🖼️")
    else:
        st.markdown(
            "<div style='height:160px;background:rgba(212,175,55,0.04);"
            "border:1px solid rgba(212,175,55,0.1);display:flex;align-items:center;"
            "justify-content:center;font-size:0.7rem;color:rgba(245,240,235,0.2);"
            "letter-spacing:0.1em'>NO IMAGE</div>",
            unsafe_allow_html=True
        )

    name        = (item.get("name") or item.get("product_name") or item.get("item_type","")).title()
    brand       = item.get("brand","")
    price       = item.get("price","")
    persona     = item.get("style_persona","")
    pc          = {"Gen-Z":"pill-genz","Millennial":"pill-millennial","Aesthetic":"pill-aesthetic"}.get(persona,"pill-millennial")
    pe          = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
    product_url = item.get("product_url","")

    # ── Use native Streamlit for text — avoids HTML escaping in columns ──
    st.markdown(f"*{name[:40]}*")
    if brand and str(brand) != "nan":
        st.caption(brand.upper())
    if price and str(price) != "nan":
        st.markdown(
            f"<div style='color:#D4AF37;font-size:0.78rem;text-align:center'>₹{price}</div>",
            unsafe_allow_html=True
        )
    if persona:
        st.markdown(
            f"<div style='text-align:center'>"
            f"<span class='persona-pill {pc}'>{pe} {persona}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    # ── Buy links ──
    query      = (name + " women").replace(" ", "+")
    links      = item.get("buy_links", {}) or {}
    myntra_url = links.get("myntra") or product_url or f"https://www.myntra.com/search?rawQuery={query}"
    amazon_url = links.get("amazon") or f"https://www.amazon.in/s?k={query}"
    ajio_url   = links.get("ajio")   or f"https://www.ajio.com/search/?text={query}"

    st.markdown(
        f"<div class='buy-links'>"
        f"<a href='{myntra_url}' target='_blank' class='buy-link'>Myntra</a>"
        f"<a href='{amazon_url}' target='_blank' class='buy-link'>Amazon</a>"
        f"<a href='{ajio_url}'   target='_blank' class='buy-link'>Ajio</a>"
        f"</div>",
        unsafe_allow_html=True
    )

# -------------------------------------------------------
# Page Header
# -------------------------------------------------------
st.markdown("""
<div style="padding: 2rem 0 1rem">
    <div style="font-size:0.62rem;letter-spacing:0.3em;text-transform:uppercase;color:#D4AF37;margin-bottom:0.5rem">Complete Your Look</div>
    <h1 class="page-title">Outfit Recommender</h1>
    <div style="font-size:0.72rem;font-weight:300;color:rgba(245,240,235,0.4);letter-spacing:0.05em">
        Upload what you're wearing → we find what completes it
    </div>
</div>
""", unsafe_allow_html=True)

# Stats bar
total        = collection.count_documents({"gender": "Women's"})
myntra_count = collection.count_documents({"source": "myntra_kaggle"})
st.markdown(f"""
<div style="font-size:0.62rem;letter-spacing:0.15em;color:rgba(245,240,235,0.25);padding:0.5rem 0 1.5rem;border-bottom:1px solid rgba(212,175,55,0.1)">
    {total:,} items in wardrobe — {myntra_count:,} Myntra products
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Upload Your Item
# -------------------------------------------------------
st.markdown('<div class="section-label">Upload the item you\'re wearing</div>', unsafe_allow_html=True)
uploaded_item = st.file_uploader(
    "Upload your top, jeans, dress — whatever you're working with",
    type=["jpg","jpeg","png","webp"],
    label_visibility="collapsed",
    key="item_upload"
)

detected_category = None
uploaded_color    = "black"

if uploaded_item:
    item_img = Image.open(uploaded_item).convert("RGB")

    col1, col2 = st.columns([1, 2], gap="large")
    with col1:
        st.image(item_img, use_container_width=True)

    with col2:
        with st.spinner("Identifying your item..."):
            detected_category, confidence = detect_garment_type(item_img)

        # Also detect color using CLIP
        uploaded_color = clip_classify(item_img, COLOR_LABELS).lower()

        st.markdown(f"""
        <div class="detected-banner">
            <div class="detected-icon">🎯</div>
            <div>
                <div class="detected-label">Detected item</div>
                <div class="detected-value">{detected_category.replace("_"," ").title()} — {uploaded_color.title()}</div>
            </div>
        </div>
        <div style="font-size:0.65rem;color:rgba(245,240,235,0.3);letter-spacing:0.08em">
            Confidence: {confidence:.0%} · We'll find pieces to complete this look
        </div>
        """, unsafe_allow_html=True)

# -------------------------------------------------------
# Preferences
# -------------------------------------------------------
st.markdown('<div class="section-label">Your Style Preferences</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    persona  = st.selectbox("Style Persona", ["All","Gen-Z","Millennial","Aesthetic"])
    location = st.selectbox("Location", ["Outdoor","Indoor"])
with col2:
    formality  = st.selectbox("Occasion", ["Casual","Smart Casual","Formal","Party","Streetwear"])
    pref_color = st.selectbox("Override Color", ["Auto (from image)","black","white","beige","navy","pink","red","blue","green","brown","gold","nude","blush"])

desc = {
    "Gen-Z":      "⚡ Y2K · Streetwear · Bold · Chunky shoes",
    "Millennial": "✨ Minimalist · Tailored · Smart casual · Classic",
    "Aesthetic":  "🌿 Cottagecore · Dark academia · Lace · Floral",
    "All":        "🎯 No filter — show all styles"
}
st.caption(desc.get(persona,""))
st.markdown("")

if st.button("Build My Outfit"):
    if not uploaded_item:
        st.warning("Upload the item you're wearing first — so we know what to complete.")
    else:
        # Use preferred color or auto-detected
        color_to_use = uploaded_color if pref_color == "Auto (from image)" else pref_color

        with st.spinner("Finding your perfect outfit..."):
            outfit = build_smart_outfit(
                items=load_items(),
                uploaded_color=color_to_use,
                detected_category=detected_category or "tops",
                persona=persona,
                formality=formality,
                location=location,
            )

        if not outfit:
            st.error("No matching items found. Try changing your filters or load more items with `python Scripts/load_myntra_to_mongodb.py`")
        else:
            pe_emoji = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
            st.markdown(f"""
            <div style="padding: 2rem 0 1rem">
                <div style="font-size:0.62rem;letter-spacing:0.3em;text-transform:uppercase;color:#D4AF37;margin-bottom:0.4rem">
                    {pe_emoji} Complete Outfit · {persona} · {formality}
                </div>
                <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-style:italic;color:#f5f0eb">
                    Here's what completes your look
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Show uploaded item first
            st.markdown('<div class="section-label">Your Item</div>', unsafe_allow_html=True)
            uc1, uc2, uc3 = st.columns([1, 2, 1])
            with uc2:
                st.image(item_img, caption=f"{detected_category.replace('_',' ').title()} — {uploaded_color.title()}", use_container_width=True)

            # Show recommended pieces
            st.markdown('<div class="section-label">Recommended to Complete Your Outfit</div>', unsafe_allow_html=True)

            cols = st.columns(min(len(outfit), 4))
            for i, (cat, item) in enumerate(outfit.items()):
                with cols[i % len(cols)]:
                    st.markdown(f'<div class="outfit-category">{cat.replace("_"," ")}</div>', unsafe_allow_html=True)
                    show_card(item, cat)

            # Summary
            st.markdown("---")
            st.markdown('<div class="section-label">Outfit Summary</div>', unsafe_allow_html=True)

            # Uploaded item row
            st.markdown(f"""
            <div class="summary-row">
                <span class="summary-cat">Your item</span>
                <span class="summary-item">{detected_category.replace("_"," ").title()} — {uploaded_color.title()}</span>
                <span class="summary-price">–</span>
            </div>
            """, unsafe_allow_html=True)

            for cat, item in outfit.items():
                name  = (item.get("name") or item.get("product_name") or item.get("item_type","")).title()
                price = item.get("price","")
                price_str = f"₹{price}" if price and price != "nan" else "–"
                st.markdown(f"""
                <div class="summary-row">
                    <span class="summary-cat">{cat.replace("_"," ")}</span>
                    <span class="summary-item">{name[:45]}</span>
                    <span class="summary-price">{price_str}</span>
                </div>
                """, unsafe_allow_html=True)
