import streamlit as st
import re
import random
import math
import arxiv
import google.generativeai as genai
from arxiv_api import arxiv_fetch
from ranker import update_liked, update_following
from LLM_utils import get_keyword, extract_title, get_score
from class_utils import *
import ast

st.set_page_config(page_title="PaperDance", layout="wide")

# Initialize session state
def init_state():
    defaults = {
        'keywords_selected': False,
        'selected_temp': [],
        'keyword_liked': [],
        'keyword_following': [],
        'paper_liked': [],
        'paper_disliked': [],
        'favorites': [],
        'his_rcm': [],
        'current_paper': None,
        'paper_index': 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
init_state()

# Recommendation engine choice
if 'ranker_choice' not in st.session_state:
    st.session_state['ranker_choice'] = 'LLM'
st.sidebar.header("Recommendation Engine")
st.sidebar.radio(
    "Select engine:",
    ["LLM", "Other"],
    key='ranker_choice'
)

# Configure LLM model (always needed)
genai.configure(api_key="Your-API-Key")
llm_model = genai.GenerativeModel("gemini-2.0-flash")
# Initialize BERT model for Other mode
bert_model = BertRanker()

# Styling
st.markdown(
    """
    <style>
    div.row-widget.stCheckbox input[type=checkbox] { position: absolute; opacity: 0; }
    div.row-widget.stCheckbox > label { display:inline-block; width:100%; padding:0.75em; border-radius:0.5em; text-align:center; cursor:pointer; border:1px solid #ccc; margin-bottom:0.5em; font-size:16px; }
    div.row-widget.stCheckbox:has(input[type=checkbox]:checked) > label { background-color:#4CAF50; color:white; border-color:#4CAF50; }
    .paper-title { font-size:24px; font-weight:bold; }
    .paper-authors { font-size:18px; margin-bottom:0.5em; }
    .paper-abstract { font-size:16px; margin-bottom:1em; }
    </style>
    """,
    unsafe_allow_html=True
)

available_keywords = [
    "Computer Vision", "Software Engineering", "Cybersecurity", "Computer Networks",
    "Database", "Operating System", "Artificial Intelligence", "Machine Learning",
    "Data Structure", "Algorithm"
]

def extract_arxiv_id(text: str) -> str:
    m = re.search(r"arXiv:(\d+\.\d+)", text)
    return m.group(1) if m else None

# Fetch functions
def fetch_latest_cs_papers(max_results=20):
    papers = []
    search = arxiv.Search(query="cat:cs.*", max_results=max_results, sort_by=arxiv.SortCriterion.SubmittedDate)
    for res in search.results():
        papers.append({
            'title': res.title,
            'authors': ", ".join(str(a) for a in res.authors),
            'abstract': f"Published: {res.published.date()}\n\n" + res.summary + f"\nLink: arXiv:{res.entry_id}"
        })
    return papers

def rm_paper_redundant(candidate, his):
    seen = set(his)
    candidate[:] = [p for p in candidate if extract_title(p) not in seen]

# Recommendation logic
def recommend(mode, keywords, his, refer=None):
    cand = []
    batch = random.sample(keywords, min(len(keywords), 5))
    for kw in batch:
        cand.extend(arxiv_fetch(kw, max_results=5))
    # dedupe
    cand = [dict(t) for t in {tuple(sorted(d.items())) for d in cand}]
    cand = [str(p) for p in cand]
    rm_paper_redundant(cand, his)

    # Choose scoring function and model
    use_bert = (st.session_state['ranker_choice'] == "Other")
    if use_bert:
        scorer = get_score_bert
        scorer_model = bert_model
    else:
        scorer = get_score
        scorer_model = llm_model

    if mode == 1 and refer and len(refer) > 5:
        score = scorer(scorer_model, refer, cand)
    elif mode in (1, 2):
        score = scorer(scorer_model, keywords, cand)
    else:
        return random.choice(cand) if cand else None

    top5 = sorted(score, key=lambda x: x[1] + math.sqrt(x[2]), reverse=True)[:5]
    pick = random.choices(top5, weights=[0.4, 0.25, 0.2, 0.1, 0.05], k=1)[0]
    return cand[pick[0]]

# Initial keyword selection UI
if not st.session_state['keywords_selected']:
    st.title("PaperDance")
    st.markdown("## Select Your Favorite Categories")
    cols = st.columns(5)
    for i, kw in enumerate(available_keywords):
        if cols[i % 5].button(kw):
            sel = st.session_state['selected_temp']
            if kw in sel:
                sel.remove(kw)
            else:
                sel.append(kw)
            st.session_state['selected_temp'] = sel
    st.write("Selected:", ", ".join(st.session_state['selected_temp']))
    if st.button("Confirm Selection"):
        if st.session_state['selected_temp']:
            seeds = st.session_state['selected_temp']
            st.session_state['keyword_liked'] = seeds.copy()
            st.session_state['keyword_following'] = seeds.copy()
            st.session_state['keywords_selected'] = True
        else:
            st.warning("Please select at least one category.")

# Main UI
options = ["Explore", "For You", "Following"]
ft = st.sidebar.radio("Mode", options)
mode = {"For You": 1, "Following": 2, "Explore": 3}[ft]
st.title("PaperDance")

# Fetch or recommend papers
papers = []
if mode == 3:
    papers = fetch_latest_cs_papers(20)
elif mode == 1:
    p = recommend(1, st.session_state['keyword_liked'], st.session_state['his_rcm'], st.session_state['paper_liked'])
    papers = [p] if p else []
    papers = [ast.literal_eval(p) for p in papers]
elif mode == 2:
    p = recommend(2, st.session_state['keyword_following'], st.session_state['his_rcm'])
    papers = [p] if p else []
    papers = [ast.literal_eval(p) for p in papers]

# Display paper and actions
if papers:
    idx = st.session_state['paper_index'] % len(papers)
    pap = papers[idx]
    st.markdown(f"<div class='paper-title'>{pap['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='paper-authors'>Authors: {pap['authors']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='paper-abstract'>{pap['abstract']}</div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("❤️ Favorite") and pap:
            if pap not in st.session_state['favorites']:
                st.session_state['favorites'].append(pap)
                # Always use LLM model for keyword update
                update_following(get_keyword(llm_model, [pap]), st.session_state['keyword_following'])
    with col2:
        if st.button("👍 Like") and pap:
            if pap not in st.session_state['paper_liked']:
                st.session_state['paper_liked'].append(pap)
                # Always use LLM model for keyword update
                update_liked(get_keyword(llm_model, [pap]), pap, st.session_state['keyword_liked'], st.session_state['paper_liked'])
            st.session_state['paper_index'] += 1
    with col3:
        if st.button("👎 Dislike") and pap:
            st.session_state['paper_disliked'].append(pap)
            st.session_state['paper_index'] += 1
    with col4:
        if st.button("⏭️ Next") and pap:
            st.session_state['paper_index'] += 1

# Sidebar favorites
with st.sidebar:
    st.header("Favorites 📚")
    if st.session_state['favorites']:
        for fav in st.session_state['favorites']:
            aid = extract_arxiv_id(fav['abstract'])
            if aid:
                st.markdown(f"- [{fav['title']}](https://arxiv.org/abs/{aid})")
            else:
                st.markdown(f"- {fav['title']}")
    else:
        st.info("No favorites yet.")
