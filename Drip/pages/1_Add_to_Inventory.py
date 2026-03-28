# # # import streamlit as st
# # # import os
# # # import json
# # # import random
# # # from tagging import tag_closet_item

# # # # Random clothing emoji for title
# # # clothing_emojis = ["👕", "👖", "👗", "🧥", "👔", "🩳", "🧢", "👚", "👘", "🥿", "👟", "🥾"]
# # # title_emoji = random.choice(clothing_emojis)

# # # st.title(f"{title_emoji} Add Clothing to Inventory")

# # # uploaded_file = st.file_uploader("Upload Photo of Clothing", type=["jpg", "jpeg", "png"])

# # # if uploaded_file is not None:
# # #     # Save uploaded image to a temporary file
# # #     temp_path = os.path.join("temp", uploaded_file.name)
# # #     os.makedirs("temp", exist_ok=True)
# # #     with open(temp_path, "wb") as f:
# # #         f.write(uploaded_file.read())

# # #     st.image(temp_path, caption="Uploaded Clothing Image", use_container_width=True)

# # #     # Tag the image
# # #     with st.spinner("Analyzing clothing..."):
# # #         result = tag_closet_item(temp_path)

# # #     if "error" in result:
# # #         st.error(f"Tagging failed: {result['error']}")
# # #     else:
# # #         st.success("Clothing tagged successfully!")
# # #         st.subheader("🧷 Clothing Details")
# # #         st.json(result)

# # #         # Save JSON to Closet folder
# # #         closet_dir = os.path.join("Closet")
# # #         os.makedirs(closet_dir, exist_ok=True)

# # #         base_name = os.path.splitext(uploaded_file.name)[0]
# # #         out_path = os.path.join(closet_dir, f"{base_name}.json")
# # #         with open(out_path, "w") as f:
# # #             json.dump(result, f, indent=2)

# # #         st.info(f"Metadata saved to `{out_path}`")

# # # """
# # # 1_Add_to_Inventory.py — Women's Wardrobe Manager
# # # Upload and tag individual clothing items for your wardrobe inventory.
# # # Now shows style persona tag for each item.
# # # """

# # # import os
# # # import json
# # # import streamlit as st
# # # from PIL import Image
# # # from pathlib import Path
# # # from tagging import tag_closet_item

# # # st.set_page_config(
# # #     page_title="Add to Inventory",
# # #     page_icon="👗",
# # #     layout="centered"
# # # )

# # # st.markdown("""
# # # <style>
# # #     @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');
# # #     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# # #     h1, h2, h3 { font-family: 'Playfair Display', serif; }
# # #     .tag-pill {
# # #         display: inline-block;
# # #         padding: 3px 10px;
# # #         border-radius: 12px;
# # #         font-size: 0.78rem;
# # #         margin: 2px;
# # #         font-weight: 500;
# # #     }
# # #     .tag-type     { background: #f3e8ff; color: #7c3aed; border: 1px solid #d8b4fe; }
# # #     .tag-color    { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
# # #     .tag-formal   { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }
# # #     .tag-persona-genz       { background: #ffe4f0; color: #c0256f; border: 1px solid #f9a8d4; }
# # #     .tag-persona-millennial { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
# # #     .tag-persona-aesthetic  { background: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
# # #     .stButton > button {
# # #         background: #1a1a1a;
# # #         color: white;
# # #         border-radius: 8px;
# # #         width: 100%;
# # #         font-family: 'DM Sans', sans-serif;
# # #     }
# # #     .stButton > button:hover { background: #c0256f; }
# # # </style>
# # # """, unsafe_allow_html=True)

# # # # -------------------------------------------------------
# # # # Header
# # # # -------------------------------------------------------
# # # st.markdown("# 👗 Add to Wardrobe")
# # # st.caption("Upload individual clothing items — AI will automatically tag them for your outfit recommendations.")
# # # st.divider()

# # # # -------------------------------------------------------
# # # # Tips
# # # # -------------------------------------------------------
# # # with st.expander("📸 Tips for best results"):
# # #     st.markdown("""
# # #     - Upload **individual items** — not full outfits
# # #     - Use **clean product photos** when possible
# # #     - Good lighting helps CLIP classify correctly
# # #     - Supported: JPG, JPEG, PNG, WebP
# # #     """)

# # # # -------------------------------------------------------
# # # # Upload
# # # # -------------------------------------------------------
# # # st.markdown("### Upload Clothing Item")
# # # uploaded_files = st.file_uploader(
# # #     "Upload one or more clothing items",
# # #     type=["jpg", "jpeg", "png", "webp"],
# # #     accept_multiple_files=True,
# # #     help="Upload individual clothing items for auto-tagging"
# # # )

# # # CLOSET_DIR = Path("Closet")
# # # CLOSET_DIR.mkdir(exist_ok=True)

# # # if uploaded_files:
# # #     for uploaded_file in uploaded_files:
# # #         st.markdown(f"---")
# # #         st.markdown(f"**Processing: {uploaded_file.name}**")

# # #         col1, col2 = st.columns([1, 1.5])

# # #         with col1:
# # #             image = Image.open(uploaded_file).convert("RGB")
# # #             st.image(image, use_container_width=True)

# # #         with col2:
# # #             # Save temporarily for tagging
# # #             temp_path = CLOSET_DIR / uploaded_file.name
# # #             with open(temp_path, "wb") as f:
# # #                 f.write(uploaded_file.getbuffer())

# # #             with st.spinner("🤖 AI is tagging your item..."):
# # #                 tags = tag_closet_item(str(temp_path))

# # #             if "error" in tags:
# # #                 st.error(f"Tagging failed: {tags['error']}")
# # #             else:
# # #                 # Display tags as pills
# # #                 st.markdown("**Auto-detected tags:**")

# # #                 persona = tags.get("style_persona", "Millennial")
# # #                 persona_class = {
# # #                     "Gen-Z": "tag-persona-genz",
# # #                     "Millennial": "tag-persona-millennial",
# # #                     "Aesthetic": "tag-persona-aesthetic",
# # #                 }.get(persona, "tag-persona-millennial")

# # #                 persona_emoji = {
# # #                     "Gen-Z": "⚡",
# # #                     "Millennial": "✨",
# # #                     "Aesthetic": "🌿",
# # #                 }.get(persona, "✨")

# # #                 st.markdown(
# # #                     f'<span class="tag-pill tag-type">👗 {tags.get("item_type", "")}</span>'
# # #                     f'<span class="tag-pill tag-color">🎨 {tags.get("color", "")}</span>'
# # #                     f'<span class="tag-pill tag-formal">👔 {tags.get("formality", "")}</span>'
# # #                     f'<span class="tag-pill tag-formal">📍 {tags.get("indoor_outdoor", "")}</span>'
# # #                     f'<span class="tag-pill {persona_class}">{persona_emoji} {persona}</span>',
# # #                     unsafe_allow_html=True
# # #                 )

# # #                 st.markdown("")

# # #                 # Show full JSON
# # #                 with st.expander("View full tag data"):
# # #                     st.json(tags)

# # #                 # Save JSON to Closet
# # #                 json_path = CLOSET_DIR / f"{Path(uploaded_file.name).stem}.json"
# # #                 with open(json_path, "w") as f:
# # #                     json.dump(tags, f, indent=2)

# # #                 st.success(f"✅ Saved to wardrobe as `{json_path.name}`")

# # # # -------------------------------------------------------
# # # # Wardrobe Overview
# # # # -------------------------------------------------------
# # # st.divider()
# # # st.markdown("### Your Wardrobe")

# # # json_files = list(CLOSET_DIR.glob("*.json"))

# # # if not json_files:
# # #     st.info("Your wardrobe is empty — upload some items above to get started!")
# # # else:
# # #     # Stats
# # #     items = []
# # #     for f in json_files:
# # #         try:
# # #             with open(f) as file:
# # #                 items.append(json.load(file))
# # #         except Exception:
# # #             continue

# # #     col1, col2, col3, col4 = st.columns(4)
# # #     col1.metric("Total Items", len(items))

# # #     from collections import Counter
# # #     personas = Counter(i.get("style_persona", "Unknown") for i in items)
# # #     col2.metric("Gen-Z Items", personas.get("Gen-Z", 0))
# # #     col3.metric("Millennial Items", personas.get("Millennial", 0))
# # #     col4.metric("Aesthetic Items", personas.get("Aesthetic", 0))

# # #     st.markdown("")

# # #     # Display grid
# # #     cols = st.columns(4)
# # #     for i, item in enumerate(items):
# # #         col = cols[i % 4]
# # #         with col:
# # #             img_path = item.get("path", "")
# # #             if img_path and os.path.exists(img_path):
# # #                 img = Image.open(img_path).convert("RGB")
# # #                 st.image(img, use_container_width=True)

# # #             persona = item.get("style_persona", "")
# # #             persona_emoji = {"Gen-Z": "⚡", "Millennial": "✨", "Aesthetic": "🌿"}.get(persona, "")
# # #             st.caption(
# # #                 f"{item.get('item_type', '').title()} · "
# # #                 f"{item.get('color', '').title()}\n"
# # #                 f"{persona_emoji} {persona}"
# # #             )

# # """
# # 1_Add_to_Inventory.py — Women's Wardrobe Manager
# # Upload items → CLIP tags them → saves to Closet/ AND MongoDB.
# # Wardrobe overview reads from MongoDB.
# # """

# # import os
# # import json
# # import streamlit as st
# # from PIL import Image
# # from pathlib import Path
# # from pymongo import MongoClient
# # from pymongo.server_api import ServerApi
# # from datetime import datetime, timezone

# # # -------------------------------------------------------
# # # Import tagging from fitcheck folder
# # # -------------------------------------------------------
# # import sys
# # sys.path.insert(0, str(Path(__file__).parent.parent))
# # from tagging import tag_closet_item

# # st.set_page_config(page_title="Add to Inventory", page_icon="👗", layout="centered")

# # st.markdown("""
# # <style>
# #     @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');
# #     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
# #     h1, h2, h3 { font-family: 'Playfair Display', serif; }
# #     .tag-pill { display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 0.78rem; margin: 2px; font-weight: 500; }
# #     .tag-type { background: #f3e8ff; color: #7c3aed; border: 1px solid #d8b4fe; }
# #     .tag-color { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }
# #     .tag-formal { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; }
# #     .tag-persona-genz { background: #ffe4f0; color: #c0256f; border: 1px solid #f9a8d4; }
# #     .tag-persona-millennial { background: #fef3c7; color: #92400e; border: 1px solid #fcd34d; }
# #     .tag-persona-aesthetic { background: #d1fae5; color: #065f46; border: 1px solid #6ee7b7; }
# #     .stButton > button { background: #1a1a1a; color: white; border-radius: 8px; width: 100%; font-family: 'DM Sans', sans-serif; }
# #     .stButton > button:hover { background: #c0256f; }
# # </style>
# # """, unsafe_allow_html=True)

# # # -------------------------------------------------------
# # # MongoDB
# # # -------------------------------------------------------
# # MONGO_URI = "mongodb+srv://fitcheck:fitcheck123@cluster0.ozebcow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # @st.cache_resource
# # def get_db():
# #     client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
# #     return client["fitcheck_women"]["wardrobe_inventory"]

# # collection = get_db()

# # # -------------------------------------------------------
# # # Header
# # # -------------------------------------------------------
# # st.markdown("# 👗 Add to Wardrobe")
# # st.caption("Upload clothing items — AI tags them and saves to your wardrobe database.")
# # st.divider()

# # with st.expander("📸 Tips for best results"):
# #     st.markdown("""
# #     - Upload **individual items** — not full outfits
# #     - Use **clean product photos** when possible
# #     - Good lighting helps CLIP classify correctly
# #     - Supported: JPG, JPEG, PNG, WebP
# #     """)

# # # -------------------------------------------------------
# # # Upload section
# # # -------------------------------------------------------
# # st.markdown("### Upload Clothing Item")
# # uploaded_files = st.file_uploader(
# #     "Upload one or more clothing items",
# #     type=["jpg","jpeg","png","webp"],
# #     accept_multiple_files=True,
# # )

# # CLOSET_DIR = Path("Closet")
# # CLOSET_DIR.mkdir(exist_ok=True)

# # if uploaded_files:
# #     for uploaded_file in uploaded_files:
# #         st.markdown("---")
# #         st.markdown(f"**Processing: {uploaded_file.name}**")
# #         col1, col2 = st.columns([1, 1.5])

# #         with col1:
# #             image = Image.open(uploaded_file).convert("RGB")
# #             st.image(image, use_container_width=True)

# #         with col2:
# #             # Save to Closet/
# #             temp_path = CLOSET_DIR / uploaded_file.name
# #             with open(temp_path, "wb") as f:
# #                 f.write(uploaded_file.getbuffer())

# #             with st.spinner("🤖 AI tagging your item..."):
# #                 tags = tag_closet_item(str(temp_path))

# #             if "error" in tags:
# #                 st.error(f"Tagging failed: {tags['error']}")
# #             else:
# #                 persona = tags.get("style_persona", "Millennial")
# #                 pc = {"Gen-Z":"tag-persona-genz","Millennial":"tag-persona-millennial","Aesthetic":"tag-persona-aesthetic"}.get(persona,"tag-persona-millennial")
# #                 pe = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"✨")

# #                 st.markdown("**Auto-detected tags:**")
# #                 st.markdown(
# #                     f'<span class="tag-pill tag-type">👗 {tags.get("item_type","")}</span>'
# #                     f'<span class="tag-pill tag-color">🎨 {tags.get("color","")}</span>'
# #                     f'<span class="tag-pill tag-formal">👔 {tags.get("formality","")}</span>'
# #                     f'<span class="tag-pill tag-formal">📍 {tags.get("indoor_outdoor","")}</span>'
# #                     f'<span class="tag-pill {pc}">{pe} {persona}</span>',
# #                     unsafe_allow_html=True
# #                 )

# #                 with st.expander("View full tag data"):
# #                     st.json(tags)

# #                 # Save JSON to Closet/
# #                 json_path = CLOSET_DIR / f"{Path(uploaded_file.name).stem}.json"
# #                 with open(json_path, "w") as f:
# #                     json.dump(tags, f, indent=2)

# #                 # Save to MongoDB
# #                 tags["filename"]   = uploaded_file.name
# #                 tags["uploaded_at"] = datetime.now(timezone.utc)
# #                 tags["source"]     = "manual_upload"

# #                 existing = collection.find_one({"image_id": tags.get("image_id")})
# #                 if not existing:
# #                     collection.insert_one({k: v for k, v in tags.items() if k != "_id"})
# #                     st.success(f"✅ Saved to wardrobe + MongoDB!")
# #                 else:
# #                     st.info("ℹ️ Item already in database")

# # # -------------------------------------------------------
# # # Wardrobe overview — reads from MongoDB
# # # -------------------------------------------------------
# # st.divider()
# # st.markdown("### Your Wardrobe")

# # tab1, tab2 = st.tabs(["📊 Stats", "👗 Browse Items"])

# # with tab1:
# #     total    = collection.count_documents({"gender": "Women's"})
# #     myntra   = collection.count_documents({"source": "myntra_kaggle"})
# #     manual   = collection.count_documents({"source": {"$in": ["manual_upload","closet_bulk_upload"]}})
# #     genz     = collection.count_documents({"style_persona": "Gen-Z"})
# #     millennial = collection.count_documents({"style_persona": "Millennial"})
# #     aesthetic  = collection.count_documents({"style_persona": "Aesthetic"})

# #     col1, col2, col3 = st.columns(3)
# #     col1.metric("Total Items", total)
# #     col2.metric("Myntra Products", myntra)
# #     col3.metric("Your Items", manual)

# #     st.markdown("")
# #     col4, col5, col6 = st.columns(3)
# #     col4.metric("⚡ Gen-Z", genz)
# #     col5.metric("✨ Millennial", millennial)
# #     col6.metric("🌿 Aesthetic", aesthetic)

# # with tab2:
# #     # Filter options
# #     filter_persona = st.selectbox("Filter by Persona", ["All","Gen-Z","Millennial","Aesthetic"])
# #     filter_source  = st.selectbox("Filter by Source", ["All","Your Items","Myntra Products"])

# #     # Build query
# #     query = {"gender": "Women's"}
# #     if filter_persona != "All":
# #         query["style_persona"] = filter_persona
# #     if filter_source == "Your Items":
# #         query["source"] = {"$in": ["manual_upload","closet_bulk_upload"]}
# #     elif filter_source == "Myntra Products":
# #         query["source"] = "myntra_kaggle"

# #     items = list(collection.find(query, {"_id": 0}).limit(40))

# #     if not items:
# #         st.info("No items found. Upload some items or run the Myntra loader script.")
# #     else:
# #         st.caption(f"Showing {len(items)} items")
# #         cols = st.columns(4)
# #         for i, item in enumerate(items):
# #             with cols[i % 4]:
# #                 # Image
# #                 path    = item.get("path","")
# #                 img_url = item.get("image_url","")
# #                 if path and os.path.exists(path):
# #                     st.image(Image.open(path).convert("RGB"), use_container_width=True)
# #                 elif img_url and img_url.startswith("http"):
# #                     st.image(img_url, use_container_width=True)
# #                 else:
# #                     st.markdown("🖼️")

# #                 persona = item.get("style_persona","")
# #                 pe      = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
# #                 name    = item.get("product_name") or item.get("item_type","")
# #                 st.caption(f"{name[:20]}\n{pe} {persona}")

# """
# 1_Add_to_Inventory.py — Women's Wardrobe Manager
# Editorial luxury fashion UI.
# Upload → CLIP tags → saves to Closet/ + MongoDB.
# """

# import os
# import json
# import streamlit as st
# from PIL import Image
# from pathlib import Path
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# from datetime import datetime, timezone
# import sys

# sys.path.insert(0, str(Path(__file__).parent.parent))
# from tagging import tag_closet_item

# st.set_page_config(page_title="Wardrobe", page_icon="👗", layout="centered")

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');

#     html, body, [class*="css"] { font-family: 'Jost', sans-serif; font-weight: 300; letter-spacing: 0.02em; }
#     #MainMenu, footer, header { visibility: hidden; }
#     .block-container { padding-top: 2rem; max-width: 860px; }

#     .page-title { font-family: 'Cormorant Garamond', serif; font-size: 2.8rem; font-weight: 300; font-style: italic; color: #f5f0eb; }
#     .section-label {
#         font-size: 0.62rem; font-weight: 400; letter-spacing: 0.3em; text-transform: uppercase;
#         color: #D4AF37; margin: 1.5rem 0 0.8rem; display: flex; align-items: center; gap: 12px;
#     }
#     .section-label::after { content: ''; flex: 1; height: 1px; background: rgba(212,175,55,0.2); }

#     [data-testid="stFileUploader"] {
#         border: 1px solid rgba(212,175,55,0.2) !important;
#         border-radius: 0 !important; background: rgba(212,175,55,0.02) !important;
#     }

#     /* Tag pills */
#     .tag-row { display: flex; flex-wrap: wrap; gap: 6px; margin: 0.8rem 0; }
#     .tag { padding: 4px 12px; font-size: 0.62rem; letter-spacing: 0.15em; text-transform: uppercase; border: 1px solid; }
#     .tag-type { border-color: rgba(167,139,250,0.4); color: rgba(167,139,250,0.8); }
#     .tag-color { border-color: rgba(212,175,55,0.4); color: rgba(212,175,55,0.8); }
#     .tag-formal { border-color: rgba(156,175,136,0.4); color: rgba(156,175,136,0.8); }
#     .tag-genz { border-color: rgba(255,107,157,0.4); color: rgba(255,107,157,0.8); }
#     .tag-millennial { border-color: rgba(212,175,55,0.4); color: rgba(212,175,55,0.8); }
#     .tag-aesthetic { border-color: rgba(156,175,136,0.4); color: rgba(156,175,136,0.8); }

#     .stButton > button {
#         background: transparent !important; color: #D4AF37 !important;
#         border: 1px solid #D4AF37 !important; border-radius: 0 !important;
#         padding: 0.75rem !important; font-family: 'Jost', sans-serif !important;
#         font-size: 0.68rem !important; letter-spacing: 0.3em !important;
#         text-transform: uppercase !important; width: 100% !important; transition: all 0.3s !important;
#     }
#     .stButton > button:hover { background: #D4AF37 !important; color: #0d0d0d !important; }

#     /* Stats grid */
#     .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: rgba(212,175,55,0.12); margin: 1rem 0; }
#     .stat-cell { background: #0d0d0d; padding: 1.2rem 1rem; text-align: center; }
#     .stat-number { font-family: 'Cormorant Garamond', serif; font-size: 2.2rem; font-weight: 300; color: #D4AF37; line-height: 1; }
#     .stat-label { font-size: 0.6rem; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(245,240,235,0.3); margin-top: 4px; }

#     /* Wardrobe grid item */
#     .wardrobe-item { background: rgba(212,175,55,0.02); border: 1px solid rgba(212,175,55,0.08); padding: 6px; margin-bottom: 6px; }
#     .wardrobe-caption { font-size: 0.62rem; letter-spacing: 0.05em; color: rgba(245,240,235,0.4); text-align: center; margin-top: 4px; line-height: 1.4; }

#     .stTabs [data-baseweb="tab"] { font-size: 0.65rem !important; letter-spacing: 0.2em !important; text-transform: uppercase !important; }
#     .stSelectbox label { font-size: 0.62rem !important; letter-spacing: 0.2em !important; text-transform: uppercase !important; color: rgba(245,240,235,0.45) !important; }
#     [data-baseweb="select"] > div { border-radius: 0 !important; border-color: rgba(212,175,55,0.2) !important; background: rgba(212,175,55,0.02) !important; }
#     hr { border-color: rgba(212,175,55,0.12) !important; }
# </style>
# """, unsafe_allow_html=True)

# # -------------------------------------------------------
# # MongoDB
# # -------------------------------------------------------
# MONGO_URI = "mongodb+srv://fitcheck:fitcheck123@cluster0.ozebcow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# @st.cache_resource
# def get_db():
#     c = MongoClient(MONGO_URI, server_api=ServerApi('1'))
#     return c["fitcheck_women"]["wardrobe_inventory"]

# collection = get_db()

# # -------------------------------------------------------
# # Header
# # -------------------------------------------------------
# st.markdown("""
# <div style="padding: 2rem 0 1rem">
#     <div style="font-size:0.62rem;letter-spacing:0.3em;text-transform:uppercase;color:#D4AF37;margin-bottom:0.5rem">Your Digital Closet</div>
#     <h1 class="page-title">Wardrobe</h1>
#     <div style="font-size:0.72rem;font-weight:300;color:rgba(245,240,235,0.4);letter-spacing:0.05em">Upload individual clothing items — AI tags them instantly</div>
# </div>
# """, unsafe_allow_html=True)
# st.markdown("---")

# # -------------------------------------------------------
# # Upload
# # -------------------------------------------------------
# st.markdown('<div class="section-label">Add New Item</div>', unsafe_allow_html=True)

# with st.expander("📸 Tips for best tagging results"):
#     st.markdown("""
#     - Upload **individual items** — not full outfits
#     - **Product photos** (clean background) work best
#     - Supported: JPG, JPEG, PNG, WebP
#     """)

# uploaded_files = st.file_uploader(
#     "Drop clothing items here",
#     type=["jpg","jpeg","png","webp"],
#     accept_multiple_files=True,
#     label_visibility="collapsed"
# )

# CLOSET_DIR = Path("Closet")
# CLOSET_DIR.mkdir(exist_ok=True)

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         st.markdown("---")
#         col1, col2 = st.columns([1, 1.5], gap="large")

#         with col1:
#             image = Image.open(uploaded_file).convert("RGB")
#             st.image(image, use_container_width=True)

#         with col2:
#             st.markdown(f"""
#             <div style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(245,240,235,0.3);margin-bottom:0.8rem">
#                 {uploaded_file.name}
#             </div>
#             """, unsafe_allow_html=True)

#             temp_path = CLOSET_DIR / uploaded_file.name
#             with open(temp_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())

#             with st.spinner("Tagging your item..."):
#                 tags = tag_closet_item(str(temp_path))

#             if "error" in tags:
#                 st.error(f"Tagging failed: {tags['error']}")
#             else:
#                 persona = tags.get("style_persona","Millennial")
#                 pc = {"Gen-Z":"tag-genz","Millennial":"tag-millennial","Aesthetic":"tag-aesthetic"}.get(persona,"tag-millennial")
#                 pe = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"✨")

#                 st.markdown(f"""
#                 <div class="tag-row">
#                     <span class="tag tag-type">{tags.get("item_type","")}</span>
#                     <span class="tag tag-color">{tags.get("color","")}</span>
#                     <span class="tag tag-formal">{tags.get("formality","")}</span>
#                     <span class="tag tag-formal">{tags.get("indoor_outdoor","")}</span>
#                     <span class="tag {pc}">{pe} {persona}</span>
#                 </div>
#                 """, unsafe_allow_html=True)

#                 with st.expander("View full tag data"):
#                     st.json(tags)

#                 # Save JSON
#                 json_path = CLOSET_DIR / f"{Path(uploaded_file.name).stem}.json"
#                 with open(json_path,"w") as f:
#                     json.dump(tags, f, indent=2)

#                 # Save to MongoDB
#                 doc = {**tags, "filename": uploaded_file.name, "uploaded_at": datetime.now(timezone.utc), "source": "manual_upload"}
#                 if not collection.find_one({"image_id": tags.get("image_id")}):
#                     collection.insert_one({k: v for k, v in doc.items() if k != "_id"})
#                     st.success("✓ Saved to wardrobe database")
#                 else:
#                     st.info("Already in database")

# # -------------------------------------------------------
# # Wardrobe Overview
# # -------------------------------------------------------
# st.markdown("---")
# st.markdown('<div class="section-label">Your Wardrobe</div>', unsafe_allow_html=True)

# # Stats
# total      = collection.count_documents({"gender": "Women's"})
# myntra     = collection.count_documents({"source": "myntra_kaggle"})
# manual     = collection.count_documents({"source": {"$in": ["manual_upload","closet_bulk_upload"]}})
# genz       = collection.count_documents({"style_persona": "Gen-Z"})
# millennial = collection.count_documents({"style_persona": "Millennial"})
# aesthetic  = collection.count_documents({"style_persona": "Aesthetic"})

# st.markdown(f"""
# <div class="stat-grid">
#     <div class="stat-cell"><div class="stat-number">{total:,}</div><div class="stat-label">Total Items</div></div>
#     <div class="stat-cell"><div class="stat-number">{myntra:,}</div><div class="stat-label">Myntra Products</div></div>
#     <div class="stat-cell"><div class="stat-number">{manual:,}</div><div class="stat-label">Your Items</div></div>
# </div>
# <div class="stat-grid">
#     <div class="stat-cell"><div class="stat-number" style="color:#ff6b9d">{genz:,}</div><div class="stat-label">⚡ Gen-Z</div></div>
#     <div class="stat-cell"><div class="stat-number">{millennial:,}</div><div class="stat-label">✨ Millennial</div></div>
#     <div class="stat-cell"><div class="stat-number" style="color:#9caf88">{aesthetic:,}</div><div class="stat-label">🌿 Aesthetic</div></div>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("")

# tab1, tab2 = st.tabs(["Browse All", "Your Uploaded Items"])

# with tab1:
#     filter_persona = st.selectbox("Filter by Persona", ["All","Gen-Z","Millennial","Aesthetic"], key="fp1")
#     query = {"gender": "Women's"}
#     if filter_persona != "All": query["style_persona"] = filter_persona
#     items = list(collection.find(query, {"_id": 0}).limit(40))

#     if not items:
#         st.info("No items yet. Upload some above or run the Myntra loader.")
#     else:
#         st.caption(f"Showing {len(items)} of {collection.count_documents(query):,} items")
#         cols = st.columns(4)
#         for i, item in enumerate(items):
#             with cols[i % 4]:
#                 path    = item.get("path","")
#                 img_url = item.get("img_url") or item.get("image_url","")
#                 if path and os.path.exists(path):
#                     st.image(Image.open(path).convert("RGB"), use_container_width=True)
#                 elif img_url and img_url.startswith("http"):
#                     try: st.image(img_url, use_container_width=True)
#                     except: st.markdown("🖼️")
#                 else:
#                     st.markdown("🖼️")
#                 persona = item.get("style_persona","")
#                 pe = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
#                 name = item.get("name") or item.get("product_name") or item.get("item_type","")
#                 st.markdown(f'<div class="wardrobe-caption">{name[:22]}<br>{pe} {persona}</div>', unsafe_allow_html=True)

# with tab2:
#     items_yours = list(collection.find({"source": {"$in": ["manual_upload","closet_bulk_upload"]}}, {"_id": 0}).limit(40))
#     if not items_yours:
#         st.info("No manually uploaded items yet.")
#     else:
#         cols = st.columns(4)
#         for i, item in enumerate(items_yours):
#             with cols[i % 4]:
#                 path = item.get("path","")
#                 if path and os.path.exists(path):
#                     st.image(Image.open(path).convert("RGB"), use_container_width=True)
#                 else:
#                     st.markdown("🖼️")
#                 persona = item.get("style_persona","")
#                 pe = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
#                 st.markdown(f'<div class="wardrobe-caption">{item.get("item_type","").title()}<br>{item.get("color","").title()}<br>{pe} {persona}</div>', unsafe_allow_html=True)


"""
1_Add_to_Inventory.py — Women's Wardrobe Manager
Editorial luxury fashion UI.
Upload → CLIP tags → saves to Closet/ + MongoDB.
"""

import os
import json
import streamlit as st
from PIL import Image
from pathlib import Path
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime, timezone
import sys
import certifi
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent.parent))
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
MONGO_URI = os.environ.get("MONGO_URI")

@st.cache_resource
def get_db():
    c = MongoClient(
        MONGO_URI,
        server_api=ServerApi('1'),
        tls=True,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )
    return c["fitcheck_women"]["wardrobe_inventory"]

collection = get_db()

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

            temp_path = CLOSET_DIR / uploaded_file.name
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
                json_path = CLOSET_DIR / f"{Path(uploaded_file.name).stem}.json"
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
