# # """
# # Fashion AI Advisor.py — Women's AI Stylist
# # Main Streamlit app — outfit critique with style persona detection.
# # """

# # from PIL import Image
# # import io
# # import imagehash
# # import streamlit as st
# # from analyze_outfit import (
# #     analyze_outfit_tool,
# #     extract_comment,
# #     extract_rating,
# #     extract_style_paragraph,
# #     extract_persona,
# # )
# # import dns
# # from pymongo import MongoClient
# # from datetime import datetime, timezone
# # import os

# # # -------------------------------------------------------
# # # Page Config
# # # -------------------------------------------------------
# # st.set_page_config(
# #     page_title="FitCheck.AI — Women's Stylist",
# #     page_icon="👗",
# #     layout="centered"
# # )

# # # -------------------------------------------------------
# # # Custom CSS — Women's Fashion Aesthetic
# # # -------------------------------------------------------
# # st.markdown("""
# # <style>
# #     @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

# #     html, body, [class*="css"] {
# #         font-family: 'DM Sans', sans-serif;
# #     }
# #     h1, h2, h3 {
# #         font-family: 'Playfair Display', serif;
# #     }
# #     .main-title {
# #         font-family: 'Playfair Display', serif;
# #         font-size: 2.8rem;
# #         font-weight: 700;
# #         color: #1a1a1a;
# #         margin-bottom: 0.2rem;
# #     }
# #     .subtitle {
# #         font-size: 1rem;
# #         color: #888;
# #         margin-bottom: 2rem;
# #         font-weight: 300;
# #     }
# #     .persona-badge {
# #         display: inline-block;
# #         padding: 6px 18px;
# #         border-radius: 20px;
# #         font-weight: 500;
# #         font-size: 0.9rem;
# #         margin-top: 8px;
# #     }
# #     .persona-genz {
# #         background: #ffe4f0;
# #         color: #c0256f;
# #         border: 1px solid #f9a8d4;
# #     }
# #     .persona-millennial {
# #         background: #fef3c7;
# #         color: #92400e;
# #         border: 1px solid #fcd34d;
# #     }
# #     .persona-aesthetic {
# #         background: #d1fae5;
# #         color: #065f46;
# #         border: 1px solid #6ee7b7;
# #     }
# #     .rating-bar {
# #         height: 8px;
# #         border-radius: 4px;
# #         background: linear-gradient(90deg, #f43f5e, #fb923c, #facc15, #4ade80);
# #         margin-top: 4px;
# #     }
# #     .result-card {
# #         background: #fafafa;
# #         border: 1px solid #f0f0f0;
# #         border-radius: 12px;
# #         padding: 1.5rem;
# #         margin: 1rem 0;
# #     }
# #     .stButton > button {
# #         background: #1a1a1a;
# #         color: white;
# #         border: none;
# #         border-radius: 8px;
# #         padding: 0.6rem 2rem;
# #         font-family: 'DM Sans', sans-serif;
# #         font-size: 0.95rem;
# #         font-weight: 500;
# #         width: 100%;
# #         transition: all 0.2s;
# #     }
# #     .stButton > button:hover {
# #         background: #c0256f;
# #         transform: translateY(-1px);
# #     }
# # </style>
# # """, unsafe_allow_html=True)

# # # -------------------------------------------------------
# # # MongoDB
# # # -------------------------------------------------------
# # MONGO_URI = "mongodb+srv://fitcheck:fitcheck123@cluster0.ozebcow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# # @st.cache_resource
# # def get_mongo_client():
# #     return MongoClient(MONGO_URI)

# # client = get_mongo_client()
# # db = client["fitcheck_women"]
# # collection = db["outfit_critiques"]

# # # -------------------------------------------------------
# # # Header
# # # -------------------------------------------------------
# # st.markdown('<p class="main-title">👗 FitCheck.AI</p>', unsafe_allow_html=True)
# # st.markdown('<p class="subtitle">Your personal women\'s fashion critic — honest, savage, and always stylish.</p>', unsafe_allow_html=True)

# # # -------------------------------------------------------
# # # Style Persona Info
# # # -------------------------------------------------------
# # with st.expander("✨ About Style Personas"):
# #     col1, col2, col3 = st.columns(3)
# #     with col1:
# #         st.markdown("**⚡ Gen-Z**")
# #         st.caption("Y2K, streetwear, bold looks, cargo pants, chunky shoes, corsets")
# #     with col2:
# #         st.markdown("**✨ Millennial**")
# #         st.caption("Minimalist, tailored, neutral tones, smart casual, classic pieces")
# #     with col3:
# #         st.markdown("**🌿 Aesthetic**")
# #         st.caption("Cottagecore, dark academia, lace, floral, vintage, romantic")

# # st.divider()

# # # -------------------------------------------------------
# # # Upload Section
# # # -------------------------------------------------------
# # st.markdown("### Upload Your Outfit")
# # uploaded_file = st.file_uploader(
# #     "Upload a full outfit photo for critique",
# #     type=["jpg", "jpeg", "png", "webp"],
# #     help="For best results, use a full-body photo in good lighting"
# # )

# # if uploaded_file:
# #     image = Image.open(uploaded_file).convert("RGB")

# #     col1, col2 = st.columns([1, 1])
# #     with col1:
# #         st.image(image, caption="Your uploaded outfit", use_container_width=True)

# #     with col2:
# #         st.markdown("**Ready to get roasted?** 🔥")
# #         st.caption("Our AI will analyze your style, rate your outfit, and assign your style persona.")
# #         analyze_btn = st.button("✨ Analyze My Outfit")

# #     if analyze_btn:
# #         # Save image temporarily
# #         temp_path = os.path.join("Images", uploaded_file.name)
# #         os.makedirs("Images", exist_ok=True)
# #         with open(temp_path, "wb") as f:
# #             f.write(uploaded_file.getbuffer())

# #         # Deduplication
# #         phash = str(imagehash.phash(image))
# #         existing = collection.find_one({"image_id": phash})

# #         if existing:
# #             st.info("📁 We've seen this outfit before! Showing saved analysis.")
# #             critique = existing.get("raw_critique", "")
# #         else:
# #             with st.spinner("🔍 Analyzing your outfit... (30-60 seconds on CPU)"):
# #                 try:
# #                     critique = analyze_outfit_tool.invoke({"image_name": uploaded_file.name})

# #                     # Save to MongoDB
# #                     collection.insert_one({
# #                         "image_id": phash,
# #                         "filename": uploaded_file.name,
# #                         "raw_critique": critique,
# #                         "rating": extract_rating(critique),
# #                         "style": extract_style_paragraph(critique),
# #                         "comment": extract_comment(critique),
# #                         "persona": extract_persona(critique),
# #                         "timestamp": datetime.now(timezone.utc),
# #                     })
# #                 except Exception as e:
# #                     st.error(f"Error processing image: {e}")
# #                     critique = None

# #         # Display Results
# #         if critique:
# #             style   = extract_style_paragraph(critique)
# #             rating  = extract_rating(critique)
# #             comment = extract_comment(critique)
# #             persona = extract_persona(critique)

# #             st.divider()
# #             st.markdown("## Analysis Results")

# #             # Style Persona Badge
# #             persona_class = {
# #                 "Gen-Z": "persona-genz",
# #                 "Millennial": "persona-millennial",
# #                 "Aesthetic": "persona-aesthetic",
# #             }.get(persona, "persona-millennial")

# #             persona_emoji = {
# #                 "Gen-Z": "⚡",
# #                 "Millennial": "✨",
# #                 "Aesthetic": "🌿",
# #             }.get(persona, "✨")

# #             st.markdown(
# #                 f'<span class="persona-badge {persona_class}">'
# #                 f'{persona_emoji} {persona} Aesthetic'
# #                 f'</span>',
# #                 unsafe_allow_html=True
# #             )

# #             st.markdown("")

# #             # Style breakdown
# #             if style:
# #                 st.markdown("**Style Breakdown:**")
# #                 st.write(style)

# #             # Rating with visual bar
# #             if rating is not None:
# #                 score = int(rating * 100)
# #                 st.markdown(f"**Rating:** {score}/100")
# #                 st.progress(rating)

# #                 if score >= 80:
# #                     st.success("🏆 Elite look! Genuinely impressive.")
# #                 elif score >= 60:
# #                     st.info("👍 Solid outfit. A few tweaks and you're there.")
# #                 elif score >= 40:
# #                     st.warning("⚠️ Average. Try harder.")
# #                 else:
# #                     st.error("💀 This outfit needs serious help.")

# #             # Savage comment
# #             if comment:
# #                 st.markdown("**Verdict:**")
# #                 st.markdown(f"> *{comment}*")

# #             st.success(f"✅ Analysis saved to database")

# #         # Cleanup temp file
# #         if os.path.exists(temp_path):
# #             os.remove(temp_path)

# """
# Fashion AI Advisor.py — Women's AI Stylist
# Authentic luxury editorial fashion aesthetic.
# Outfit critique + style persona detection.
# """

# from PIL import Image
# import io
# import imagehash
# import streamlit as st
# from analyze_outfit import (
#     analyze_outfit_tool,
#     extract_comment,
#     extract_rating,
#     extract_style_paragraph,
#     extract_persona,
# )
# import dns
# from pymongo import MongoClient
# from datetime import datetime, timezone
# import os

# st.set_page_config(
#     page_title="FitCheck.AI — Women's Stylist",
#     page_icon="👗",
#     layout="centered"
# )

# # -------------------------------------------------------
# # Authentic Luxury Fashion CSS
# # Inspired by: Vogue, Net-a-Porter, The Row
# # Palette: Deep noir + champagne gold + blush rose
# # Font: Cormorant Garamond (editorial luxury) + Jost (clean modern)
# # -------------------------------------------------------
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');

#     /* ── Base ── */
#     html, body, [class*="css"] {
#         font-family: 'Jost', sans-serif;
#         font-weight: 300;
#         letter-spacing: 0.02em;
#     }

#     /* ── Hide Streamlit chrome ── */
#     #MainMenu, footer, header { visibility: hidden; }
#     .block-container { padding-top: 2rem; max-width: 780px; }

#     /* ── Masthead ── */
#     .masthead {
#         text-align: center;
#         padding: 3rem 0 1.5rem;
#         border-bottom: 1px solid rgba(212,175,55,0.25);
#         margin-bottom: 2.5rem;
#     }
#     .masthead-kicker {
#         font-family: 'Jost', sans-serif;
#         font-size: 0.65rem;
#         font-weight: 400;
#         letter-spacing: 0.35em;
#         text-transform: uppercase;
#         color: #D4AF37;
#         margin-bottom: 0.6rem;
#     }
#     .masthead-title {
#         font-family: 'Cormorant Garamond', serif;
#         font-size: 4rem;
#         font-weight: 300;
#         color: #f5f0eb;
#         line-height: 1;
#         letter-spacing: 0.08em;
#         margin: 0;
#     }
#     .masthead-title em {
#         font-style: italic;
#         color: #D4AF37;
#     }
#     .masthead-sub {
#         font-size: 0.72rem;
#         font-weight: 300;
#         letter-spacing: 0.2em;
#         text-transform: uppercase;
#         color: rgba(245,240,235,0.45);
#         margin-top: 0.8rem;
#     }

#     /* ── Section headings ── */
#     .section-label {
#         font-size: 0.62rem;
#         font-weight: 400;
#         letter-spacing: 0.3em;
#         text-transform: uppercase;
#         color: #D4AF37;
#         margin-bottom: 1rem;
#         display: flex;
#         align-items: center;
#         gap: 12px;
#     }
#     .section-label::after {
#         content: '';
#         flex: 1;
#         height: 1px;
#         background: rgba(212,175,55,0.2);
#     }

#     /* ── Persona accordion ── */
#     .persona-grid {
#         display: grid;
#         grid-template-columns: 1fr 1fr 1fr;
#         gap: 1px;
#         background: rgba(212,175,55,0.15);
#         border: 1px solid rgba(212,175,55,0.15);
#         margin-bottom: 2rem;
#     }
#     .persona-cell {
#         background: #0d0d0d;
#         padding: 1.2rem 1rem;
#     }
#     .persona-cell-label {
#         font-family: 'Cormorant Garamond', serif;
#         font-size: 1.1rem;
#         font-style: italic;
#         color: #f5f0eb;
#         margin-bottom: 0.3rem;
#     }
#     .persona-cell-desc {
#         font-size: 0.68rem;
#         font-weight: 300;
#         letter-spacing: 0.05em;
#         color: rgba(245,240,235,0.45);
#         line-height: 1.6;
#     }

#     /* ── Upload zone ── */
#     [data-testid="stFileUploader"] {
#         border: 1px solid rgba(212,175,55,0.2) !important;
#         border-radius: 0 !important;
#         padding: 1.5rem !important;
#         background: rgba(212,175,55,0.02) !important;
#         transition: border-color 0.3s !important;
#     }
#     [data-testid="stFileUploader"]:hover {
#         border-color: rgba(212,175,55,0.5) !important;
#     }

#     /* ── CTA Button ── */
#     .stButton > button {
#         background: transparent !important;
#         color: #D4AF37 !important;
#         border: 1px solid #D4AF37 !important;
#         border-radius: 0 !important;
#         padding: 0.75rem 2.5rem !important;
#         font-family: 'Jost', sans-serif !important;
#         font-size: 0.68rem !important;
#         font-weight: 400 !important;
#         letter-spacing: 0.3em !important;
#         text-transform: uppercase !important;
#         width: 100% !important;
#         transition: all 0.3s ease !important;
#     }
#     .stButton > button:hover {
#         background: #D4AF37 !important;
#         color: #0d0d0d !important;
#     }

#     /* ── Persona badge ── */
#     .persona-badge {
#         display: inline-flex;
#         align-items: center;
#         gap: 8px;
#         padding: 6px 20px;
#         border: 1px solid;
#         font-size: 0.65rem;
#         font-weight: 400;
#         letter-spacing: 0.25em;
#         text-transform: uppercase;
#         margin-bottom: 1.5rem;
#     }
#     .badge-genz {
#         border-color: #ff6b9d;
#         color: #ff6b9d;
#         background: rgba(255,107,157,0.05);
#     }
#     .badge-millennial {
#         border-color: #D4AF37;
#         color: #D4AF37;
#         background: rgba(212,175,55,0.05);
#     }
#     .badge-aesthetic {
#         border-color: #9caf88;
#         color: #9caf88;
#         background: rgba(156,175,136,0.05);
#     }

#     /* ── Results layout ── */
#     .result-divider {
#         border: none;
#         border-top: 1px solid rgba(212,175,55,0.15);
#         margin: 2rem 0;
#     }
#     .critique-text {
#         font-family: 'Cormorant Garamond', serif;
#         font-size: 1.05rem;
#         font-weight: 300;
#         font-style: italic;
#         color: rgba(245,240,235,0.8);
#         line-height: 1.8;
#         border-left: 2px solid rgba(212,175,55,0.3);
#         padding-left: 1.2rem;
#         margin: 1rem 0;
#     }
#     .verdict-text {
#         font-family: 'Cormorant Garamond', serif;
#         font-size: 1.15rem;
#         font-style: italic;
#         color: #D4AF37;
#         line-height: 1.7;
#     }

#     /* ── Score display ── */
#     .score-display {
#         display: flex;
#         align-items: baseline;
#         gap: 6px;
#         margin: 0.5rem 0;
#     }
#     .score-number {
#         font-family: 'Cormorant Garamond', serif;
#         font-size: 3.5rem;
#         font-weight: 300;
#         color: #D4AF37;
#         line-height: 1;
#     }
#     .score-denom {
#         font-size: 0.75rem;
#         color: rgba(245,240,235,0.3);
#         letter-spacing: 0.1em;
#     }

#     /* ── Rating bar ── */
#     .stProgress > div > div {
#         background: linear-gradient(90deg, #3d0000, #D4AF37, #f5f0eb) !important;
#         border-radius: 0 !important;
#         height: 3px !important;
#     }
#     .stProgress {
#         margin: 0.3rem 0 1.5rem !important;
#     }

#     /* ── Expander ── */
#     .streamlit-expanderHeader {
#         font-size: 0.7rem !important;
#         font-weight: 400 !important;
#         letter-spacing: 0.2em !important;
#         text-transform: uppercase !important;
#         color: rgba(245,240,235,0.5) !important;
#         background: transparent !important;
#         border-bottom: 1px solid rgba(212,175,55,0.1) !important;
#     }

#     /* ── Info/success/warning ── */
#     .stAlert {
#         border-radius: 0 !important;
#         border-left-width: 2px !important;
#     }

#     /* ── Image caption ── */
#     .stImage > figcaption {
#         font-size: 0.62rem !important;
#         letter-spacing: 0.15em !important;
#         text-transform: uppercase !important;
#         color: rgba(245,240,235,0.3) !important;
#         text-align: center !important;
#     }

#     /* ── Divider ── */
#     hr {
#         border-color: rgba(212,175,55,0.15) !important;
#     }
# </style>
# """, unsafe_allow_html=True)

# # -------------------------------------------------------
# # MongoDB
# # -------------------------------------------------------
# MONGO_URI = "mongodb+srv://fitcheck:fitcheck123@cluster0.ozebcow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# @st.cache_resource
# def get_mongo_client():
#     return MongoClient(MONGO_URI)

# client = get_mongo_client()
# db = client["fitcheck_women"]
# collection = db["outfit_critiques"]

# # -------------------------------------------------------
# # Masthead
# # -------------------------------------------------------
# st.markdown("""
# <div class="masthead">
#     <div class="masthead-kicker">AI · Fashion · Critique</div>
#     <h1 class="masthead-title">Fit<em>Check</em></h1>
#     <div class="masthead-sub">Your personal women's fashion critic — honest, savage, always stylish</div>
# </div>
# """, unsafe_allow_html=True)

# # -------------------------------------------------------
# # Style Persona Grid
# # -------------------------------------------------------
# with st.expander("STYLE PERSONAS — WHAT'S YOURS?"):
#     st.markdown("""
#     <div class="persona-grid">
#         <div class="persona-cell">
#             <div class="persona-cell-label">⚡ Gen-Z</div>
#             <div class="persona-cell-desc">Y2K revival · Streetwear · Cargo · Chunky shoes · Corsets · Bold graphics · Platform boots</div>
#         </div>
#         <div class="persona-cell">
#             <div class="persona-cell-label">✨ Millennial</div>
#             <div class="persona-cell-desc">Minimalist · Tailored · Silk blouses · Neutral tones · Structured bags · Classic silhouettes</div>
#         </div>
#         <div class="persona-cell">
#             <div class="persona-cell-label">🌿 Aesthetic</div>
#             <div class="persona-cell-desc">Cottagecore · Dark academia · Lace · Floral · Velvet · Prairie dresses · Romantic details</div>
#         </div>
#     </div>
#     """, unsafe_allow_html=True)

# st.markdown('<div class="section-label">Upload Your Outfit</div>', unsafe_allow_html=True)

# uploaded_file = st.file_uploader(
#     "Drop your outfit photo here — full body shots work best",
#     type=["jpg", "jpeg", "png", "webp"],
#     label_visibility="collapsed"
# )

# if uploaded_file:
#     image = Image.open(uploaded_file).convert("RGB")

#     col1, col2 = st.columns([1, 1], gap="large")
#     with col1:
#         st.image(image, caption="Your uploaded outfit", use_container_width=True)
#     with col2:
#         st.markdown("""
#         <div style="padding-top:1rem">
#             <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;
#                         font-style:italic;color:#f5f0eb;margin-bottom:0.5rem">
#                 Ready to be judged?
#             </div>
#             <div style="font-size:0.72rem;font-weight:300;letter-spacing:0.08em;
#                         color:rgba(245,240,235,0.45);line-height:1.8;margin-bottom:1.5rem">
#                 Our AI analyses silhouette, fabric, colour theory, and style persona.
#                 Zero tolerance for mediocrity.
#             </div>
#         </div>
#         """, unsafe_allow_html=True)
#         analyze_btn = st.button("Analyse My Outfit")

#     if analyze_btn:
#         temp_path = os.path.join("Images", uploaded_file.name)
#         os.makedirs("Images", exist_ok=True)
#         with open(temp_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         phash = str(imagehash.phash(image))
#         existing = collection.find_one({"image_id": phash})

#         if existing:
#             st.info("📁 Outfit recognised — showing saved critique.")
#             critique = existing.get("raw_critique", "")
#         else:
#             with st.spinner("Critiquing your outfit... (30–60 seconds)"):
#                 try:
#                     critique = analyze_outfit_tool.invoke({"image_name": uploaded_file.name})
#                     collection.insert_one({
#                         "image_id": phash,
#                         "filename": uploaded_file.name,
#                         "raw_critique": critique,
#                         "rating": extract_rating(critique),
#                         "style": extract_style_paragraph(critique),
#                         "comment": extract_comment(critique),
#                         "persona": extract_persona(critique),
#                         "timestamp": datetime.now(timezone.utc),
#                     })
#                 except Exception as e:
#                     st.error(f"Error: {e}")
#                     critique = None

#         if critique:
#             style   = extract_style_paragraph(critique)
#             rating  = extract_rating(critique)
#             comment = extract_comment(critique)
#             persona = extract_persona(critique)

#             st.markdown('<hr class="result-divider">', unsafe_allow_html=True)
#             st.markdown('<div class="section-label">The Verdict</div>', unsafe_allow_html=True)

#             # Persona badge
#             badge_class = {"Gen-Z":"badge-genz","Millennial":"badge-millennial","Aesthetic":"badge-aesthetic"}.get(persona,"badge-millennial")
#             badge_icon  = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"✨")
#             st.markdown(f'<span class="persona-badge {badge_class}">{badge_icon}&nbsp;&nbsp;{persona} Aesthetic</span>', unsafe_allow_html=True)

#             # Score
#             if rating is not None:
#                 score = int(rating * 100)
#                 st.markdown(f"""
#                 <div class="score-display">
#                     <span class="score-number">{score}</span>
#                     <span class="score-denom">/ 100</span>
#                 </div>
#                 """, unsafe_allow_html=True)
#                 st.progress(rating)

#                 if score >= 80:
#                     st.success("🏆 Elite. Genuinely impressive.")
#                 elif score >= 60:
#                     st.info("👍 Solid. A few refinements and you're there.")
#                 elif score >= 40:
#                     st.warning("⚠️ Average. The effort shows — barely.")
#                 else:
#                     st.error("💀 This needs serious help.")

#             # Style breakdown
#             if style:
#                 st.markdown('<div class="section-label" style="margin-top:1.5rem">Style Breakdown</div>', unsafe_allow_html=True)
#                 st.markdown(f'<div class="critique-text">{style}</div>', unsafe_allow_html=True)

#             # Savage comment
#             if comment:
#                 st.markdown('<div class="section-label" style="margin-top:1.5rem">Stylist\'s Note</div>', unsafe_allow_html=True)
#                 clean_comment = comment.replace("***","").replace("**","").replace("*","").strip().strip('"')
#                 st.markdown(f'<div class="verdict-text">"{clean_comment}"</div>', unsafe_allow_html=True)

#             st.markdown('<div style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(245,240,235,0.25);margin-top:2rem">✓ Critique saved to database</div>', unsafe_allow_html=True)

#         if os.path.exists(temp_path):
#             os.remove(temp_path)


"""
Fashion AI Advisor.py — Women's AI Stylist
Authentic luxury editorial fashion aesthetic.
Outfit critique + style persona detection.
"""

from PIL import Image
import io
import imagehash
import streamlit as st
from analyze_outfit import (
    analyze_outfit_tool,
    extract_comment,
    extract_rating,
    extract_style_paragraph,
    extract_persona,
)
import dns
from pymongo import MongoClient
from datetime import datetime, timezone
import os
import certifi
from pymongo.server_api import ServerApi

st.set_page_config(
    page_title="FitCheck.AI — Women's Stylist",
    page_icon="👗",
    layout="centered"
)

# -------------------------------------------------------
# Authentic Luxury Fashion CSS
# Inspired by: Vogue, Net-a-Porter, The Row
# Palette: Deep noir + champagne gold + blush rose
# Font: Cormorant Garamond (editorial luxury) + Jost (clean modern)
# -------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Jost:wght@200;300;400;500&display=swap');
    /* ── Base ── */
    html, body, [class*="css"] {
        font-family: 'Jost', sans-serif;
        font-weight: 300;
        letter-spacing: 0.02em;
    }
    /* ── Hide Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 2rem; max-width: 780px; }
    /* ── Masthead ── */
    .masthead {
        text-align: center;
        padding: 3rem 0 1.5rem;
        border-bottom: 1px solid rgba(212,175,55,0.25);
        margin-bottom: 2.5rem;
    }
    .masthead-kicker {
        font-family: 'Jost', sans-serif;
        font-size: 0.65rem;
        font-weight: 400;
        letter-spacing: 0.35em;
        text-transform: uppercase;
        color: #D4AF37;
        margin-bottom: 0.6rem;
    }
    .masthead-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4rem;
        font-weight: 300;
        color: #f5f0eb;
        line-height: 1;
        letter-spacing: 0.08em;
        margin: 0;
    }
    .masthead-title em {
        font-style: italic;
        color: #D4AF37;
    }
    .masthead-sub {
        font-size: 0.72rem;
        font-weight: 300;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: rgba(245,240,235,0.45);
        margin-top: 0.8rem;
    }
    /* ── Section headings ── */
    .section-label {
        font-size: 0.62rem;
        font-weight: 400;
        letter-spacing: 0.3em;
        text-transform: uppercase;
        color: #D4AF37;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: rgba(212,175,55,0.2);
    }
    /* ── Persona accordion ── */
    .persona-grid {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 1px;
        background: rgba(212,175,55,0.15);
        border: 1px solid rgba(212,175,55,0.15);
        margin-bottom: 2rem;
    }
    .persona-cell {
        background: #0d0d0d;
        padding: 1.2rem 1rem;
    }
    .persona-cell-label {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.1rem;
        font-style: italic;
        color: #f5f0eb;
        margin-bottom: 0.3rem;
    }
    .persona-cell-desc {
        font-size: 0.68rem;
        font-weight: 300;
        letter-spacing: 0.05em;
        color: rgba(245,240,235,0.45);
        line-height: 1.6;
    }
    /* ── Upload zone ── */
    [data-testid="stFileUploader"] {
        border: 1px solid rgba(212,175,55,0.2) !important;
        border-radius: 0 !important;
        padding: 1.5rem !important;
        background: rgba(212,175,55,0.02) !important;
        transition: border-color 0.3s !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: rgba(212,175,55,0.5) !important;
    }
    /* ── CTA Button ── */
    .stButton > button {
        background: transparent !important;
        color: #D4AF37 !important;
        border: 1px solid #D4AF37 !important;
        border-radius: 0 !important;
        padding: 0.75rem 2.5rem !important;
        font-family: 'Jost', sans-serif !important;
        font-size: 0.68rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.3em !important;
        text-transform: uppercase !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        background: #D4AF37 !important;
        color: #0d0d0d !important;
    }
    /* ── Persona badge ── */
    .persona-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 6px 20px;
        border: 1px solid;
        font-size: 0.65rem;
        font-weight: 400;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
    }
    .badge-genz {
        border-color: #ff6b9d;
        color: #ff6b9d;
        background: rgba(255,107,157,0.05);
    }
    .badge-millennial {
        border-color: #D4AF37;
        color: #D4AF37;
        background: rgba(212,175,55,0.05);
    }
    .badge-aesthetic {
        border-color: #9caf88;
        color: #9caf88;
        background: rgba(156,175,136,0.05);
    }
    /* ── Results layout ── */
    .result-divider {
        border: none;
        border-top: 1px solid rgba(212,175,55,0.15);
        margin: 2rem 0;
    }
    .critique-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.05rem;
        font-weight: 300;
        font-style: italic;
        color: rgba(245,240,235,0.8);
        line-height: 1.8;
        border-left: 2px solid rgba(212,175,55,0.3);
        padding-left: 1.2rem;
        margin: 1rem 0;
    }
    .verdict-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.15rem;
        font-style: italic;
        color: #D4AF37;
        line-height: 1.7;
    }
    /* ── Score display ── */
    .score-display {
        display: flex;
        align-items: baseline;
        gap: 6px;
        margin: 0.5rem 0;
    }
    .score-number {
        font-family: 'Cormorant Garamond', serif;
        font-size: 3.5rem;
        font-weight: 300;
        color: #D4AF37;
        line-height: 1;
    }
    .score-denom {
        font-size: 0.75rem;
        color: rgba(245,240,235,0.3);
        letter-spacing: 0.1em;
    }
    /* ── Rating bar ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, #3d0000, #D4AF37, #f5f0eb) !important;
        border-radius: 0 !important;
        height: 3px !important;
    }
    .stProgress {
        margin: 0.3rem 0 1.5rem !important;
    }
    /* ── Expander ── */
    .streamlit-expanderHeader {
        font-size: 0.7rem !important;
        font-weight: 400 !important;
        letter-spacing: 0.2em !important;
        text-transform: uppercase !important;
        color: rgba(245,240,235,0.5) !important;
        background: transparent !important;
        border-bottom: 1px solid rgba(212,175,55,0.1) !important;
    }
    /* ── Info/success/warning ── */
    .stAlert {
        border-radius: 0 !important;
        border-left-width: 2px !important;
    }
    /* ── Image caption ── */
    .stImage > figcaption {
        font-size: 0.62rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        color: rgba(245,240,235,0.3) !important;
        text-align: center !important;
    }
    /* ── Divider ── */
    hr {
        border-color: rgba(212,175,55,0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# MongoDB
# -------------------------------------------------------
MONGO_URI = "mongodb+srv://fitcheck:fitcheck123@cluster0.ozebcow.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

@st.cache_resource
def get_mongo_client():
    return MongoClient(
        MONGO_URI,
        server_api=ServerApi('1'),
        tls=True,
        tlsCAFile=certifi.where(),
        tlsAllowInvalidCertificates=True
    )

client = get_mongo_client()
db = client["fitcheck_women"]
collection = db["outfit_critiques"]

# -------------------------------------------------------
# Masthead
# -------------------------------------------------------
st.markdown("""
<div class="masthead">
    <div class="masthead-kicker">AI · Fashion · Critique</div>
    <h1 class="masthead-title">Fit<em>Check</em></h1>
    <div class="masthead-sub">Your personal women's fashion critic — honest, savage, always stylish</div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Style Persona Grid
# -------------------------------------------------------
with st.expander("STYLE PERSONAS — WHAT'S YOURS?"):
    st.markdown("""
    <div class="persona-grid">
        <div class="persona-cell">
            <div class="persona-cell-label">⚡ Gen-Z</div>
            <div class="persona-cell-desc">Y2K revival · Streetwear · Cargo · Chunky shoes · Corsets · Bold graphics · Platform boots</div>
        </div>
        <div class="persona-cell">
            <div class="persona-cell-label">✨ Millennial</div>
            <div class="persona-cell-desc">Minimalist · Tailored · Silk blouses · Neutral tones · Structured bags · Classic silhouettes</div>
        </div>
        <div class="persona-cell">
            <div class="persona-cell-label">🌿 Aesthetic</div>
            <div class="persona-cell-desc">Cottagecore · Dark academia · Lace · Floral · Velvet · Prairie dresses · Romantic details</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-label">Upload Your Outfit</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your outfit photo here — full body shots work best",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed"
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.image(image, caption="Your uploaded outfit", use_container_width=True)
    with col2:
        st.markdown("""
        <div style="padding-top:1rem">
            <div style="font-family:'Cormorant Garamond',serif;font-size:1.6rem;
                        font-style:italic;color:#f5f0eb;margin-bottom:0.5rem">
                Ready to be judged?
            </div>
            <div style="font-size:0.72rem;font-weight:300;letter-spacing:0.08em;
                        color:rgba(245,240,235,0.45);line-height:1.8;margin-bottom:1.5rem">
                Our AI analyses silhouette, fabric, colour theory, and style persona.
                Zero tolerance for mediocrity.
            </div>
        </div>
        """, unsafe_allow_html=True)
        analyze_btn = st.button("Analyse My Outfit")

    if analyze_btn:
        temp_path = os.path.join("Images", uploaded_file.name)
        os.makedirs("Images", exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        phash = str(imagehash.phash(image))
        existing = collection.find_one({"image_id": phash})

        if existing:
            st.info("📁 Outfit recognised — showing saved critique.")
            critique = existing.get("raw_critique", "")
        else:
            with st.spinner("Critiquing your outfit... (30–60 seconds)"):
                try:
                    critique = analyze_outfit_tool.invoke({"image_name": uploaded_file.name})
                    collection.insert_one({
                        "image_id": phash,
                        "filename": uploaded_file.name,
                        "raw_critique": critique,
                        "rating": extract_rating(critique),
                        "style": extract_style_paragraph(critique),
                        "comment": extract_comment(critique),
                        "persona": extract_persona(critique),
                        "timestamp": datetime.now(timezone.utc),
                    })
                except Exception as e:
                    st.error(f"Error: {e}")
                    critique = None

        if critique:
            style   = extract_style_paragraph(critique)
            rating  = extract_rating(critique)
            comment = extract_comment(critique)
            persona = extract_persona(critique)

            st.markdown('<hr class="result-divider">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">The Verdict</div>', unsafe_allow_html=True)

            # Persona badge
            badge_class = {"Gen-Z":"badge-genz","Millennial":"badge-millennial","Aesthetic":"badge-aesthetic"}.get(persona,"badge-millennial")
            badge_icon  = {"Gen-Z":"⚡","Millennial":"✨","Aesthetic":"🌿"}.get(persona,"✨")
            st.markdown(f'<span class="persona-badge {badge_class}">{badge_icon}&nbsp;&nbsp;{persona} Aesthetic</span>', unsafe_allow_html=True)

            # Score
            if rating is not None:
                score = int(rating * 100)
                st.markdown(f"""
                <div class="score-display">
                    <span class="score-number">{score}</span>
                    <span class="score-denom">/ 100</span>
                </div>
                """, unsafe_allow_html=True)
                st.progress(rating)

                if score >= 80:
                    st.success("🏆 Elite. Genuinely impressive.")
                elif score >= 60:
                    st.info("👍 Solid. A few refinements and you're there.")
                elif score >= 40:
                    st.warning("⚠️ Average. The effort shows — barely.")
                else:
                    st.error("💀 This needs serious help.")

            # Style breakdown
            if style:
                st.markdown('<div class="section-label" style="margin-top:1.5rem">Style Breakdown</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="critique-text">{style}</div>', unsafe_allow_html=True)

            # Savage comment
            if comment:
                st.markdown('<div class="section-label" style="margin-top:1.5rem">Stylist\'s Note</div>', unsafe_allow_html=True)
                clean_comment = comment.replace("***","").replace("**","").replace("*","").strip().strip('"')
                st.markdown(f'<div class="verdict-text">"{clean_comment}"</div>', unsafe_allow_html=True)

            st.markdown('<div style="font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;color:rgba(245,240,235,0.25);margin-top:2rem">✓ Critique saved to database</div>', unsafe_allow_html=True)

        if os.path.exists(temp_path):
            os.remove(temp_path)