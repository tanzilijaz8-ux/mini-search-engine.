import streamlit as st
from duckduckgo_search import DDGS
from urllib.parse import urlparse
from typing import List, Dict, Any, Optional

st.set_page_config(
    page_title="Tanzil Search",
    page_icon="🔎",
    layout="wide",
    menu_items={"About": "Tanzil Search – a mini, free search engine powered by DuckDuckGo."},
)

def host_from_url(url: str) -> str:
    try:
        netloc = urlparse(url).netloc
        return netloc.replace("www.", "")
    except Exception:
        return ""

def favicon_for(url: str) -> str:
    host = host_from_url(url)
    if not host:
        return ""
    return f"https://www.google.com/s2/favicons?sz=64&domain={host}"

def get_page_size() -> int:
    return st.session_state.get("page_size", 10)

def get_page() -> int:
    return st.session_state.get("page", 1)

def set_page(p: int):
    st.session_state["page"] = max(1, p)

def slice_page(items):
    size = get_page_size()
    p = get_page()
    start = (p - 1) * size
    end = start + size
    return items[start:end]

@st.cache_data(show_spinner=False, ttl=300)
def ddg_text(query: str, region="wt-wt", safesearch="moderate", timelimit=None, max_results=100):
    with DDGS() as d:
        return list(d.text(query, region=region, safesearch=safesearch, timelimit=timelimit, max_results=max_results))

@st.cache_data(show_spinner=False, ttl=300)
def ddg_images(query: str, region="wt-wt", safesearch="moderate", max_results=60):
    with DDGS() as d:
        return list(d.images(query, region=region, safesearch=safesearch, max_results=max_results))

@st.cache_data(show_spinner=False, ttl=300)
def ddg_news(query: str, region="wt-wt", safesearch="moderate", timelimit=None, max_results=50):
    with DDGS() as d:
        return list(d.news(query, region=region, safesearch=safesearch, timelimit=timelimit, max_results=max_results))

@st.cache_data(show_spinner=False, ttl=300)
def ddg_videos(query: str, region="wt-wt", safesearch="moderate", timelimit=None, max_results=50):
    with DDGS() as d:
        return list(d.videos(query, region=region, safesearch=safesearch, timelimit=timelimit, max_results=max_results))

def result_card(item):
    title = item.get("title") or item.get("name") or "Untitled"
    href = item.get("href") or item.get("url") or "#"
    body = item.get("body") or item.get("snippet") or ""
    date = item.get("date") or item.get("published") or ""
    host = host_from_url(href)
    fav = favicon_for(href)

    with st.container(border=True):
        cols = st.columns([0.12, 0.88])
        with cols[0]:
            if fav:
                st.image(fav, width=24)
            if host:
                st.caption(host)
        with cols[1]:
            st.markdown(f"### [{title}]({href})")
            if body:
                st.write(body)
            if date:
                st.caption(str(date))

def news_card(item):
    title = item.get("title") or "Untitled"
    url = item.get("url") or item.get("href") or "#"
    source = item.get("source") or ""
    date = item.get("date") or item.get("published") or ""
    snippet = item.get("body") or item.get("excerpt") or item.get("description") or ""
    host = host_from_url(url)
    fav = favicon_for(url)

    with st.container(border=True):
        cols = st.columns([0.12, 0.88])
        with cols[0]:
            if fav:
                st.image(fav, width=24)
            if source or host:
                st.caption(source or host)
        with cols[1]:
            st.markdown(f"### [{title}]({url})")
            if snippet:
                st.write(snippet)
            if date:
                st.caption(str(date))

def video_card(item):
    title = item.get("title") or "Untitled"
    url = item.get("content") or item.get("url") or "#"
    duration = item.get("duration") or ""
    publisher = item.get("publisher") or ""
    host = host_from_url(url)
    fav = favicon_for(url)

    with st.container(border=True):
        cols = st.columns([0.12, 0.88])
        with cols[0]:
            if fav:
                st.image(fav, width=24)
            if host:
                st.caption(host)
        with cols[1]:
            st.markdown(f"### [{title}]({url})")
            meta = " • ".join([x for x in [publisher, duration] if x])
            if meta:
                st.caption(meta)

def image_card(item):
    img = item.get("image") or item.get("thumbnail")
    title = item.get("title") or ""
    src = item.get("source") or ""
    url = item.get("url") or ""
    with st.container(border=True):
        if img:
            st.image(img, use_container_width=True)
        if title:
            st.markdown(f"**{title}**")
        meta = " | ".join([x for x in [src, host_from_url(url)] if x])
        if meta:
            st.caption(meta)
        if url:
            st.markdown(f"[Open source page]({url})")

st.sidebar.markdown("## 🔎 Tanzil Search")
st.sidebar.caption("DuckDuckGo powered • Private • Fast")

if "history" not in st.session_state:
    st.session_state.history = []

def add_history(q: str):
    if not q:
        return
    hist = [q] + [h for h in st.session_state.history if h != q]
    st.session_state.history = hist[:5]

region = st.sidebar.selectbox("Region", ["wt-wt","us-en","uk-en","in-en","fr-fr","de-de","es-es","br-pt"], index=0)
safesearch = st.sidebar.selectbox("SafeSearch", ["off","moderate","strict"], index=1)
timelimit = st.sidebar.selectbox("Time filter", [None, "d","w","m","y"], index=0)
page_size = st.sidebar.slider("Results per page", 5, 20, 10, 5)
st.session_state["page_size"] = page_size

st.sidebar.divider()
st.sidebar.subheader("Recent searches")
if st.session_state.history:
    for q in st.session_state.history:
        if st.sidebar.button(q, use_container_width=True):
            st.session_state["query"] = q
            set_page(1)
else:
    st.sidebar.caption("No searches yet.")

st.title("🔎 Tanzil Search")
st.caption("A sleek mini search engine – Web • Images • News • Videos")

q_default = st.session_state.get("query", "")
query = st.text_input("Search", value=q_default, placeholder="Type your query…", label_visibility="collapsed")
if query != q_default:
    set_page(1)
st.session_state["query"] = query

tabs = st.tabs(["Web", "Images", "News", "Videos"])

if query:
    add_history(query)
    with tabs[0]:
        with st.spinner("Searching the web…"):
            try:
                web_results = ddg_text(query, region=region, safesearch=safesearch, timelimit=timelimit, max_results=100)
            except Exception as e:
                st.error(f"Web search error: {e}")
                web_results = []
        total = len(web_results)
        st.caption(f"Found {total} results")
        page_items = slice_page(web_results)
        for item in page_items:
            result_card(item)
        cols = st.columns(3)
        with cols[0]:
            if st.button("⬅️ Prev", disabled=(get_page()==1)):
                set_page(get_page()-1)
        with cols[1]:
            st.markdown(f"**Page {get_page()}**")
        with cols[2]:
            if st.button("Next ➡️", disabled=(get_page()*get_page_size() >= total)):
                set_page(get_page()+1)

    with tabs[1]:
        with st.spinner("Fetching images…"):
            try:
                img_results = ddg_images(query, region=region, safesearch=safesearch, max_results=60)
            except Exception as e:
                st.error(f"Image search error: {e}")
                img_results = []
        st.caption(f"Found {len(img_results)} images")
        cols = st.columns(3)
        for i, item in enumerate(img_results):
            with cols[i % 3]:
                image_card(item)

    with tabs[2]:
        with st.spinner("Fetching news…"):
            try:
                news_results = ddg_news(query, region=region, safesearch=safesearch, timelimit=timelimit, max_results=50)
            except Exception as e:
                st.error(f"News error: {e}")
                news_results = []
        total = len(news_results)
        st.caption(f"Found {total} news articles")
        page_items = slice_page(news_results)
        for item in page_items:
            news_card(item)
        cols = st.columns(3)
        with cols[0]:
            if st.button("⬅️ Prev news", key="prev_news", disabled=(get_page()==1)):
                set_page(get_page()-1)
        with cols[1]:
            st.markdown(f"**Page {get_page()}**")
        with cols[2]:
            if st.button("Next news ➡️", key="next_news", disabled=(get_page()*get_page_size() >= total)):
                set_page(get_page()+1)

    with tabs[3]:
        with st.spinner("Fetching videos…"):
            try:
                vid_results = ddg_videos(query, region=region, safesearch=safesearch, timelimit=timelimit, max_results=50)
            except Exception as e:
                st.error(f"Videos error: {e}")
                vid_results = []
        total = len(vid_results)
        st.caption(f"Found {total} videos")
        page_items = slice_page(vid_results)
        for item in page_items:
            video_card(item)
        cols = st.columns(3)
        with cols[0]:
            if st.button("⬅️ Prev videos", key="prev_videos", disabled=(get_page()==1)):
                set_page(get_page()-1)
        with cols[1]:
            st.markdown(f"**Page {get_page()}**")
        with cols[2]:
            if st.button("Next videos ➡️", key="next_videos", disabled=(get_page()*get_page_size() >= total)):
                set_page(get_page()+1)
else:
    st.info("Type a query to start searching.")