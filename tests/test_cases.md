# 🧪 Test Cases — Skill Gap Analyzer

> **LearnDepth Track 1 | Project #58 | Anik Sarkar**

---

## 📋 Summary

| # | Test Scenario | CLI Mode | Expected Verdict | Result |
|---|---|---|---|---|
| 1 | Valid resume file + valid JD | Mode 1 — files | Partial fit | ✅ Pass |
| 2 | Manual skills via `--skills` flag | Mode 2 — skills | Partial fit | ✅ Pass |
| 3 | JD file not found | Mode 1 | Error message | ✅ Pass |
| 4 | Fully interactive, no flags | Mode 3 — interactive | Partial fit | ✅ Pass |
| 5 | All required skills provided | Mode 2 — skills | Good fit | ✅ Pass |
| 6 | Resume file not found | Mode 1 | Error message | ✅ Pass |
| 7 | All required, missing preferred | Mode 2 — skills | Good fit | ✅ Pass |
| 8 | All skills including preferred | Mode 2 — skills | Strong fit | ✅ Pass |

---

## 🔬 Detailed Test Cases

---

### ✅ Test Case #1 — Valid Resume File + Valid JD File

**📌 CLI Mode:** Mode 1 (file inputs)

**▶️ Command:**
```bash
uv run python src/main.py --resume data/resume.txt --jd data/job_description.txt
```

**📥 Input:**
- Resume: `data/resume.txt` — Michael Carter, skills: Java, Git, Docker, 3 years exp
- JD: `data/job_description.txt` — Senior Backend Engineer

**📤 Expected Output:**
- Matched skills listed with ✅
- Missing skills with correct priority labels (CRITICAL / IMPORTANT / NICE-TO-HAVE)
- Experience gap: "You have 3.0 yr(s). Role needs 4.0 yr(s). Gap: 1.0 yr(s)."
- Verdict: `Partial fit — missing 2 critical skill(s).`
- JSON report saved to `output/`

**🏁 Result:** ✅ Pass

---

### ✅ Test Case #2 — Skills Typed Manually via `--skills` Flag

**📌 CLI Mode:** Mode 2 (manual skills)

**▶️ Command:**
```bash
uv run python src/main.py --skills "Java, Git, Python" --jd data/job_description.txt
```

**📥 Input:**
- Skills typed: `Java, Git, Python`
- JD: `data/job_description.txt`

**📤 Expected Output:**
- Candidate name shown as `Unknown` (no resume, no name extractable)
- Matched skills: Java, Git
- Missing skills ranked by priority
- Report saved correctly

**🏁 Result:** ✅ Pass

---

### ✅ Test Case #3 — JD File Not Found

**📌 CLI Mode:** Mode 1

**▶️ Command:**
```bash
uv run python src/main.py --resume data/resume.txt --jd data/wrong_path.txt
```

**📥 Input:**
- JD path: `data/wrong_path.txt` ❌ (does not exist)

**📤 Expected Output:**
```
Error: File not found: data\wrong_path.txt
```
- ✅ Program exits cleanly — no crash, no traceback shown

**🏁 Result:** ✅ Pass

---

### ✅ Test Case #4 — Interactive Mode (No Flags)

**📌 CLI Mode:** Mode 3 (fully interactive)

**▶️ Command:**
```bash
uv run python src/main.py
```

**💬 Interaction:**
```
Enter path to JD file: data/job_description.txt
Enter resume file path OR type your skills manually: Java, Git, Docker
```

**📤 Expected Output:**
- Same quality output as Mode 1/2
- Handles both file path input and typed skills at the prompt

**🏁 Result:** ✅ Pass

---

### ✅ Test Case #5 — All Required Skills Provided

**📌 CLI Mode:** Mode 2

**▶️ Command:**
```bash
uv run python src/main.py --skills "Spring Boot, PostgreSQL, REST APIs, Docker, Git, Java" --jd data/job_description.txt
```

**📥 Input:**
- Candidate has all required skills in the JD
- Missing preferred skills: AWS, Kubernetes, Redis, Kafka

**📤 Expected Output:**
- All required skills appear under Matched Skills ✅
- Only NICE-TO-HAVE gaps remain
- Verdict: `Good fit — only minor gaps.`

**🏁 Result:** ✅ Pass

---

### ✅ Test Case #6 — Resume File Not Found

**📌 CLI Mode:** Mode 1

**▶️ Command:**
```bash
uv run python src/main.py --resume data/fake_resume.pdf --jd data/job_description.txt
```

**📥 Input:**
- Resume path: `data/fake_resume.pdf` ❌ (does not exist)

**📤 Expected Output:**
```
Error: File not found: data\fake_resume.pdf
```
- ✅ Program exits cleanly — no crash

**🏁 Result:** ✅ Pass

---

### ✅ Test Case #7 — Good Fit (Required Skills Met, Preferred Skills Missing)

**📌 CLI Mode:** Mode 2

**▶️ Command:**
```bash
uv run python src/main.py --skills "Spring Boot, PostgreSQL, REST APIs, Docker, Git, Java" --jd data/job_description.txt
```

**📥 Input:**
- All required skills provided ✅
- No preferred skills (AWS, Kubernetes, Redis, Kafka) ❌

**📤 Expected Output:**
- 0 CRITICAL gaps
- 0 IMPORTANT gaps
- 4 NICE-TO-HAVE gaps
- Verdict: `Good fit — only minor gaps.`

**🏁 Result:** ✅ Pass

---

### ✅ Test Case #8 — Strong Fit (Zero Gaps)

**📌 CLI Mode:** Mode 2

**▶️ Command:**
```bash
uv run python src/main.py --skills "Spring Boot, PostgreSQL, REST APIs, Docker, Git, Java, AWS, Kubernetes, Redis, Kafka" --jd data/job_description.txt
```

**📥 Input:**
- Candidate has every required AND preferred skill from the JD ✅

**📤 Expected Output:**
- All 10 skills matched ✅
- Missing Skills section: empty
- Verdict: `Strong fit — no skill gaps found.`

**🏁 Result:** ✅ Pass
