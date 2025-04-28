# PaperDance
![image](https://github.com/user-attachments/assets/79772276-a417-4880-a94b-f2a2f9c27c77)

# PaperDance

**An interactive Streamlit app for personalized arXiv paper recommendations.**

---

## 🔍 Project Overview
**PaperDance** helps researchers discover computer science papers tailored to their interests. It supports two recommendation engines:

- **LLM (Gemini):** Scoring via Google Gemini generative model.
- **Other (BERT):** Scoring via a BertRanker implementation.

Key features:
- **Keyword-based seeding:** Users select favorite CS subfields (e.g., AI, Networking).
- **Modes:**
  - **Explore:** Fetches latest CS papers from arXiv.
  - **For You:** Personalized recommendations based on liked papers.
  - **Following:** Recommendations derived from followed keywords.
- **Interactive feedback:** ❤️ Favorite, 👍 Like, 👎 Dislike, ⏭️ Next.
- **Favorites sidebar:** Quick access to saved papers with direct arXiv links.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Pip or Conda package manager

### Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/PaperDance.git
   cd PaperDance
   ```
2. **Create & activate environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux/macOS
   venv\Scripts\activate       # Windows
   ```
3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Configuration

1. **arXiv API**
   - No key required; uses `arxiv` Python package.
2. **Google Gemini**
   - Obtain an API key and set in environment:
     ```bash
     export GENAI_API_KEY="YOUR_GOOGLE_GENAI_KEY"
     ```
   - Or hardcode in `app.py` (not recommended).

---

## 🛠️ Usage

```bash
streamlit run paperdance.py
```

1. **Select keywords** on first launch.
2. **Switch engine** in the sidebar: choose **LLM** or **Other**.
3. **Choose mode** (`Explore`, `For You`, `Following`).
4. **Interact** with paper cards using the four action buttons.
5. **View favorites** in the sidebar with clickable arXiv links.

---

## 🧩 Code Structure

```
├── app.py               # Main Streamlit application
├── arxiv_api.py         # Wrapper for arXiv fetch logic
├── ranker.py            # `update_liked` & `update_following` utilities
├── class_utils.py       # Data classes & helpers
├── LLM_utils.py         # `get_score`, `get_score_bert`, `get_keyword`, `extract_title` functions
├── requirements.txt     # Python dependencies
└── README.md            # This documentation
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m "Add new feature"`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

---

## 📄 License

MIT License © 2025 Your Name


