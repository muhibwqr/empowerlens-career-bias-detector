# EmpowerLens - AI Career Bias Detector

> **Leveling the playing field, one job description at a time.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-green.svg)](https://flask.palletsprojects.com)

---

## About

**EmpowerLens** is an AI-powered web tool that scans job descriptions for gender-coded language, biased phrasing, and exclusionary patterns -- then provides actionable, inclusive rewrites. Research shows that masculine-coded words in job postings discourage women and underrepresented candidates from applying, even when they are fully qualified. EmpowerLens closes that gap.

Built for the **#75HER Challenge Hackathon 2026**, this project sits at the intersection of **Machine Learning/AI** and **Social Good** -- using NLP analysis and heuristic keyword detection to surface hidden bias in hiring pipelines.

---

## Features

- **Bias Detection Engine** -- scans for 100+ masculine-coded, feminine-coded, and exclusionary words
- **Bias Score** -- a 0-100 inclusivity score with color-coded feedback
- **Category Breakdown** -- separates findings into Masculine-Coded, Feminine-Coded, Jargon/Exclusionary, and Age-Biased categories
- **Inclusive Rewrites** -- suggests drop-in replacement phrases for every flagged term
- **OpenAI Enhancement** -- if an API key is present, GPT rewrites the entire JD inclusively
- **Clean UI** -- single-page Flask app, no JavaScript frameworks required

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.9+, Flask |
| NLP | Custom heuristics + optional OpenAI GPT-3.5/4 |
| Frontend | Jinja2 templates, inline HTML/CSS |
| Analysis | Regex, keyword matching, scoring algorithm |
| Deployment | Heroku / Railway / any Python host |

---

## Quick Start

### 1. Clone the repo
```bash
git clone https://github.com/muhibwqr/empowerlens-career-bias-detector.git
cd empowerlens-career-bias-detector
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Add OpenAI API key for GPT-powered rewrites
```bash
export OPENAI_API_KEY=sk-your-key-here
```

### 4. Run the app
```bash
python app.py
```

Visit **http://localhost:5000** in your browser.

---

## Demo

Paste any job description into the textarea. EmpowerLens will:
1. Highlight every biased term, color-coded by category
2. Display an **Inclusivity Score** (0 = very biased, 100 = fully inclusive)
3. Show **suggested replacements** for each flagged word
4. (With OpenAI key) Generate a fully rewritten, inclusive version of the JD

**Example input flagged terms:**
- `rockstar`, `ninja`, `dominate` -- masculine-coded aggression language
- `competitive` -- discourages collaborative-leaning applicants
- `digital native` -- age-biased
- `he/his` -- gendered pronoun assumption

---

## Project Structure

```
empowerlens-career-bias-detector/
├── app.py              # Flask app + bias detection engine + inline HTML
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── LICENSE             # MIT License
```

---

## Research Background

Studies by Gaucher, Friesen & Kay (2011) demonstrated that job ads with more masculine-coded words attract fewer female applicants. LinkedIn and Indeed have since rolled out bias-flagging tools internally -- EmpowerLens brings that same capability to anyone, for free.

---

## What's Next

- [ ] Chrome extension to analyze JDs inline on LinkedIn/Indeed
- [ ] API endpoint for ATS (Applicant Tracking System) integrations
- [ ] Multilingual bias detection (Spanish, French, German)
- [ ] Custom bias dictionaries per industry vertical
- [ ] Accessibility audit layer (reading level, jargon density)

---

## License

MIT 2026 EmpowerLens -- Built for the #75HER Challenge Hackathon
