"""
1_Add_to_Inventory.py — Women's Wardrobe Manager
Editorial luxury fashion UI.
Upload → CLIP tags → saves to Closet/ + MongoDB.
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st
from PIL import Image

sys.path.insert(0, str(Path(__file__).parent.parent))
from db import MissingConfigError, get_collection
from tagging import tag_closet_item

st.set_page_config(page_title="Wardrobe", page_icon="👗", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');

    html, body, [class*="css"] { font-family: 'Jost', sans-serif; font-weight: 300; letter-spacing: 0.02em; }
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 860px; }

    .page-title { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; font-weight: 300; font-style: italic; color: #f5f0eb; }
    .section-label {
        font-size: 0.62rem; font-weight: 400; letter-spacing: 0.3em; text-transform: uppercase;
        color: #D4AF37; margin: 1.5rem 0 0.8rem; display: flex; align-items: center; gap: 12px;
    }
    .section-label::after { content: ''; flex: 1; height: 1px; background: rgba(212,175,55,0.2); }

    [data-testid="stFileUploader"] {
        border: 1px solid rgba(212,175,55,0.2) !important;
        border-radius: 0 !important; background: rgba(212,175,55,0.02) !important;
    }

    /* Tag pills */
    .tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.8rem 0; }
    .tag { padding: 4px 12px; font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase; border: 1px solid; }
    .tag-type { border-color: rgba(167,139,250,0.4); color: rgba(167,139,250,0.8); }
    .tag-color { border-color: rgba(212,175,55,0.4); color: rgba(212,175,55,0.8); }
    .tag-formal { border-color: rgba(156,175,136,0.4); color: rgba(156,175,136,0.8); }
    .tag-genz { border-color: rgba(255,107,157,0.4); color: rgba(255,107,157,0.8); }
    .tag-millennial { border-color: rgba(212,175,55,0.4); color: rgba(212,175,55,0.8); }
    .tag-aesthetic { border-color: rgba(156,175,136,0.4); color: rgba(156,175,136,0.8); }

    .stButton > button {
        background: transparent !important; color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important; border-radius: 0 !important;
        padding: 0.75rem !important; font-family: 'Jost', sans-serif !important;
        font-size: 0.68rem !important; letter-spacing: 0.3em !important;
        text-transform: uppercase !important; width: 100% !important; transition: all 0.3s !important;
    }
    .stButton > button:hover { background: #D4AF37 !important; color: #0d0d0d !important; }

    /* Stats grid */
    .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: rgba(212,175,55,0.12); margin: 1rem 0; }
    .stat-cell { background: #0d0d0d; padding: 1.2rem 1rem; text-align: center; }
    .stat-number { font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 300; color: #D4AF37; line-height: 1; }
    .stat-label { font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(245,240,235,0.3); margin-top: 4px; }

    /* Wardrobe grid item */
    .wardrobe-item { background: rgba(212,175,55,0.02); border: 1px solid rgba(212,175,55,0.08); padding: 6px; margin-bottom: 6px; }
    .wardrobe-caption { font-size: 0.62rem; letter-spacing: 0.05em; color: rgba(245,240,235,0.4); text-align: center; margin-top: 4px; line-height: 1.4; }

    .stTabs [data-baseweb="tab"] { font-size: 0.65rem !important; letter-spacing: 0.2em !important; text-transform: uppercase !important; }
    .stSelectbox label { font-size: 0.62rem !important; letter-spacing: 0.2em !important; text-transform: uppercase !important; color: rgba(245,240,235,0.45) !important; }
    [data-baseweb="select"] > div { border-radius: 0 !important; border-color: rgba(212,175,55,0.2) !important; background: rgba(212,175,55,0.02) !important; }
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
# Header
# -------------------------------------------------------
st.markdown("""
<div style="padding: 2rem 0 1rem">
    <div style="font-size:0.62rem;letter-spacing:0.3em;text-transform:uppercase;color:#D4AF37;margin-bottom:0.5rem">Your Digital Closet</div>
    <h1 class="page-title">Wardrobe</h1>
    <div style="font-size:0.72rem;font-weight:300;color:rgba(245,240,235,0.4);letter-spacing:0.05em">Upload individual clothing items — AI tags them instantly</div>
</div>
""", unsafe_allow_html=True)
st.markdown("---")

# -------------------------------------------------------
# Upload
# -------------------------------------------------------
st.markdown('<div class="section-label">Add New Item</div>', unsafe_allow_html=True)

with st.expander("📸 Tips for best tagging results"):
    st.markdown("""
    - Upload **individual items** — not full outfits
    - **Product photos** (clean background) work best
    - Supported: JPG, JPEG, PNG, WebP
    """)

uploaded_files = st.file_uploader(
    "Drop clothing items here",
    type=["jpg","jpeg","png","webp"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

CLOSET_DIR = Path("Closet")
CLOSET_DIR.mkdir(exist_ok=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.markdown("---")
        col1, col2 = st.columns([1, 1.5], gap="large")

        with col1:
            image = Image.open(uploaded_file).convert("RGB")
            st.image(image, use_container_width=True)

        with col2:
            st.markdown(f"""
            <div style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(245,240,235,0.3);margin-bottom:0.8rem">
                {uploaded_file.name}
            </div>
            """, unsafe_allow_html=True)

            safe_name = Path(uploaded_file.name).name  # drop any client-supplied directories
            temp_path = CLOSET_DIR / safe_name
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("Tagging your item..."):
                tags = tag_closet_item(str(temp_path))

            if "error" in tags:
                st.error(f"Tagging failed: {tags['error']}")
            else:
                persona = tags.get("style_persona","Millennial")
                pc = {"Gen-Z":"tag-genz","Millennial":"tag-millennial","Aesthetic":"tag-aesthetic"}.get(persona,"tag-millennial")
                pe = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"✨")

                st.markdown(f"""
                <div class="tag-row">
                    <span class="tag tag-type">{tags.get("item_type","")}</span>
                    <span class="tag tag-color">{tags.get("color","")}</span>
                    <span class="tag tag-formal">{tags.get("formality","")}</span>
                    <span class="tag tag-formal">{tags.get("indoor_outdoor","")}</span>
                    <span class="tag {pc}">{pe} {persona}</span>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("View full tag data"):
                    st.json(tags)

                # Save JSON
                json_path = CLOSET_DIR / f"{Path(safe_name).stem}.json"
                with open(json_path,"w") as f:
                    json.dump(tags, f, indent=2)

                # Save to MongoDB
                doc = {**tags, "filename": uploaded_file.name, "uploaded_at": datetime.now(timezone.utc), "source": "manual_upload"}
                if not collection.find_one({"image_id": tags.get("image_id")}):
                    collection.insert_one({k: v for k, v in doc.items() if k != "_id"})
                    st.success("✓ Saved to wardrobe database")
                else:
                    st.info("Already in database")

# -------------------------------------------------------
# Wardrobe Overview
# -------------------------------------------------------
st.markdown("---")
st.markdown('<div class="section-label">Your Wardrobe</div>', unsafe_allow_html=True)

# Stats
total      = collection.count_documents({"gender": "Women's"})
myntra     = collection.count_documents({"source": "myntra_kaggle"})
manual     = collection.count_documents({"source": {"$in": ["manual_upload","closet_bulk_upload"]}})
genz       = collection.count_documents({"style_persona": "Gen-Z"})
millennial = collection.count_documents({"style_persona": "Millennial"})
aesthetic  = collection.count_documents({"style_persona": "Aesthetic"})

st.markdown(f"""
<div class="stat-grid">
    <div class="stat-cell"><div class="stat-number">{total:,}</div><div class="stat-label">Total Items</div></div>
    <div class="stat-cell"><div class="stat-number">{myntra:,}</div><div class="stat-label">Myntra Products</div></div>
    <div class="stat-cell"><div class="stat-number">{manual:,}</div><div class="stat-label">Your Items</div></div>
</div>
<div class="stat-grid">
    <div class="stat-cell"><div class="stat-number" style="color:#ff6b9d">{genz:,}</div><div class="stat-label">⚡ Gen-Z</div></div>
    <div class="stat-cell"><div class="stat-number">{millennial:,}</div><div class="stat-label">✨ Millennial</div></div>
    <div class="stat-cell"><div class="stat-number" style="color:#9caf88">{aesthetic:,}</div><div class="stat-label">🌿 Aesthetic</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("")

tab1, tab2 = st.tabs(["Browse All", "Your Uploaded Items"])

with tab1:
    filter_persona = st.selectbox("Filter by Persona", ["All","Gen-Z","Millennial","Aesthetic"], key="fp1")
    query = {"gender": "Women's"}
    if filter_persona != "All": query["style_persona"] = filter_persona
    items = list(collection.find(query, {"_id": 0}).limit(40))

    if not items:
        st.info("No items yet. Upload some above or run the Myntra loader.")
    else:
        st.caption(f"Showing {len(items)} of {collection.count_documents(query):,} items")
        cols = st.columns(4)
        for i, item in enumerate(items):
            with cols[i % 4]:
                path    = item.get("path","")
                img_url = item.get("img_url") or item.get("image_url","")
                if path and os.path.exists(path):
                    st.image(Image.open(path).convert("RGB"), use_container_width=True)
                elif img_url and img_url.startswith("http"):
                    try: st.image(img_url, use_container_width=True)
                    except: st.markdown("🖼️")
                else:
                    st.markdown("🖼️")
                persona = item.get("style_persona","")
                pe = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
                name = item.get("name") or item.get("product_name") or item.get("item_type","")
                st.markdown(f'<div class="wardrobe-caption">{name[:22]}<br>{pe} {persona}</div>', unsafe_allow_html=True)

with tab2:
    items_yours = list(collection.find({"source": {"$in": ["manual_upload","closet_bulk_upload"]}}, {"_id": 0}).limit(40))
    if not items_yours:
        st.info("No manually uploaded items yet.")
    else:
        cols = st.columns(4)
        for i, item in enumerate(items_yours):
            with cols[i % 4]:
                path = item.get("path","")
                if path and os.path.exists(path):
                    st.image(Image.open(path).convert("RGB"), use_container_width=True)
                else:
                    st.markdown("🖼️")
                persona = item.get("style_persona","")
                pe = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
                st.markdown(f'<div class="wardrobe-caption">{item.get("item_type","").title()}<br>{item.get("color","").title()}<br>{pe} {persona}</div>', unsafe_allow_html=True)
