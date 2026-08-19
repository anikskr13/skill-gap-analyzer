# 📝 Project Report — Skill Gap Analyzer

> **LearnDepth Track 1 | Level 4 | Project #58**
> **Author:** Anik Sarkar
> **GitHub:** [skill-gap-analyzer](https://github.com/anikskr13/skill-gap-analyzer)

---

## 1. 🎯 Problem Understanding

Candidates preparing for job roles often struggle to identify which skills to focus on. Job descriptions vary widely in format — some list required vs preferred explicitly, others mix them together. Manual comparison is time-consuming and subjective.

**Core task from LearnDepth #58:**
> Compare candidate skills against role requirements and prioritize missing skills.
> Test case: `COMPARE Python, SQL vs ML Engineer`

**Key challenges identified:**
- Resumes and JDs have no fixed format — rule-based parsing breaks
- Skill matching must be case-insensitive and normalized
- Priority ranking must be deterministic and explainable, not a black box
- Output must be both human-readable (terminal) and machine-readable (JSON)

---

## 2. 🧩 Proposed Approach

Split the problem into two clear concerns:

| Concern | Solution |
|---|---|
| **Extraction** (unstructured text → structured data) | LLM via Groq API + Pydantic validation |
| **Analysis** (comparison + ranking) | Pure Python deterministic logic |

**Why this split?**
- LLMs handle any resume/JD format reliably — regex would break on varied headings
- Priority ranking stays transparent — every decision can be explained with a rule
- Pydantic v2 validates LLM output before it reaches the analyzer — no silent failures

---

## 3. 🔧 Implementation Details

### File Structure

```
src/
├── extractor.py   # Groq API calls + Pydantic models
├── analyzer.py    # Gap logic + priority ranking (no LLM)
├── storage.py     # Save/load reports as JSON
└── main.py        # CLI entry point (argparse, 3 modes)
```

### Pydantic Models

- `CandidateProfile` — name, skills, experience_years, education, projects, certifications
- `RoleRequirements` — role_name, required_skills, preferred_skills, min_experience, responsibilities
- `SkillGap` — skill_name, priority, reason
- `GapReport` — candidate_name, target_role, matched_skills, gaps, experience_gap, verdict

### Priority Ranking Logic (`analyzer.py`)

```python
def assign_priority(skill, required_skills, preferred_skills, jd_text):
    frequency = jd_text.lower().count(skill.lower())
    is_required = skill.lower() in [s.lower() for s in required_skills]
    is_preferred = skill.lower() in [s.lower() for s in preferred_skills]

    if is_required and frequency >= 2:   return "Critical"
    elif is_required and frequency < 2:  return "Important"
    elif is_preferred and frequency >= 2: return "Important"
    else:                                 return "Nice-to-have"
```

Two factors determine priority: **classification** (required vs preferred) and **frequency** (how often the skill appears in the JD).

### 3 CLI Modes

```bash
# Mode 1 — resume file + JD file
python src/main.py --resume data/resume.txt --jd data/job_description.txt

# Mode 2 — manual skills + JD file
python src/main.py --skills "Python, SQL" --jd data/job_description.txt

# Mode 3 — fully interactive
python src/main.py
```

### LLM Setup — Dual Client Architecture

The tool supports **two LLM backends**, switchable via a single flag:

| Backend | Client | Model | Use Case |
|---|---|---|---|
| ☁️ **Groq** (default) | `Groq()` | `openai/gpt-oss-120b` | Cloud, fast, free tier |
| 🦙 **Local** (optional) | `OpenAI(base_url=...)` | Any model loaded in LM Studio / Ollama | Offline, private, no API key needed |

```python
# In extractor.py — one toggle controls everything
USE_LOCAL_LLM = False   # flip to True for local mode
```

- **Output format:** `json_object` — forces structured JSON response from both backends
- **Temperature:** `0` — deterministic extraction, no creative variation
- **API key:** Groq key loaded from `.env` via `python-dotenv`; local server needs no real key

---

## 4. ⚙️ Important Technical Decisions

### ✅ LLM for extraction, NOT for ranking
Using LLM only for extraction (unstructured → structured) keeps the expensive, variable part isolated. Ranking uses deterministic Python logic — every skill's priority can be explained with a clear rule.

### ✅ Pydantic v2 for output validation
LLM output is parsed directly into Pydantic models. If the LLM returns unexpected fields or wrong types, Pydantic raises a validation error before it can break downstream logic. This acts as a contract between the LLM and the rest of the program.

### ✅ Skill normalization to lowercase
All skill matching converts both sides to `.lower()` before comparison. This prevents false negatives like `"Python"` not matching `"python"`.

### ✅ Reason string is human-readable, not LLM-generated
Each `SkillGap.reason` is built deterministically in Python:
```
"Required skill, mentioned 2x in JD."
```
This makes every output explainable without querying the LLM again.

### ✅ sys.stdout.reconfigure(encoding="utf-8")
Windows terminal defaults to cp1252 encoding, which can't render emojis (✅, ❌). Reconfiguring stdout to UTF-8 at startup fixes this cleanly without changing system settings.

---

## 5. 🧪 Testing Performed

8 test cases documented in `tests/test_cases.md`:

| # | Scenario | Result |
|---|---|---|
| 1 | Valid resume + valid JD | ✅ Pass |
| 2 | Manual `--skills` flag + JD | ✅ Pass |
| 3 | JD file path not found | ✅ Pass |
| 4 | Interactive mode (no flags) | ✅ Pass |
| 5 | All required skills provided | ✅ Pass |
| 6 | Resume file path not found | ✅ Pass |
| 7 | Good fit — only preferred skills missing | ✅ Pass |
| 8 | Strong fit — all skills including preferred matched | ✅ Pass |

**Verdict logic verified across 3 outcomes:**
- `Strong fit` — zero gaps
- `Good fit` — no critical gaps, only nice-to-have
- `Partial fit` — one or more critical gaps

---

## 6. ⚠️ Challenges Encountered

### 🔴 Windows terminal Unicode encoding error
Emoji characters (✅, ❌, —) caused `UnicodeEncodeError` on Windows because PowerShell uses cp1252 encoding by default.

### 🟠 Unused `openai` import causing ModuleNotFoundError
`extractor.py` had a leftover `from openai import OpenAI` import that was never used, causing an import error at runtime.

### 🟠 `generate_verdict` parameter bug
The parameter was incorrectly typed as `skill_gap: SkillGap` (a single object) instead of `gaps: list[SkillGap]`. The inner loop used `skill_gap.priority` instead of `g.priority`, which would have caused an AttributeError at runtime.

### 🟡 requirements.txt UTF-16 encoding
Running `uv pip freeze` on Windows generated a UTF-16 encoded file, which is unreadable on Linux/Mac without explicit encoding flags.

---

## 7. 🛠️ Solutions Implemented

| Challenge | Solution |
|---|---|
| Unicode encoding error | Added `sys.stdout.reconfigure(encoding="utf-8")` at top of `main.py` |
| Unused `openai` import | Removed the unused `from openai import OpenAI` line from `extractor.py` |
| `generate_verdict` bug | Fixed parameter name to `gaps: list[SkillGap]` and corrected inner loop to `g.priority` |
| UTF-16 requirements.txt | Regenerated with `uv pip freeze \| Out-File -Encoding utf8 requirements.txt` |

---

## 8. 🔮 Future Scope

| Improvement | Impact |
|---|---|
| 🌐 Web UI with Flask/FastAPI | Makes it accessible without CLI knowledge |
| 📚 Learning resource suggestions | Links courses to each missing skill automatically |
| 👥 Batch processing | Analyze multiple candidates against one JD |
| 🦙 Local LLM via Ollama | Fully offline use, no API dependency |
| 📄 PDF report export | Shareable, formatted output beyond JSON |
| 🔍 Fuzzy skill matching | "ML" matches "Machine Learning", "JS" matches "JavaScript" |

---

*LearnDepth Track 1 | #58 Skill Gap Analyzer | Anik Sarkar*
