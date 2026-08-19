# 🔍 Skill Gap Analyzer

> **Give it your resume and a job description — it tells you exactly what skills you're missing, how critical each gap is, and what to learn first.**

---

## 🧠 What It Does

Skill Gap Analyzer compares a candidate's skills against a job description and produces a **prioritized skill gap report** — no guesswork, no black boxes.

| Input | Output |
|---|---|
| 📄 Resume (PDF / DOCX / TXT) or typed skills | ✅ Matched skills |
| 📋 Job Description file | ❌ Missing skills ranked by priority |
| | 📊 Experience gap analysis |
| | 🧾 Verdict + saved JSON report |

---

## ❗ Problem Statement

Candidates often don't know which skills to focus on when preparing for a role.  
This tool solves that by comparing your skills against a JD and ranking every missing skill — so you always know **what to learn first**.

---

## ✨ Features

- 🖥️ **3 input modes** — resume file, manual skill input, or fully interactive
- 🤖 **LLM-powered extraction** — handles any resume or JD format
- ☁️ **Cloud + Local LLM support** — Groq API (default) or local models via LM Studio / Ollama
- 🧮 **Rule-based priority ranking** — transparent, explainable logic (not a black box)
- 📉 **Experience gap detection** — compares candidate experience against role minimum
- 💾 **JSON report output** — every report saved to `output/` automatically
- 🎨 **Clean terminal output** — formatted report with emojis and clear layout

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| 🐍 Python 3.11+ | Core language |
| ⚡ Groq API | Cloud LLM extraction (free tier, default) |
| 🦙 LM Studio / Ollama | Local LLM extraction (optional, offline) |
| ✅ Pydantic v2 | Structured output validation |
| 📄 pdfplumber | Read PDF resumes |
| 📝 python-docx | Read DOCX resumes |
| 🔐 python-dotenv | Load API key from `.env` |
| ⚙️ argparse | CLI argument parsing |

---

## 📁 Project Structure

```
skill_gap_analyzer/
├── src/
│   ├── main.py          # CLI entry point — orchestrates everything
│   ├── extractor.py     # LLM calls + Pydantic models + dual client setup
│   ├── analyzer.py      # Gap comparison + priority ranking (no LLM)
│   └── storage.py       # Save/load reports as JSON
├── data/
│   ├── resume.txt           # Sample resume
│   └── job_description.txt  # Sample job description
├── output/              # Generated JSON reports (auto-created)
├── tests/
│   └── test_cases.md    # Documented test cases
├── screenshots/         # Terminal output screenshots
├── .env                 # API key (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

**1️⃣ Clone the repo:**
```bash
git clone https://github.com/anikskr13/skill-gap-analyzer.git
cd skill_gap_analyzer
```

**2️⃣ Install dependencies:**
```bash
pip install -r requirements.txt
```
> Or with `uv`: `uv sync`

**3️⃣ Set up your API key:**

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```
> 🔑 Get a free API key at [console.groq.com](https://console.groq.com)

---

## 🚀 How to Run

### Mode 1 — Resume file + JD file
```bash
uv run python src/main.py --resume data/resume.txt --jd data/job_description.txt
```

### Mode 2 — Type skills manually + JD file
```bash
uv run python src/main.py --skills "Python, SQL, REST APIs" --jd data/job_description.txt
```

### Mode 3 — Fully interactive (no flags)
```bash
uv run python src/main.py
```
> The tool will prompt you to enter paths or type skills directly.

---

## 🦙 Local LLM Support (Offline Mode)

By default, the tool uses **Groq API** (cloud). But you can switch to a **local LLM** for fully offline, private usage — no API key needed.

### Supported local servers:

| Server | Default URL | Setup |
|---|---|---|
| 🖥️ [LM Studio](https://lmstudio.ai/) | `http://localhost:1234/v1` | Download → load a model → start server |
| 🦙 [Ollama](https://ollama.ai/) | `http://localhost:11434/v1` | `ollama run gemma2` → server starts automatically |

### How to switch:

Open `src/extractor.py` and flip the toggle:

```python
# =================================================================
# TOGGLE — flip to True to use local LLM instead of Groq
USE_LOCAL_LLM = True    # ← change False to True
# =================================================================
```

To change the local model or server URL, edit these lines in `extractor.py`:

```python
# --- Local LLM (LM Studio / Ollama) ---
client_local = OpenAI(
    base_url="http://localhost:1234/v1",   # ← change URL for Ollama
    api_key="anything"
)
local_model = "google/gemma-4-e2b"         # ← change to your loaded model
```

> ⚠️ **Note:** Local LLM quality depends on the model you load. Larger models (7B+) give better extraction results. The tool still works the same way — only the extraction backend changes.

---

## 📊 Sample Output

```
============================================
         SKILL GAP ANALYSIS REPORT
============================================
Candidate  : Michael Carter
Target Role: Senior Backend Engineer

Matched Skills:
  ✅ Java
  ✅ Git
  ✅ Docker

Missing Skills:
  ❌ [CRITICAL]      Spring Boot — Required skill, mentioned 2x in JD.
  ❌ [CRITICAL]      PostgreSQL  — Required skill, mentioned 2x in JD.
  ❌ [IMPORTANT]     REST APIs   — Required skill, mentioned 1x in JD.
  ❌ [NICE-TO-HAVE]  AWS         — Preferred skill, mentioned 1x in JD.

Experience Gap : You have 3.0 yr(s). Role needs 4.0 yr(s). Gap: 1.0 yr(s).
Verdict        : Partial fit — missing 2 critical skill(s).
============================================
```

> 💾 JSON report auto-saved to `output/Michael_Carter_Senior_Backend_Engineer.json`

---

## 🎯 Priority Ranking Logic

Priority is assigned using **pure Python logic** — no LLM involved:

| Priority | Condition |
|---|---|
| 🔴 **Critical** | Required skill + mentioned ≥ 2x in JD |
| 🟠 **Important** | Required skill + mentioned < 2x in JD |
| 🟠 **Important** | Preferred skill + mentioned ≥ 2x in JD |
| 🟡 **Nice-to-have** | Preferred skill + mentioned < 2x in JD |

> Every priority decision is transparent and explainable — no black box.

---

## 🧪 Testing

8 test cases documented in [`tests/test_cases.md`](tests/test_cases.md), covering:

- ✅ Valid resume + JD (full report generation)
- ✅ Manual skill input via `--skills`
- ✅ JD file not found (error handling)
- ✅ Interactive mode (no flags)
- ✅ All required skills matched (Good fit)
- ✅ Resume file not found (error handling)
- ✅ Good fit — no critical gaps
- ✅ Strong fit — zero gaps at all

---

## ⚠️ Limitations

- 🌐 Cloud mode depends on Groq API availability
- 🦙 Local mode quality depends on the model loaded
- 🔤 Skill matching is exact — no fuzzy matching (e.g. "ML" won't match "Machine Learning")
- 🖼️ Does not handle image-based / scanned PDFs
- 🖥️ CLI only — no GUI
- 🤖 Extraction quality depends on LLM output

---

## 🔮 Future Improvements

| Improvement | Impact |
|---|---|
| 🌐 Web UI with Flask/FastAPI | Accessible without CLI knowledge |
| 📚 Learning resource suggestions | Auto-link courses to each missing skill |
| 👥 Batch processing | Analyze multiple candidates against one JD |
| 📄 PDF report export | Shareable, formatted output beyond JSON |
| 🔍 Fuzzy skill matching | "ML" ↔ "Machine Learning", "JS" ↔ "JavaScript" |
| 🔄 CLI flag for LLM toggle | `--local` flag instead of editing code |

---

## 👤 Author

**Anik Sarkar** — LearnDepth Track 1 | Project #58

📂 GitHub: [skill-gap-analyzer](https://github.com/anikskr13/skill-gap-analyzer)
