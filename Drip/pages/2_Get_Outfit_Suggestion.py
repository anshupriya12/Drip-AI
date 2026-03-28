# """
# 2_Get_Outfit_Suggestion.py — Women's Outfit Recommender
# Rule-based outfit generator from women's closet inventory.
# Now includes Style Persona filter (Gen-Z / Millennial / Aesthetic).
# """

# import os
# import json
# import streamlit as st
# from pathlib import Path
# from PIL import Image

# st.set_page_config(
#     page_title="Outfit Recommender",
#     page_icon="✨",
#     layout="centered"
# )

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');
#     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#     h1, h2, h3 { font-family: 'Playfair Display', serif; }
#     .stButton > button {
#         background: #1a1a1a;
#         color: white;
#         border-radius: 8px;
#         width: 100%;
#         font-family: 'DM Sans', sans-serif;
#     }
#     .stButton > button:hover { background: #c0256f; }
#     .item-label {
#         font-size: 0.8rem;
#         color: #888;
#         text-align: center;
#         margin-top: 4px;
#     }
# </style>
# """, unsafe_allow_html=True)

# # -------------------------------------------------------
# # Header
# # -------------------------------------------------------
# st.markdown("# ✨ Outfit Recommender")
# st.caption("Get a complete women's outfit from your wardrobe inventory.")
# st.divider()

# # -------------------------------------------------------
# # Color Compatibility Rules
# # -------------------------------------------------------
# COLOR_COMPATIBILITY = {
#     "black":    ["white", "beige", "cream", "nude", "red", "pink", "gold", "silver", "grey", "blush"],
#     "white":    ["black", "navy", "blue", "red", "pink", "beige", "grey", "gold", "coral"],
#     "beige":    ["black", "white", "brown", "camel", "navy", "olive", "burgundy"],
#     "navy":     ["white", "beige", "cream", "gold", "red", "pink", "grey"],
#     "grey":     ["black", "white", "pink", "blush", "navy", "burgundy", "yellow"],
#     "pink":     ["black", "white", "grey", "nude", "gold", "blush", "navy"],
#     "red":      ["black", "white", "navy", "gold", "beige"],
#     "blue":     ["white", "beige", "navy", "gold", "grey", "brown"],
#     "green":    ["white", "beige", "brown", "camel", "gold", "black"],
#     "brown":    ["beige", "cream", "white", "olive", "camel", "gold"],
#     "camel":    ["black", "white", "beige", "brown", "navy", "olive"],
#     "burgundy": ["beige", "grey", "black", "gold", "cream", "blush"],
#     "olive":    ["white", "beige", "brown", "camel", "black"],
#     "yellow":   ["black", "white", "grey", "navy", "blue"],
#     "purple":   ["black", "white", "grey", "gold", "blush"],
#     "lavender": ["white", "grey", "blush", "gold", "navy"],
#     "coral":    ["white", "beige", "gold", "navy", "cream"],
#     "mustard":  ["black", "white", "brown", "olive", "navy"],
#     "gold":     ["black", "white", "navy", "burgundy", "brown"],
#     "silver":   ["black", "white", "grey", "navy", "blush"],
#     "nude":     ["black", "white", "beige", "camel", "gold"],
#     "blush":    ["black", "white", "grey", "gold", "navy"],
#     "cream":    ["black", "brown", "navy", "camel", "burgundy"],
# }

# def colors_compatible(c1: str, c2: str) -> bool:
#     """Check if two colors work together."""
#     c1, c2 = c1.lower(), c2.lower()
#     if c1 == c2:
#         return True
#     compatible = COLOR_COMPATIBILITY.get(c1, [])
#     return c2 in compatible

# # -------------------------------------------------------
# # Style Persona Rules
# # -------------------------------------------------------
# PERSONA_ITEM_PREFERENCES = {
#     "Gen-Z": [
#         "crop top", "cargo pants", "wide leg pants", "mini skirt",
#         "hoodie", "sneakers", "platform shoes", "ankle boots",
#         "corset top", "co-ord set", "crossbody bag", "backpack"
#     ],
#     "Millennial": [
#         "blouse", "shirt", "trousers", "midi skirt", "dress",
#         "blazer", "coat", "loafers", "flats", "heels",
#         "handbag", "tote bag", "cardigan", "sweater"
#     ],
#     "Aesthetic": [
#         "dress", "maxi dress", "mini dress", "skirt", "midi skirt",
#         "blouse", "cardigan", "flats", "sandals", "mules",
#         "handbag", "clutch", "scarf", "hair accessory"
#     ],
#     "All": []  # No preference filtering
# }

# def matches_persona(item_type: str, persona: str) -> bool:
#     """Check if item type matches the selected persona."""
#     if persona == "All":
#         return True
#     preferences = PERSONA_ITEM_PREFERENCES.get(persona, [])
#     if not preferences:
#         return True
#     item_lower = item_type.lower()
#     return any(pref in item_lower for pref in preferences)

# # -------------------------------------------------------
# # Load Closet
# # -------------------------------------------------------
# def load_closet(closet_dir: str = "Closet") -> list[dict]:
#     """Load all JSON-tagged items from Closet folder."""
#     items = []
#     closet_path = Path(closet_dir)
#     if not closet_path.exists():
#         return items

#     for json_file in closet_path.glob("*.json"):
#         try:
#             with open(json_file) as f:
#                 item = json.load(f)
#             if "error" not in item:
#                 items.append(item)
#         except Exception:
#             continue
#     return items

# # -------------------------------------------------------
# # Outfit Categories
# # -------------------------------------------------------
# OUTFIT_CATEGORIES = {
#     "tops": ["crop top", "blouse", "tank top", "shirt", "t-shirt",
#              "sweater", "cardigan", "hoodie", "corset top"],
#     "bottoms": ["jeans", "leggings", "skirt", "mini skirt", "midi skirt",
#                 "shorts", "trousers", "wide leg pants", "cargo pants"],
#     "dresses": ["dress", "mini dress", "maxi dress", "jumpsuit", "co-ord set"],
#     "outerwear": ["jacket", "blazer", "coat", "denim jacket", "leather jacket"],
#     "shoes": ["heels", "sneakers", "sandals", "boots", "ankle boots",
#               "flats", "loafers", "platform shoes", "mules"],
#     "bags": ["handbag", "tote bag", "clutch", "crossbody bag", "backpack"],
#     "accessories": ["earrings", "necklace", "bracelet", "sunglasses",
#                     "hair accessory", "belt", "scarf"],
# }

# def get_category(item_type: str) -> str:
#     """Map item type to outfit category."""
#     item_lower = item_type.lower()
#     for cat, items in OUTFIT_CATEGORIES.items():
#         if any(i in item_lower for i in items):
#             return cat
#     return "other"

# # -------------------------------------------------------
# # Outfit Builder
# # -------------------------------------------------------
# def build_outfit(
#     items: list[dict],
#     location: str,
#     formality: str,
#     preferred_color: str,
#     persona: str,
# ) -> dict:
#     """
#     Build a complete outfit from closet items based on preferences.
#     Returns dict of category → item.
#     """
#     outfit = {}

#     # Priority order for building outfit
#     priority = ["dresses", "tops", "bottoms", "outerwear", "shoes", "bags", "accessories"]

#     for category in priority:
#         candidates = []
#         for item in items:
#             item_cat = get_category(item.get("item_type", ""))
#             if item_cat != category:
#                 continue

#             # Filter by location
#             item_location = item.get("indoor_outdoor", "").lower()
#             if location.lower() == "outdoor" and item_location == "indoor":
#                 continue

#             # Filter by formality
#             item_formality = item.get("formality", "").lower()
#             if formality.lower() == "formal" and item_formality == "casual":
#                 continue
#             if formality.lower() == "casual" and item_formality == "formal":
#                 continue

#             # Filter by persona
#             item_persona = item.get("style_persona", "")
#             if persona != "All" and item_persona and item_persona != persona:
#                 continue

#             # Filter by persona item preferences
#             if not matches_persona(item.get("item_type", ""), persona):
#                 continue

#             candidates.append(item)

#         print(f"{category}: Found {len(candidates)} candidates after filtering")

#         if not candidates:
#             print(f"❌ No candidates for '{category}' — skipping")
#             continue

#         # Score by color compatibility
#         if preferred_color and preferred_color.lower() != "any":
#             scored = []
#             for item in candidates:
#                 item_color = item.get("color", "").lower()
#                 score = 2 if item_color == preferred_color.lower() else (
#                     1 if colors_compatible(preferred_color.lower(), item_color) else 0
#                 )
#                 scored.append((score, item))
#             scored.sort(key=lambda x: -x[0])
#             best = scored[0][1]
#         else:
#             best = candidates[0]

#         # Skip if dress already chosen (no separate top/bottom needed)
#         if category in ["tops", "bottoms"] and "dresses" in outfit:
#             continue

#         outfit[category] = best

#     return outfit

# # -------------------------------------------------------
# # Preferences UI
# # -------------------------------------------------------
# st.markdown("### Your Preferences")

# col1, col2 = st.columns(2)
# with col1:
#     location = st.selectbox("Location", ["Outdoor", "Indoor"])
#     persona = st.selectbox(
#         "Style Persona",
#         ["All", "Gen-Z", "Millennial", "Aesthetic"],
#         help="Filter outfit pieces by style aesthetic"
#     )
# with col2:
#     formality = st.selectbox("Occasion", ["Casual", "Smart Casual", "Formal", "Party", "Streetwear", "Athleisure"])
#     preferred_color = st.selectbox(
#         "Preferred Color",
#         ["Any", "black", "white", "beige", "navy", "pink", "red",
#          "blue", "green", "brown", "camel", "burgundy", "grey",
#          "yellow", "purple", "coral", "gold", "nude", "blush", "cream"]
#     )

# # Persona description
# persona_desc = {
#     "Gen-Z": "⚡ Y2K, streetwear, bold looks, cargo, chunky shoes",
#     "Millennial": "✨ Minimalist, tailored, smart casual, classic pieces",
#     "Aesthetic": "🌿 Cottagecore, dark academia, lace, floral, vintage",
#     "All": "🎯 No style filter — show all available items",
# }
# st.caption(persona_desc.get(persona, ""))

# st.divider()

# # -------------------------------------------------------
# # Generate Outfit
# # -------------------------------------------------------
# if st.button("✨ Recommend Outfit"):
#     items = load_closet()

#     if not items:
#         st.warning("👗 Your closet is empty! Go to **Add to Inventory** to add clothes first.")
#     else:
#         color_input = preferred_color if preferred_color != "Any" else ""
#         outfit = build_outfit(items, location, formality, color_input, persona)

#         if not outfit:
#             st.error("😔 No matching items found. Try changing your filters or add more items to your closet.")
#         else:
#             st.markdown(f"## Recommended Outfit")
#             if persona != "All":
#                 persona_emoji = {"Gen-Z": "⚡", "Millennial": "✨", "Aesthetic": "🌿"}.get(persona, "")
#                 st.caption(f"{persona_emoji} {persona} aesthetic — {formality} · {location}")

#             # Display outfit grid
#             cols = st.columns(min(len(outfit), 4))
#             for i, (category, item) in enumerate(outfit.items()):
#                 col = cols[i % len(cols)]
#                 with col:
#                     img_path = item.get("path", "")
#                     if img_path and os.path.exists(img_path):
#                         img = Image.open(img_path).convert("RGB")
#                         st.image(img, use_container_width=True)
#                     else:
#                         st.markdown(f"🖼️ _{item.get('item_type', category)}_")

#                     st.markdown(
#                         f'<p class="item-label">'
#                         f'{item.get("item_type", category).title()}<br>'
#                         f'<span style="color:#c0256f">{item.get("color", "").title()}</span>'
#                         f'</p>',
#                         unsafe_allow_html=True
#                     )

#             # Outfit summary
#             st.divider()
#             st.markdown("**Outfit Summary**")
#             summary_cols = st.columns(2)
#             for i, (category, item) in enumerate(outfit.items()):
#                 col = summary_cols[i % 2]
#                 with col:
#                     item_persona = item.get("style_persona", "")
#                     persona_tag = f" · {item_persona}" if item_persona else ""
#                     st.markdown(
#                         f"**{category.title()}:** "
#                         f"{item.get('item_type', '').title()} — "
#                         f"{item.get('color', '').title()}"
#                         f"*{persona_tag}*"
#                     )
# """
# 2_Get_Outfit_Suggestion.py — Women's Outfit Recommender
# Reads from MongoDB — supports local closet + Myntra catalog with Buy Now links.
# """

# import os
# import streamlit as st
# from pathlib import Path
# from PIL import Image
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi

# st.set_page_config(page_title="Outfit Recommender", page_icon="✨", layout="centered")

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');
#     html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
#     h1, h2, h3 { font-family: 'Playfair Display', serif; }
#     .stButton > button { background: #1a1a1a; color: white; border-radius: 8px; width: 100%; font-family: 'DM Sans', sans-serif; }
#     .stButton > button:hover { background: #c0256f; }
#     .buy-btn { display: inline-block; padding: 4px 10px; background: #ff3f6c; color: white !important; border-radius: 6px; font-size: 0.73rem; text-decoration: none; margin: 2px; font-weight: 500; }
#     .buy-btn:hover { background: #c0256f; }
#     .buy-btn-amazon { background: #ff9900 !important; }
#     .buy-btn-ajio { background: #7b2d8b !important; }
#     .product-card { background: #fafafa; border: 1px solid #f0f0f0; border-radius: 12px; padding: 10px; margin-bottom: 6px; text-align: center; }
#     .product-name { font-size: 0.8rem; font-weight: 500; color: #1a1a1a; margin: 4px 0 2px; }
#     .product-brand { font-size: 0.73rem; color: #888; }
#     .product-price { font-size: 0.83rem; font-weight: 600; color: #c0256f; margin: 3px 0; }
#     .persona-tag { display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; margin: 3px 0; }
#     .tag-genz { background: #ffe4f0; color: #c0256f; }
#     .tag-millennial { background: #fef3c7; color: #92400e; }
#     .tag-aesthetic { background: #d1fae5; color: #065f46; }
# </style>
# """, unsafe_allow_html=True)

# # -------------------------------------------------------
# # MongoDB
# # -------------------------------------------------------
# MONGO_URI = "mongodb+srv://fitcheck:fitcheck123@cluster0.ozebcow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# @st.cache_resource
# def get_db():
#     client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
#     return client["fitcheck_women"]["wardrobe_inventory"]

# collection = get_db()

# # -------------------------------------------------------
# # Color compatibility
# # -------------------------------------------------------
# COLOR_COMPAT = {
#     "black": ["white","beige","cream","nude","red","pink","gold","silver","grey","blush"],
#     "white": ["black","navy","blue","red","pink","beige","grey","gold","coral"],
#     "beige": ["black","white","brown","camel","navy","olive","burgundy"],
#     "navy":  ["white","beige","cream","gold","red","pink","grey"],
#     "grey":  ["black","white","pink","blush","navy","burgundy","yellow"],
#     "pink":  ["black","white","grey","nude","gold","blush","navy"],
#     "red":   ["black","white","navy","gold","beige"],
#     "blue":  ["white","beige","navy","gold","grey","brown"],
#     "green": ["white","beige","brown","camel","gold","black"],
#     "brown": ["beige","cream","white","olive","camel","gold"],
#     "camel": ["black","white","beige","brown","navy","olive"],
#     "burgundy": ["beige","grey","black","gold","cream","blush"],
#     "gold":  ["black","white","navy","burgundy","brown"],
#     "nude":  ["black","white","beige","camel","gold"],
#     "blush": ["black","white","grey","gold","navy"],
# }

# def colors_ok(c1, c2):
#     c1, c2 = c1.lower(), c2.lower()
#     return c1 == c2 or c2 in COLOR_COMPAT.get(c1, [])

# # -------------------------------------------------------
# # Category mapping
# # -------------------------------------------------------
# CATEGORIES = {
#     "tops":       ["crop top","blouse","tank top","shirt","t-shirt","sweater","cardigan","hoodie","corset top","topwear","sweatshirt","tunic"],
#     "bottoms":    ["jeans","leggings","skirt","mini skirt","midi skirt","shorts","trousers","wide leg pants","cargo pants","bottomwear","jeggings","capris"],
#     "dresses":    ["dress","mini dress","maxi dress","jumpsuit","co-ord set","kurta","saree"],
#     "outerwear":  ["jacket","blazer","coat","denim jacket","leather jacket","shrug","waistcoat"],
#     "shoes":      ["heels","sneakers","sandals","boots","ankle boots","flats","loafers","platform shoes","mules","wedges","footwear","stilettos"],
#     "bags":       ["handbag","tote bag","clutch","crossbody bag","backpack","sling bag","wallet"],
#     "accessories":["earrings","necklace","bracelet","sunglasses","hair accessory","belt","scarf","jewellery"],
# }

# def get_cat(item_type):
#     it = item_type.lower()
#     for cat, kws in CATEGORIES.items():
#         if any(k in it for k in kws):
#             return cat
#     return "other"

# PERSONA_PREFS = {
#     "Gen-Z":      ["crop top","cargo pants","wide leg pants","mini skirt","hoodie","sneakers","platform shoes","ankle boots","corset top","backpack"],
#     "Millennial": ["blouse","shirt","trousers","midi skirt","dress","blazer","coat","loafers","flats","heels","handbag","tote bag","cardigan"],
#     "Aesthetic":  ["dress","maxi dress","skirt","midi skirt","blouse","cardigan","flats","sandals","handbag","clutch","scarf"],
#     "All":        []
# }

# def ok_persona(item_type, persona):
#     if persona == "All": return True
#     prefs = PERSONA_PREFS.get(persona, [])
#     return not prefs or any(p in item_type.lower() for p in prefs)

# # -------------------------------------------------------
# # Load from MongoDB
# # -------------------------------------------------------
# @st.cache_data(ttl=300)
# def load_items():
#     return list(collection.find({"gender": "Women's"}, {"_id": 0}))

# # -------------------------------------------------------
# # Build outfit
# # -------------------------------------------------------
# def build_outfit(items, location, formality, color, persona):
#     outfit = {}
#     for cat in ["dresses","tops","bottoms","outerwear","shoes","bags","accessories"]:

#         #skip what user already has 
#         if skip_category and cat == skip_category:
#             continue
#         candidates = []
#         for item in items:
#             item_cat = item.get("category") or get_cat(item.get("item_type",""))
#             if item_cat != cat: continue
#             if location == "Outdoor" and item.get("indoor_outdoor","").lower() == "indoor": continue
#             if formality == "Formal" and item.get("formality","").lower() == "casual": continue
#             if formality == "Casual" and item.get("formality","").lower() == "formal": continue
#             ip = item.get("style_persona","")
#             if persona != "All" and ip and ip != persona: continue
#             if not ok_persona(item.get("item_type",""), persona): continue
#             candidates.append(item)

#         if not candidates: continue

#         if color and color != "any":
#             scored = sorted(candidates, key=lambda i: (
#                 2 if i.get("color","").lower() == color.lower()
#                 else 1 if colors_ok(color, i.get("color",""))
#                 else 0
#             ), reverse=True)
#             best = scored[0]
#         else:
#             best = candidates[0]

#         if cat in ["tops","bottoms"] and "dresses" in outfit: continue
#         outfit[cat] = best
#     return outfit

# # -------------------------------------------------------
# # Display product card
# # -------------------------------------------------------
# # def show_card(item, category):
# #     # Image
# #     path = item.get("path","")
# #     img_url = item.get("image_url","")
# #     if path and os.path.exists(path):
# #         st.image(Image.open(path).convert("RGB"), use_container_width=True)
# #     elif img_url and img_url.startswith("http"):
# #         st.image(img_url, use_container_width=True)
# #     else:
# #         st.markdown(f"🖼️ _{item.get('item_type', category).title()}_")

# #     # Info
# #     name    = (item.get("product_name") or item.get("item_type","")).title()
# #     brand   = item.get("brand","")
# #     price   = item.get("price","")
# #     persona = item.get("style_persona","")
# #     pc      = {"Gen-Z":"tag-genz","Millennial":"tag-millennial","Aesthetic":"tag-aesthetic"}.get(persona,"tag-millennial")
# #     pe      = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")

# #     price_html = f"<div class='product-price'>₹{price}</div>" if price else ""
# #     st.markdown(f"""
# #     <div class="product-card">
# #         <div class="product-name">{name[:38]}</div>
# #         <div class="product-brand">{brand}</div>
# #         {price_html}
# #         <span class="persona-tag {pc}">{pe} {persona}</span>
# #     </div>
# #     """, unsafe_allow_html=True)

# #     # Buy links
# #     links = item.get("buy_links", {})
# #     if links:
# #         html = ""
# #         if links.get("myntra"): html += f'<a href="{links["myntra"]}" target="_blank" class="buy-btn">🛍️ Myntra</a>'
# #         if links.get("amazon"): html += f'<a href="{links["amazon"]}" target="_blank" class="buy-btn buy-btn-amazon">📦 Amazon</a>'
# #         if links.get("ajio"):   html += f'<a href="{links["ajio"]}" target="_blank" class="buy-btn buy-btn-ajio">✨ Ajio</a>'
# #         if html: st.markdown(html, unsafe_allow_html=True)

# def show_card(item, category):
#     # Image
#     path    = item.get("path", "")
#     img_url = item.get("image_url", "")
#     if path and os.path.exists(path):
#         st.image(Image.open(path).convert("RGB"), use_container_width=True)
#     elif img_url and img_url.startswith("http"):
#         st.image(img_url, use_container_width=True)
#     else:
#         st.markdown(f"🖼️ _{item.get('item_type', category).title()}_")

#     # Info — use st.caption instead of raw HTML
#     name    = (item.get("product_name") or item.get("item_type","")).title()
#     brand   = item.get("brand","")
#     price   = item.get("price","")
#     persona = item.get("style_persona","")
#     pe      = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")

#     st.caption(f"{name[:35]}")
#     if brand:
#         st.caption(f"_{brand}_")
#     if price:
#         st.markdown(f"**₹{price}**")
#     st.caption(f"{pe} {persona}")

#     # Buy links
#     links = item.get("buy_links", {})
#     if links.get("myntra"):
#         st.markdown(f'[🛍️ Myntra]({links["myntra"]}) | [📦 Amazon]({links.get("amazon","#")})')
# # -------------------------------------------------------
# # UI
# # -------------------------------------------------------
# st.markdown("# ✨ Outfit Recommender")
# st.caption("Complete outfits from your wardrobe + real Myntra products.")

# # Stats
# total = collection.count_documents({"gender": "Women's"})
# myntra_count = collection.count_documents({"source": "myntra_kaggle"})
# local_count  = total - myntra_count
# st.caption(f"📊 {total} items — {myntra_count} Myntra products + {local_count} your wardrobe")
# st.divider()

# st.markdown("### Your Preferences")
# col1, col2 = st.columns(2)
# with col1:
#     location = st.selectbox("Location", ["Outdoor","Indoor"])
#     persona  = st.selectbox("Style Persona", ["All","Gen-Z","Millennial","Aesthetic"])
# with col2:
#     formality = st.selectbox("Occasion", ["Casual","Smart Casual","Formal","Party","Streetwear"])
#     pref_color = st.selectbox("Preferred Color", [
#         "Any","black","white","beige","navy","pink","red",
#         "blue","green","brown","camel","burgundy","grey","gold","nude","blush"
#     ])

# desc = {"Gen-Z":"⚡ Y2K, streetwear, bold, cargo, chunky shoes",
#         "Millennial":"✨ Minimalist, tailored, smart casual, classic",
#         "Aesthetic":"🌿 Cottagecore, dark academia, lace, floral, vintage",
#         "All":"🎯 No style filter"}
# st.caption(desc.get(persona,""))
# st.divider()

# st.markdown("### What are you wearing?")
# wearing = st.selectbox(
#     "I already have a...",
#     ["Nothing selected", "tops", "bottoms", "dresses",
#      "outerwear", "shoes", "bags", "accessories"],
#     help="Select what you're already wearing — we'll complete the rest"
# )

# if st.button("✨ Recommend Outfit"):
#     with st.spinner("Finding your perfect outfit..."):
#         items = load_items()

#     if not items:
#         st.warning("👗 Wardrobe is empty! Run `python Scripts/bulk_tag_images.py` first.")
#         st.info("💡 For Myntra products run: `python Scripts/load_myntra_to_mongodb.py`")
#     else:
#         color_in = pref_color if pref_color != "Any" else ""
#         outfit   = build_outfit(items, location, formality, color_in, persona)

#         if not outfit:
#             st.error("😔 No matching items. Try changing your filters.")
#         else:
#             pe = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
#             st.markdown(f"## {pe} Your Complete Outfit")
#             st.caption(f"{persona} · {formality} · {location}")

#             cols = st.columns(min(len(outfit), 4))
#             for i, (cat, item) in enumerate(outfit.items()):
#                 with cols[i % len(cols)]:
#                     st.markdown(f"**{cat.title()}**")
#                     show_card(item, cat)

# #             st.divider()
# #             st.markdown("**Outfit Summary**")
# #             scols = st.columns(2)
# #             for i, (cat, item) in enumerate(outfit.items()):
# #                 with scols[i % 2]:
# #                     name  = (item.get("product_name") or item.get("item_type","")).title()
# #                     brand = item.get("brand","")
# #                     price = item.get("price","")
# #                     st.markdown(f"**{cat.title()}:** {name[:35]}"
# #                                f"{' — '+brand if brand else ''}"
# #                                f"{' · ₹'+str(price) if price else ''}")

# """
# 2_Get_Outfit_Suggestion.py — Smart Women's Outfit Recommender

# KEY FEATURE: Upload a clothing item → CLIP detects what it is
# → recommends COMPLEMENTARY pieces from MongoDB to complete the outfit.

# This is the originality: the system understands what you have
# and finds what you need — not just random filtering.
# """

# import os
# import sys
# import torch
# import numpy as np
# import streamlit as st
# from pathlib import Path
# from PIL import Image
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# from transformers import CLIPProcessor, CLIPModel
# from io import BytesIO

# # -------------------------------------------------------
# # Add fitcheck to path
# # -------------------------------------------------------
# sys.path.insert(0, str(Path(__file__).parent.parent))

# st.set_page_config(page_title="Outfit Recommender", page_icon="✨", layout="centered")

# # -------------------------------------------------------
# # Authentic Fashion CSS — same editorial palette
# # -------------------------------------------------------
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');

#     html, body, [class*="css"] { font-family: 'Jost', sans-serif; font-weight: 300; letter-spacing: 0.02em; }
#     #MainMenu, footer, header { visibility: hidden; }
#     .block-container { padding-top: 2rem; max-width: 900px; }

#     .page-title {
#         font-family: 'Cormorant Garamond', serif;
#         font-size: 2.8rem;
#         font-weight: 300;
#         font-style: italic;
#         color: #f5f0eb;
#         margin-bottom: 0.3rem;
#     }
#     .section-label {
#         font-size: 0.62rem; font-weight: 400; letter-spacing: 0.3em;
#         text-transform: uppercase; color: #D4AF37; margin: 1.5rem 0 0.8rem;
#         display: flex; align-items: center; gap: 12px;
#     }
#     .section-label::after { content: ''; flex: 1; height: 1px; background: rgba(212,175,55,0.2); }

#     /* Upload zone */
#     [data-testid="stFileUploader"] {
#         border: 1px solid rgba(212,175,55,0.2) !important;
#         border-radius: 0 !important;
#         background: rgba(212,175,55,0.02) !important;
#     }

#     /* Detected item banner */
#     .detected-banner {
#         background: rgba(212,175,55,0.06);
#         border: 1px solid rgba(212,175,55,0.2);
#         padding: 1rem 1.2rem;
#         margin: 1rem 0;
#         display: flex;
#         align-items: center;
#         gap: 12px;
#     }
#     .detected-icon { font-size: 1.4rem; }
#     .detected-label { font-size: 0.65rem; letter-spacing: 0.2em; text-transform: uppercase; color: rgba(245,240,235,0.4); }
#     .detected-value { font-family: 'Cormorant Garamond', serif; font-size: 1.2rem; font-style: italic; color: #D4AF37; }

#     /* Preference selects */
#     .stSelectbox label {
#         font-size: 0.62rem !important; letter-spacing: 0.2em !important;
#         text-transform: uppercase !important; color: rgba(245,240,235,0.45) !important;
#     }
#     [data-baseweb="select"] > div {
#         border-radius: 0 !important;
#         border-color: rgba(212,175,55,0.2) !important;
#         background: rgba(212,175,55,0.02) !important;
#     }

#     /* Recommend button */
#     .stButton > button {
#         background: transparent !important; color: #D4AF37 !important;
#         border: 1px solid #D4AF37 !important; border-radius: 0 !important;
#         padding: 0.75rem !important; font-family: 'Jost', sans-serif !important;
#         font-size: 0.68rem !important; letter-spacing: 0.3em !important;
#         text-transform: uppercase !important; width: 100% !important;
#         transition: all 0.3s !important;
#     }
#     .stButton > button:hover { background: #D4AF37 !important; color: #0d0d0d !important; }

#     /* Outfit grid cards */
#     .outfit-category {
#         font-size: 0.58rem; letter-spacing: 0.25em; text-transform: uppercase;
#         color: rgba(245,240,235,0.35); margin-bottom: 0.5rem; text-align: center;
#     }
#     .product-info {
#         background: rgba(212,175,55,0.03);
#         border-top: 1px solid rgba(212,175,55,0.1);
#         padding: 0.6rem;
#         text-align: center;
#     }
#     .product-name-text {
#         font-family: 'Cormorant Garamond', serif;
#         font-size: 0.85rem; font-style: italic; color: #f5f0eb;
#         margin-bottom: 2px; line-height: 1.3;
#     }
#     .product-brand-text { font-size: 0.62rem; color: rgba(245,240,235,0.35); letter-spacing: 0.1em; text-transform: uppercase; }
#     .product-price-text { font-size: 0.78rem; color: #D4AF37; font-weight: 400; margin: 3px 0; }
#     .persona-pill {
#         display: inline-block; padding: 2px 8px; border: 1px solid;
#         font-size: 0.58rem; letter-spacing: 0.12em; text-transform: uppercase;
#         margin-top: 4px;
#     }
#     .pill-genz { border-color: #ff6b9d; color: #ff6b9d; }
#     .pill-millennial { border-color: #D4AF37; color: #D4AF37; }
#     .pill-aesthetic { border-color: #9caf88; color: #9caf88; }

#     /* Buy links */
#     .buy-links { display: flex; gap: 4px; justify-content: center; margin-top: 6px; flex-wrap: wrap; }
#     .buy-link {
#         font-size: 0.58rem; letter-spacing: 0.1em; text-transform: uppercase;
#         padding: 3px 8px; border: 1px solid rgba(212,175,55,0.3);
#         color: rgba(245,240,235,0.5) !important; text-decoration: none !important;
#         transition: all 0.2s;
#     }
#     .buy-link:hover { border-color: #D4AF37; color: #D4AF37 !important; }

#     /* Summary table */
#     .summary-row {
#         display: flex; justify-content: space-between; align-items: baseline;
#         padding: 0.6rem 0; border-bottom: 1px solid rgba(212,175,55,0.08);
#         font-size: 0.78rem;
#     }
#     .summary-cat { color: rgba(245,240,235,0.4); letter-spacing: 0.1em; text-transform: uppercase; font-size: 0.62rem; }
#     .summary-item { font-family: 'Cormorant Garamond', serif; font-style: italic; color: #f5f0eb; }
#     .summary-price { color: #D4AF37; font-size: 0.72rem; }

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
# # CLIP for detecting uploaded item
# # -------------------------------------------------------
# @st.cache_resource
# def load_clip():
#     device =  "cpu"
#     proc  = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
#     mdl   = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
#     return proc, mdl, device

# # -------------------------------------------------------
# # Category definitions
# # -------------------------------------------------------
# CATEGORY_LABELS = {
#     "tops":        "a women's top, blouse, shirt, crop top, tank top or sweater",
#     "bottoms":     "women's jeans, pants, trousers, shorts, leggings or skirt",
#     "dresses":     "a women's dress, jumpsuit, maxi dress or mini dress",
#     "outerwear":   "a women's jacket, coat, blazer or cardigan",
#     "shoes":       "women's shoes, heels, sneakers, boots or sandals",
#     "bags":        "a women's handbag, tote bag, clutch or purse",
#     "accessories": "women's jewellery, earrings, necklace, sunglasses or scarf",
# }

# # What to recommend for each detected category
# COMPLETION_MAP = {
#     "tops":        ["bottoms", "shoes", "bags", "accessories", "outerwear"],
#     "bottoms":     ["tops", "shoes", "bags", "accessories", "outerwear"],
#     "dresses":     ["shoes", "bags", "accessories", "outerwear"],
#     "outerwear":   ["tops", "bottoms", "shoes", "bags"],
#     "shoes":       ["tops", "bottoms", "bags", "accessories"],
#     "bags":        ["tops", "bottoms", "shoes", "accessories"],
#     "accessories": ["tops", "bottoms", "shoes", "bags"],
# }

# def detect_garment_type(image: Image.Image) -> tuple[str, float]:
#     """Use CLIP zero-shot to detect what garment type was uploaded."""
#     proc, mdl, device = load_clip()

#     labels = list(CATEGORY_LABELS.values())
#     keys   = list(CATEGORY_LABELS.keys())

#     inputs = proc(
#         text=labels, images=image,
#         return_tensors="pt", padding=True
#     ).to(device)

#     with torch.no_grad():
#         outputs = mdl(**inputs)
#         probs   = outputs.logits_per_image.softmax(dim=1).cpu().numpy()[0]

#     best_idx  = int(np.argmax(probs))
#     best_cat  = keys[best_idx]
#     best_conf = float(probs[best_idx])
#     return best_cat, best_conf

# def get_clip_embedding(image: Image.Image) -> np.ndarray:
#     """Get CLIP image embedding for similarity scoring."""
#     proc, mdl, device = load_clip()
#     inputs = proc(images=image, return_tensors="pt").to(device)
#     with torch.no_grad():
#         feats = mdl.get_image_features(**inputs)
#         feats = feats / feats.norm(dim=-1, keepdim=True)
#     return feats.cpu().numpy()[0]

# # -------------------------------------------------------
# # Color compatibility
# # -------------------------------------------------------
# COLOR_COMPAT = {
#     "black":    ["white","beige","cream","nude","red","pink","gold","silver","grey","blush","ivory"],
#     "white":    ["black","navy","blue","red","pink","beige","grey","gold","coral","camel"],
#     "beige":    ["black","white","brown","camel","navy","olive","burgundy","cream"],
#     "navy":     ["white","beige","cream","gold","red","pink","grey","camel"],
#     "grey":     ["black","white","pink","blush","navy","burgundy","yellow","camel"],
#     "pink":     ["black","white","grey","nude","gold","blush","navy","beige"],
#     "red":      ["black","white","navy","gold","beige","cream"],
#     "blue":     ["white","beige","navy","gold","grey","brown","camel"],
#     "green":    ["white","beige","brown","camel","gold","black","cream"],
#     "brown":    ["beige","cream","white","olive","camel","gold","burgundy"],
#     "camel":    ["black","white","beige","brown","navy","olive","cream","gold"],
#     "burgundy": ["beige","grey","black","gold","cream","blush","camel"],
#     "olive":    ["white","beige","brown","camel","black","cream"],
#     "gold":     ["black","white","navy","burgundy","brown","beige"],
#     "nude":     ["black","white","beige","camel","gold","blush"],
#     "blush":    ["black","white","grey","gold","navy","beige"],
#     "ivory":    ["black","brown","navy","camel","burgundy","gold"],
#     "cream":    ["black","brown","navy","camel","burgundy","olive"],
# }

# def color_score(c1: str, c2: str) -> int:
#     c1, c2 = c1.lower(), c2.lower()
#     if c1 == c2: return 2
#     return 1 if c2 in COLOR_COMPAT.get(c1, []) else 0

# # -------------------------------------------------------
# # Persona preferences
# # -------------------------------------------------------
# PERSONA_PREFS = {
#     "Gen-Z":      ["crop top","cargo","wide leg","mini skirt","hoodie","sneakers","platform","ankle boots","corset","backpack","chunky"],
#     "Millennial": ["blouse","shirt","trousers","midi skirt","dress","blazer","coat","loafers","flats","heels","handbag","tote","cardigan"],
#     "Aesthetic":  ["dress","maxi","skirt","midi","blouse","cardigan","flats","sandals","handbag","clutch","scarf","lace","floral"],
#     "All":        []
# }

# def ok_persona(item_type: str, persona: str) -> bool:
#     if persona == "All": return True
#     prefs = PERSONA_PREFS.get(persona, [])
#     return not prefs or any(p in item_type.lower() for p in prefs)

# def get_cat(item_type: str) -> str:
#     it = item_type.lower()
#     CATS = {
#         "tops":       ["top","blouse","shirt","t-shirt","tshirt","tank","crop","sweater","cardigan","hoodie","corset","sweatshirt","tunic","camisole","vest","kurti","pullover"],
#         "bottoms":    ["jean","pant","trouser","legging","skirt","shorts","capri","cargo","palazzo","jogger","culotte"],
#         "dresses":    ["dress","gown","jumpsuit","romper","coord","playsuit","saree","kurta"],
#         "outerwear":  ["jacket","blazer","coat","shrug","cape","bomber","windbreaker","trench"],
#         "shoes":      ["heel","pump","stiletto","wedge","sneaker","trainer","boot","sandal","loafer","flat","mule","shoe","footwear"],
#         "bags":       ["bag","purse","tote","clutch","sling","backpack","crossbody","satchel","hobo","wallet"],
#         "accessories":["earring","necklace","bracelet","ring","jewel","sunglass","goggle","scarf","stole","hair","belt","watch"],
#     }
#     for cat, kws in CATS.items():
#         if any(k in it for k in kws): return cat
#     return "other"

# # -------------------------------------------------------
# # Smart outfit builder
# # -------------------------------------------------------
# @st.cache_data(ttl=300)
# def load_items():
#     return list(collection.find({"gender": "Women's"}, {"_id": 0}))

# def build_smart_outfit(
#     uploaded_color: str,
#     detected_category: str,
#     persona: str,
#     formality: str,
#     location: str,
#     n_results: int = 1,
# ) -> dict:
#     """
#     Build outfit by completing what the user is missing.
#     Scores each candidate by color compatibility + persona match.
#     """
#     items = load_items()
#     completion_cats = COMPLETION_MAP.get(detected_category, list(COMPLETION_MAP.keys()))
#     outfit = {}

#     for cat in completion_cats:
#         candidates = []
#         for item in items:
#             item_cat = item.get("category_group") or item.get("category") or get_cat(item.get("item_type",""))
#             if item_cat != cat: continue
#             if location == "Outdoor" and item.get("indoor_outdoor","").lower() == "indoor": continue
#             if formality == "Formal" and item.get("formality","").lower() == "casual": continue
#             if formality == "Casual" and item.get("formality","").lower() == "formal": continue
#             ip = item.get("style_persona","")
#             if persona != "All" and ip and ip != persona: continue
#             if not ok_persona(item.get("item_type",""), persona): continue
#             candidates.append(item)

#         if not candidates: continue

#         # Score by color compatibility with uploaded item
#         scored = sorted(
#             candidates,
#             key=lambda i: color_score(uploaded_color, i.get("color","").lower()),
#             reverse=True
#         )
#         outfit[cat] = scored[0]

#     return outfit

# # -------------------------------------------------------
# # Display card
# # -------------------------------------------------------
# # def show_card(item: dict, category: str):
# #     path    = item.get("path","")
# #     img_url = item.get("img_url") or item.get("image_url","")

# #     if path and os.path.exists(path):
# #         st.image(Image.open(path).convert("RGB"), use_container_width=True)
# #     elif img_url and img_url.startswith("http"):
# #         try:
# #             st.image(img_url, use_container_width=True)
# #         except Exception:
# #             st.markdown("🖼️")
# #     else:
# #         st.markdown(f"<div style='height:160px;background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.1);display:flex;align-items:center;justify-content:center;font-size:0.7rem;color:rgba(245,240,235,0.2);letter-spacing:0.1em'>NO IMAGE</div>", unsafe_allow_html=True)

# #     name    = (item.get("name") or item.get("product_name") or item.get("item_type","")).title()
# #     brand   = item.get("brand","")
# #     price   = item.get("price","")
# #     persona = item.get("style_persona","")
# #     pc      = {"Gen-Z":"pill-genz","Millennial":"pill-millennial","Aesthetic":"pill-aesthetic"}.get(persona,"pill-millennial")
# #     pe      = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
# #     product_url = item.get("product_url","")

# #     price_html  = f'<div class="product-price-text">₹{price}</div>' if price and price != "nan" else ""
# #     brand_html  = f'<div class="product-brand-text">{brand}</div>' if brand and brand != "nan" else ""

# #     st.markdown(f"""
# #     <div class="product-info">
# #         <div class="product-name-text">{name[:40]}</div>
# #         {brand_html}
# #         {price_html}
# #         <div><span class="persona-pill {pc}">{pe} {persona}</span></div>
# #     </div>
# #     """, unsafe_allow_html=True)

# #     # Buy links
# #     query = (name + " women").replace(" ", "+")
# #     links = item.get("buy_links", {})
# #     myntra_url = links.get("myntra") or product_url or f"https://www.myntra.com/search?rawQuery={query}"
# #     amazon_url = links.get("amazon") or f"https://www.amazon.in/s?k={query}"
# #     ajio_url   = links.get("ajio")   or f"https://www.ajio.com/search/?text={query}"

# #     st.markdown(f"""
# #     <div class="buy-links">
# #         <a href="{myntra_url}" target="_blank" class="buy-link">Myntra</a>
# #         <a href="{amazon_url}" target="_blank" class="buy-link">Amazon</a>
# #         <a href="{ajio_url}"   target="_blank" class="buy-link">Ajio</a>
# #     </div>
# #     """, unsafe_allow_html=True)

# def show_card(item: dict, category: str):
#     path    = item.get("path","")
#     img_url = item.get("img_url") or item.get("image_url","")

#     if path and os.path.exists(path):
#         st.image(Image.open(path).convert("RGB"), use_container_width=True)
#     elif img_url and img_url.startswith("http"):
#         try:
#             st.image(img_url, use_container_width=True)
#         except Exception:
#             st.markdown("🖼️")
#     else:
#         st.markdown(
#             "<div style='height:160px;background:rgba(212,175,55,0.04);"
#             "border:1px solid rgba(212,175,55,0.1);display:flex;align-items:center;"
#             "justify-content:center;font-size:0.7rem;color:rgba(245,240,235,0.2);"
#             "letter-spacing:0.1em'>NO IMAGE</div>",
#             unsafe_allow_html=True
#         )

#     name        = (item.get("name") or item.get("product_name") or item.get("item_type","")).title()
#     brand       = item.get("brand","")
#     price       = item.get("price","")
#     persona     = item.get("style_persona","")
#     pc          = {"Gen-Z":"pill-genz","Millennial":"pill-millennial","Aesthetic":"pill-aesthetic"}.get(persona,"pill-millennial")
#     pe          = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
#     product_url = item.get("product_url","")

#     # ── Use native Streamlit for text — avoids HTML escaping in columns ──
#     st.markdown(f"*{name[:40]}*")
#     if brand and str(brand) != "nan":
#         st.caption(brand.upper())
#     if price and str(price) != "nan":
#         st.markdown(
#             f"<div style='color:#D4AF37;font-size:0.78rem;text-align:center'>₹{price}</div>",
#             unsafe_allow_html=True
#         )
#     if persona:
#         st.markdown(
#             f"<div style='text-align:center'>"
#             f"<span class='persona-pill {pc}'>{pe} {persona}</span>"
#             f"</div>",
#             unsafe_allow_html=True
#         )

#     # ── Buy links ──
#     query      = (name + " women").replace(" ", "+")
#     links      = item.get("buy_links", {}) or {}
#     myntra_url = links.get("myntra") or product_url or f"https://www.myntra.com/search?rawQuery={query}"
#     amazon_url = links.get("amazon") or f"https://www.amazon.in/s?k={query}"
#     ajio_url   = links.get("ajio")   or f"https://www.ajio.com/search/?text={query}"

#     st.markdown(
#         f"<div class='buy-links'>"
#         f"<a href='{myntra_url}' target='_blank' class='buy-link'>Myntra</a>"
#         f"<a href='{amazon_url}' target='_blank' class='buy-link'>Amazon</a>"
#         f"<a href='{ajio_url}'   target='_blank' class='buy-link'>Ajio</a>"
#         f"</div>",
#         unsafe_allow_html=True
#     )

# # -------------------------------------------------------
# # Page Header
# # -------------------------------------------------------
# st.markdown("""
# <div style="padding: 2rem 0 1rem">
#     <div style="font-size:0.62rem;letter-spacing:0.3em;text-transform:uppercase;color:#D4AF37;margin-bottom:0.5rem">Complete Your Look</div>
#     <h1 class="page-title">Outfit Recommender</h1>
#     <div style="font-size:0.72rem;font-weight:300;color:rgba(245,240,235,0.4);letter-spacing:0.05em">
#         Upload what you're wearing → we find what completes it
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # Stats bar
# total        = collection.count_documents({"gender": "Women's"})
# myntra_count = collection.count_documents({"source": "myntra_kaggle"})
# st.markdown(f"""
# <div style="font-size:0.62rem;letter-spacing:0.15em;color:rgba(245,240,235,0.25);padding:0.5rem 0 1.5rem;border-bottom:1px solid rgba(212,175,55,0.1)">
#     {total:,} items in wardrobe — {myntra_count:,} Myntra products
# </div>
# """, unsafe_allow_html=True)

# # -------------------------------------------------------
# # Upload Your Item
# # -------------------------------------------------------
# st.markdown('<div class="section-label">Upload the item you\'re wearing</div>', unsafe_allow_html=True)
# uploaded_item = st.file_uploader(
#     "Upload your top, jeans, dress — whatever you're working with",
#     type=["jpg","jpeg","png","webp"],
#     label_visibility="collapsed",
#     key="item_upload"
# )

# detected_category = None
# uploaded_color    = "black"

# if uploaded_item:
#     item_img = Image.open(uploaded_item).convert("RGB")

#     col1, col2 = st.columns([1, 2], gap="large")
#     with col1:
#         st.image(item_img, use_container_width=True)

#     with col2:
#         with st.spinner("Identifying your item..."):
#             detected_category, confidence = detect_garment_type(item_img)

#         # Also detect color using CLIP
#         from tagging import classify as clip_classify, COLOR_LABELS
#         uploaded_color = clip_classify(item_img, COLOR_LABELS).lower()

#         st.markdown(f"""
#         <div class="detected-banner">
#             <div class="detected-icon">🎯</div>
#             <div>
#                 <div class="detected-label">Detected item</div>
#                 <div class="detected-value">{detected_category.replace("_"," ").title()} — {uploaded_color.title()}</div>
#             </div>
#         </div>
#         <div style="font-size:0.65rem;color:rgba(245,240,235,0.3);letter-spacing:0.08em">
#             Confidence: {confidence:.0%} · We'll find pieces to complete this look
#         </div>
#         """, unsafe_allow_html=True)

# # -------------------------------------------------------
# # Preferences
# # -------------------------------------------------------
# st.markdown('<div class="section-label">Your Style Preferences</div>', unsafe_allow_html=True)

# col1, col2 = st.columns(2)
# with col1:
#     persona  = st.selectbox("Style Persona", ["All","Gen-Z","Millennial","Aesthetic"])
#     location = st.selectbox("Location", ["Outdoor","Indoor"])
# with col2:
#     formality  = st.selectbox("Occasion", ["Casual","Smart Casual","Formal","Party","Streetwear"])
#     pref_color = st.selectbox("Override Color", ["Auto (from image)","black","white","beige","navy","pink","red","blue","green","brown","gold","nude","blush"])

# desc = {
#     "Gen-Z":      "⚡ Y2K · Streetwear · Bold · Chunky shoes",
#     "Millennial": "✨ Minimalist · Tailored · Smart casual · Classic",
#     "Aesthetic":  "🌿 Cottagecore · Dark academia · Lace · Floral",
#     "All":        "🎯 No filter — show all styles"
# }
# st.caption(desc.get(persona,""))
# st.markdown("")

# if st.button("Build My Outfit"):
#     if not uploaded_item:
#         st.warning("Upload the item you're wearing first — so we know what to complete.")
#     else:
#         # Use preferred color or auto-detected
#         color_to_use = uploaded_color if pref_color == "Auto (from image)" else pref_color

#         with st.spinner("Finding your perfect outfit..."):
#             outfit = build_smart_outfit(
#                 uploaded_color=color_to_use,
#                 detected_category=detected_category or "tops",
#                 persona=persona,
#                 formality=formality,
#                 location=location,
#             )

#         if not outfit:
#             st.error("No matching items found. Try changing your filters or load more items with `python Scripts/load_myntra_to_mongodb.py`")
#         else:
#             pe_emoji = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
#             st.markdown(f"""
#             <div style="padding: 2rem 0 1rem">
#                 <div style="font-size:0.62rem;letter-spacing:0.3em;text-transform:uppercase;color:#D4AF37;margin-bottom:0.4rem">
#                     {pe_emoji} Complete Outfit · {persona} · {formality}
#                 </div>
#                 <div style="font-family:'Cormorant Garamond',serif;font-size:1.8rem;font-style:italic;color:#f5f0eb">
#                     Here's what completes your look
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)

#             # Show uploaded item first
#             st.markdown('<div class="section-label">Your Item</div>', unsafe_allow_html=True)
#             uc1, uc2, uc3 = st.columns([1, 2, 1])
#             with uc2:
#                 st.image(item_img, caption=f"{detected_category.replace('_',' ').title()} — {uploaded_color.title()}", use_container_width=True)

#             # Show recommended pieces
#             st.markdown('<div class="section-label">Recommended to Complete Your Outfit</div>', unsafe_allow_html=True)

#             cols = st.columns(min(len(outfit), 4))
#             for i, (cat, item) in enumerate(outfit.items()):
#                 with cols[i % len(cols)]:
#                     st.markdown(f'<div class="outfit-category">{cat.replace("_"," ")}</div>', unsafe_allow_html=True)
#                     show_card(item, cat)

#             # Summary
#             st.markdown("---")
#             st.markdown('<div class="section-label">Outfit Summary</div>', unsafe_allow_html=True)

#             # Uploaded item row
#             st.markdown(f"""
#             <div class="summary-row">
#                 <span class="summary-cat">Your item</span>
#                 <span class="summary-item">{detected_category.replace("_"," ").title()} — {uploaded_color.title()}</span>
#                 <span class="summary-price">–</span>
#             </div>
#             """, unsafe_allow_html=True)

#             for cat, item in outfit.items():
#                 name  = (item.get("name") or item.get("product_name") or item.get("item_type","")).title()
#                 price = item.get("price","")
#                 price_str = f"₹{price}" if price and price != "nan" else "–"
#                 st.markdown(f"""
#                 <div class="summary-row">
#                     <span class="summary-cat">{cat.replace("_"," ")}</span>
#                     <span class="summary-item">{name[:45]}</span>
#                     <span class="summary-price">{price_str}</span>
#                 </div>
#                 """, unsafe_allow_html=True)

"""
2_Get_Outfit_Suggestion.py — Smart Women's Outfit Recommender
KEY FEATURE: Upload a clothing item → CLIP detects what it is
→ recommends COMPLEMENTARY pieces from MongoDB to complete the outfit.
This is the originality: the system understands what you have
and finds what you need — not just random filtering.
"""

import os
import sys
import torch
import numpy as np
import streamlit as st
from pathlib import Path
from PIL import Image
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from transformers import CLIPProcessor, CLIPModel
from io import BytesIO
import certifi

# -------------------------------------------------------
# Add fitcheck to path
# -------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent))

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
MONGO_URI = "mongodb+srv://fitcheck:fitcheck123@cluster0.ozebcow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

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
# CLIP for detecting uploaded item
# -------------------------------------------------------
@st.cache_resource
def load_clip():
    device =  "cpu"
    proc  = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    mdl   = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
    return proc, mdl, device

# -------------------------------------------------------
# Category definitions
# -------------------------------------------------------
CATEGORY_LABELS = {
    "tops":        "a women's top, blouse, shirt, crop top, tank top or sweater",
    "bottoms":     "women's jeans, pants, trousers, shorts, leggings or skirt",
    "dresses":     "a women's dress, jumpsuit, maxi dress or mini dress",
    "outerwear":   "a women's jacket, coat, blazer or cardigan",
    "shoes":       "women's shoes, heels, sneakers, boots or sandals",
    "bags":        "a women's handbag, tote bag, clutch or purse",
    "accessories": "women's jewellery, earrings, necklace, sunglasses or scarf",
}

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

def detect_garment_type(image: Image.Image) -> tuple[str, float]:
    """Use CLIP zero-shot to detect what garment type was uploaded."""
    proc, mdl, device = load_clip()

    labels = list(CATEGORY_LABELS.values())
    keys   = list(CATEGORY_LABELS.keys())

    inputs = proc(
        text=labels, images=image,
        return_tensors="pt", padding=True
    ).to(device)

    with torch.no_grad():
        outputs = mdl(**inputs)
        probs   = outputs.logits_per_image.softmax(dim=1).cpu().numpy()[0]

    best_idx  = int(np.argmax(probs))
    best_cat  = keys[best_idx]
    best_conf = float(probs[best_idx])
    return best_cat, best_conf

def get_clip_embedding(image: Image.Image) -> np.ndarray:
    """Get CLIP image embedding for similarity scoring."""
    proc, mdl, device = load_clip()
    inputs = proc(images=image, return_tensors="pt").to(device)
    with torch.no_grad():
        feats = mdl.get_image_features(**inputs)
        feats = feats / feats.norm(dim=-1, keepdim=True)
    return feats.cpu().numpy()[0]

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
    c1, c2 = c1.lower(), c2.lower()
    if c1 == c2: return 2
    return 1 if c2 in COLOR_COMPAT.get(c1, []) else 0

# -------------------------------------------------------
# Persona preferences
# -------------------------------------------------------
PERSONA_PREFS = {
    "Gen-Z":      ["crop top","cargo","wide leg","mini skirt","hoodie","sneakers","platform","ankle boots","corset","backpack","chunky"],
    "Millennial": ["blouse","shirt","trousers","midi skirt","dress","blazer","coat","loafers","flats","heels","handbag","tote","cardigan"],
    "Aesthetic":  ["dress","maxi","skirt","midi","blouse","cardigan","flats","sandals","handbag","clutch","scarf","lace","floral"],
    "All":        []
}

def ok_persona(item_type: str, persona: str) -> bool:
    if persona == "All": return True
    prefs = PERSONA_PREFS.get(persona, [])
    return not prefs or any(p in item_type.lower() for p in prefs)

def get_cat(item_type: str) -> str:
    it = item_type.lower()
    CATS = {
        "tops":       ["top","blouse","shirt","t-shirt","tshirt","tank","crop","sweater","cardigan","hoodie","corset","sweatshirt","tunic","camisole","vest","kurti","pullover"],
        "bottoms":    ["jean","pant","trouser","legging","skirt","shorts","capri","cargo","palazzo","jogger","culotte"],
        "dresses":    ["dress","gown","jumpsuit","romper","coord","playsuit","saree","kurta"],
        "outerwear":  ["jacket","blazer","coat","shrug","cape","bomber","windbreaker","trench"],
        "shoes":      ["heel","pump","stiletto","wedge","sneaker","trainer","boot","sandal","loafer","flat","mule","shoe","footwear"],
        "bags":       ["bag","purse","tote","clutch","sling","backpack","crossbody","satchel","hobo","wallet"],
        "accessories":["earring","necklace","bracelet","ring","jewel","sunglass","goggle","scarf","stole","hair","belt","watch"],
    }
    for cat, kws in CATS.items():
        if any(k in it for k in kws): return cat
    return "other"

# -------------------------------------------------------
# Smart outfit builder
# -------------------------------------------------------
@st.cache_data(ttl=300)
def load_items():
    return list(collection.find({"gender": "Women's"}, {"_id": 0}))

def build_smart_outfit(
    uploaded_color: str,
    detected_category: str,
    persona: str,
    formality: str,
    location: str,
    n_results: int = 1,
) -> dict:
    """
    Build outfit by completing what the user is missing.
    Scores each candidate by color compatibility + persona match.
    """
    items = load_items()
    completion_cats = COMPLETION_MAP.get(detected_category, list(COMPLETION_MAP.keys()))
    outfit = {}

    for cat in completion_cats:
        candidates = []
        for item in items:
            item_cat = item.get("category_group") or item.get("category") or get_cat(item.get("item_type",""))
            if item_cat != cat: continue
            if location == "Outdoor" and item.get("indoor_outdoor","").lower() == "indoor": continue
            if formality == "Formal" and item.get("formality","").lower() == "casual": continue
            if formality == "Casual" and item.get("formality","").lower() == "formal": continue
            ip = item.get("style_persona","")
            if persona != "All" and ip and ip != persona: continue
            if not ok_persona(item.get("item_type",""), persona): continue
            candidates.append(item)

        if not candidates: continue

        # Score by color compatibility with uploaded item
        scored = sorted(
            candidates,
            key=lambda i: color_score(uploaded_color, i.get("color","").lower()),
            reverse=True
        )
        outfit[cat] = scored[0]

    return outfit

# -------------------------------------------------------
# Display card
# -------------------------------------------------------
# def show_card(item: dict, category: str):
#     path    = item.get("path","")
#     img_url = item.get("img_url") or item.get("image_url","")

#     if path and os.path.exists(path):
#         st.image(Image.open(path).convert("RGB"), use_container_width=True)
#     elif img_url and img_url.startswith("http"):
#         try:
#             st.image(img_url, use_container_width=True)
#         except Exception:
#             st.markdown("🖼️")
#     else:
#         st.markdown(f"<div style='height:160px;background:rgba(212,175,55,0.04);border:1px solid rgba(212,175,55,0.1);display:flex;align-items:center;justify-content:center;font-size:0.7rem;color:rgba(245,240,235,0.2);letter-spacing:0.1em'>NO IMAGE</div>", unsafe_allow_html=True)

#     name    = (item.get("name") or item.get("product_name") or item.get("item_type","")).title()
#     brand   = item.get("brand","")
#     price   = item.get("price","")
#     persona = item.get("style_persona","")
#     pc      = {"Gen-Z":"pill-genz","Millennial":"pill-millennial","Aesthetic":"pill-aesthetic"}.get(persona,"pill-millennial")
#     pe      = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"")
#     product_url = item.get("product_url","")

#     price_html  = f'<div class="product-price-text">₹{price}</div>' if price and price != "nan" else ""
#     brand_html  = f'<div class="product-brand-text">{brand}</div>' if brand and brand != "nan" else ""

#     st.markdown(f"""
#     <div class="product-info">
#         <div class="product-name-text">{name[:40]}</div>
#         {brand_html}
#         {price_html}
#         <div><span class="persona-pill {pc}">{pe} {persona}</span></div>
#     </div>
#     """, unsafe_allow_html=True)

#     # Buy links
#     query = (name + " women").replace(" ", "+")
#     links = item.get("buy_links", {})
#     myntra_url = links.get("myntra") or product_url or f"https://www.myntra.com/search?rawQuery={query}"
#     amazon_url = links.get("amazon") or f"https://www.amazon.in/s?k={query}"
#     ajio_url   = links.get("ajio")   or f"https://www.ajio.com/search/?text={query}"

#     st.markdown(f"""
#     <div class="buy-links">
#         <a href="{myntra_url}" target="_blank" class="buy-link">Myntra</a>
#         <a href="{amazon_url}" target="_blank" class="buy-link">Amazon</a>
#         <a href="{ajio_url}"   target="_blank" class="buy-link">Ajio</a>
#     </div>
#     """, unsafe_allow_html=True)

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
        from tagging import classify as clip_classify, COLOR_LABELS
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