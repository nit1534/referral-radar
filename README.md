# 📡 Referral Radar

> **Stop cold-applying into the void.** Referral Radar helps job seekers identify the highest-value companies to target for referrals — ranked by data, not guesswork.

---

## The Problem

LinkedIn job applications submitted without a referral have a near-zero success rate. The bottleneck isn't your resume — it's visibility. A single internal referral can move your application from the rejection pile to the hiring manager's desk.

But who do you reach out to, and at which company?

## The Solution

Referral Radar analyzes a dataset of **123,849 real LinkedIn job postings** to surface the companies where your outreach will have the highest impact. It filters by your target role, scores each company using a custom **Referral Score**, and generates a personalized cold message — ready to send.

---

## How It Works

```
Input: Target job role (e.g. "Data Analyst")
         ↓
Filter 123,849 LinkedIn job postings by role
         ↓
Score each company using a custom Referral Score
         ↓
Output: Ranked Excel sheet + cold outreach message
```

### Referral Score Formula

Each company is ranked using a composite score based on three signals:

| Signal | Why It Matters |
|---|---|
| **Number of openings** | More roles = higher chance your referral contact can help |
| **Application competition ratio** | Fewer applicants per role = better odds |
| **Salary data** | Filters for roles worth pursuing |

---

## Getting Started

### Prerequisites

- Python 3.7+
- pip

### Installation

```bash
git clone https://github.com/your-username/referral-radar.git
cd referral-radar
pip install pandas openpyxl
```

### Run

```bash
python referral_radar.py
```

When prompted, enter your target job role (e.g. `Software Engineer`, `Product Manager`, `Data Analyst`).

---

## Output

The tool produces two outputs:

**1. `referral_targets.xlsx`** — A ranked list of companies with columns for openings, competition ratio, salary range, and Referral Score.

**2. Cold Outreach Message** — A personalized message template for the top-ranked company, printed to the console and ready to copy-paste into LinkedIn.


## Dataset

The analysis is based on a dataset of **123,849 LinkedIn job postings** containing role titles, company names, applicant counts, salary ranges, and posting metadata.

> **Note:** The dataset is not included in this repository due to size constraints. Place your dataset file in the project root and update the filename reference in `referral_radar.py` if needed.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Python** | Core logic and scripting |
| **Pandas** | Data filtering, aggregation, and scoring |
| **openpyxl** | Excel export |

---

## Project Structure

```
referral-radar/
├── referral_radar.py       # Main script
├── README.md
└── data/
    └── linkedin_jobs.csv   # Dataset (not included — see Dataset section)
