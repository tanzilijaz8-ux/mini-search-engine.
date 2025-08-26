# 🔎 Mini Search (DuckDuckGo + Streamlit)

A deploy-ready, free search engine prototype using **DuckDuckGo Search** and **Streamlit**.
No API key needed.

## ✨ Features
- Web results (title, snippet, link, source host)
- Image results (grid with source links)
- Region, SafeSearch, time filter, and max results controls
- Caching for fast repeated queries (Streamlit `@st.cache_data`)

## 🧱 Tech
- Python, Streamlit
- [`duckduckgo-search`](https://pypi.org/project/duckduckgo-search/)

## 🚀 Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## ☁️ Deploy to Streamlit Cloud (Community)
1. Push these files to a public GitHub repo (root should have `app.py` and `requirements.txt`).
2. Go to https://share.streamlit.io/ and connect your repo.
3. Select branch and `app.py` as the entrypoint. Deploy!

## 🔧 Options
- **Region**: `wt-wt` (worldwide), `us-en`, `uk-en`, etc.
- **SafeSearch**: `off`, `moderate`, `strict`
- **Time limit**: `d`/`w`/`m`/`y` for results from last day/week/month/year.

## 📁 Project structure
```
.
├── app.py
├── requirements.txt
└── README.md
```

## ⚠️ Notes
- DuckDuckGo results are fetched via the `duckduckgo-search` library. It may have rate limits. If you hit errors, wait a bit and try again.
- This is a learning prototype (not Google-scale). You can extend it with your own crawler/indexer later.