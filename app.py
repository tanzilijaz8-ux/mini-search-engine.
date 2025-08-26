import streamlit as st
from duckduckgo_search import DDGS
from urllib.parse import urlparse
from datetime import datetime
from typing import List, Dict, Any, Optional

st.set_page_config(
    page_title="Mini Search - DuckDuckGo",
    page_icon="🔎",
    layout="wide",
    menu_items={
        "Get help": "https://docs.streamlit.io/",
        "Report a bug": "https://github.com/",
        "About": "A minimal search engine UI powered by DuckDuckGo Search (no API key needed).",
    },
)

# ------------------ Utilities ------------------
def source_host(url: str) -> str:
    try:
        return urlparse(url).netloc.replace("www.", "")
    except Exception:
        return ""

@st.cache_data(show_spinner=False, ttl=300)
def ddg_text_search(query: str, max_results: int = 25, region: str = "wt-wt", safesearch: str = "moderate", timelimit: Optional[str] = None):
    with DDGS() as ddgs:
        results = list(ddgs.text(
            query,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            max_results=max_results
        ))
    return results

@st.cache_data(show_spinner=False, ttl=300)
def ddg_image_search(query: str, max_results: int = 30, region: str = "wt-wt", safesearch: str = "moderate", size=None, color=None, type_image=None, layout=None, license_image=None):
    with DDGS() as ddgs:
        results = list(ddgs.images(
            query,
            region=region,
            safesearch=safesearch,
            size=size,
            color=color,
            type_image=type_image,
            layout=layout,
            license_image=license_image,
            max_results=max_results
        ))
    return results

def render_result_card(item: Dict[str, Any]):
    title = item.get("title") or item.get("name") or "Untitled"
    href = item.get("href") or item.get("url") or "#"
    body = item.get("body") or item.get("snippet") or ""
    date = item.get("date") or item.get("published") or None
    host = source_host(href)
    with st.container(border=True):
        st.markdown(f"### [{title}]({href})")
        if host:
            st.caption(host)
        if body:
            st.write(body)
        if date:
            st.caption(f"Published: {date}")
        # Show raw dict in expander (debug/info)
        with st.expander("Details"):
            st.json(item)

def render_image_card(item: Dict[str, Any]):
    img_url = item.get("image")
    thumb = item.get("thumbnail")
    title = item.get("title") or ""
    source = item.get("source") or ""
    url = item.get("url") or ""
    with st.container(border=True):
        if thumb:
            st.image(thumb, use_container_width=True)
        elif img_url:
            st.image(img_url, use_container_width=True)
        if title:
            st.markdown(f"**{title}**")
        meta = " | ".join(x for x in [source, source_host(url)] if x)
        if meta:
            st.caption(meta)
        if url:
            st.markdown(f"[Open source page]({url})")
        with st.expander("Image JSON"):
            st.json(item)

# ------------------ Sidebar ------------------
st.sidebar.title("🔧 Settings")
st.sidebar.caption("DuckDuckGo powered search")
region = st.sidebar.selectbox("Region", ["wt-wt","us-en","uk-en","in-en","fr-fr","de-de","es-es","br-pt"], index=0, help="wt-wt = worldwide")
safesearch = st.sidebar.selectbox("SafeSearch", ["off","moderate","strict"], index=1)
max_results = st.sidebar.slider("Max results", min_value=5, max_value=100, value=30, step=5)
timelimit = st.sidebar.selectbox("Time limit", [None, "d", "w", "m", "y"], index=0, help="Filter by last Day/Week/Month/Year")
st.sidebar.divider()
st.sidebar.caption("Made with ❤️ using Streamlit")

# ------------------ Main ------------------
st.title("🔎 Mini Search")
st.write("Type anything to search the web (results by DuckDuckGo).")

query = st.text_input("Search the web", placeholder="e.g., best python tutorial", label_visibility="collapsed")

tabs = st.tabs(["Web", "Images"])

if query:
    with tabs[0]:
        with st.spinner("Searching the web…"):
            try:
                results = ddg_text_search(query, max_results=max_results, region=region, safesearch=safesearch, timelimit=timelimit)
            except Exception as e:
                st.error(f"Search error: {e}")
                results = []
        st.caption(f"Found {len(results)} results.")
        for item in results:
            render_result_card(item)

    with tabs[1]:
        with st.spinner("Fetching images…"):
            try:
                images = ddg_image_search(query, max_results=max_results, region=region, safesearch=safesearch)
            except Exception as e:
                st.error(f"Image search error: {e}")
                images = []
        cols = st.columns(3)
        for i, item in enumerate(images):
            with cols[i % 3]:
                render_image_card(item)
else:
    st.info("Enter a query above to start searching.")