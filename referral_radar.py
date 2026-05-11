import pandas as pd

df = pd.read_csv("postings.csv")

print(f" Loaded {len(df)} job postings\n")

def find_referral_targets(job_title, top_n=10):
    
    mask = df["title"].str.contains(job_title, case=False, na=False)
    filtered = df[mask].copy()
    
    print(f" Found {len(filtered)} '{job_title}' postings\n")
    
    if len(filtered) == 0:
        print("❌ No results. Try: 'Data Analyst', 'Machine Learning', 'AI Engineer'")
        return
    
    company_stats = filtered.groupby("company_name").agg(
        total_openings    = ("job_id",           "count"),
        avg_salary        = ("normalized_salary", "mean"),
        total_views       = ("views",             "sum"),
        total_applies     = ("applies",           "sum"),
        experience_levels = ("formatted_experience_level", 
                            lambda x: ", ".join(x.dropna().unique()[:2]))
    ).reset_index()

    # smarter referral score
    # views/applies ratio = how competitive the role is
    # lower competition = easier referral conversation
    company_stats["applies"] = company_stats["total_applies"].fillna(1)
    company_stats["views"]   = company_stats["total_views"].fillna(1)
    
    company_stats["competition_ratio"] = (
        company_stats["applies"] / company_stats["views"]
    )
    
    # score = more openings + lower competition + higher salary
    company_stats["raw_score"] = (
        company_stats["total_openings"]    * 2.0 +
        (1 - company_stats["competition_ratio"]) * 5.0 +
        company_stats["avg_salary"].fillna(0) / 50000
    )
    
    max_score = company_stats["raw_score"].max()
    company_stats["referral_score"] = (
        (company_stats["raw_score"] / max_score) * 10
    ).round(1)
    
    company_stats["avg_salary"] = company_stats["avg_salary"].apply(
        lambda x: f"${x:,.0f}" if pd.notna(x) and x > 0 else "Not disclosed"
    )
    
    top = company_stats.sort_values(
        "referral_score", ascending=False
    ).head(top_n)
    
    print(f" TOP {top_n} COMPANIES TO TARGET:\n")
    print(f"{'#':<4} {'Company':<32} {'Openings':<10} {'Experience':<25} {'Salary':<18} {'Score'}")
    print("-" * 100)
    
    for i, (_, row) in enumerate(top.iterrows(), 1):
        exp = row["experience_levels"] if row["experience_levels"] else "Not specified"
        print(f"{i:<4} {row['company_name']:<32} {int(row['total_openings']):<10} {exp:<25} {row['avg_salary']:<18} ⭐ {row['referral_score']}/10")
    
    # show competition insight
    print(f"\n COMPETITION INSIGHT:")
    print(f"   Lowest competition role: {top.iloc[-1]['company_name']}")
    print(f"   Highest paying role: ", end="")
    
    salary_df = company_stats[
        company_stats["avg_salary"] != "Not disclosed"
    ].copy()
    
    if len(salary_df) > 0:
        salary_df["salary_num"] = filtered.groupby("company_name")[
            "normalized_salary"
        ].mean().reindex(salary_df["company_name"]).values
        best_pay = salary_df.loc[salary_df["salary_num"].idxmax(), "company_name"]
        print(best_pay)
    else:
        print("Salary data not available")
    
    # generate message for top company
    print()
    generate_cold_message(job_title, top.iloc[0]["company_name"])
    
    # save to excel
    save_results(top, job_title)
    
    return top

def generate_cold_message(job_title, company):
    message = f"""
 COLD MESSAGE TEMPLATE:
{'='*55}
Hi [First Name],

I came across your profile and noticed you're a {job_title} 
at {company} — a role and company I'm genuinely excited about.

I'm currently building my data science skills through real 
projects (Python, ML, SQL) and would love to learn from 
someone already doing this work at {company}.

Would you be open to a quick 10-minute chat? I'd love to 
hear about your journey — and if you feel my profile is a 
fit, a referral would genuinely change my career trajectory.

Either way, thank you for your time!

[Your Name]
LinkedIn: [your URL]
GitHub:   [your URL]
{'='*55}
 TIPS TO GET A REPLY:
   1. Comment on one of their recent LinkedIn posts first
   2. Mention something SPECIFIC about their career path
   3. Send on Tuesday/Wednesday morning for best response rate
   4. Follow up once after 5 days if no reply
"""
    print(message)

def save_results(df, job_title):
    filename = f"referral_targets_{job_title.replace(' ','_')}.xlsx"
    df.to_excel(filename, index=False)
    print(f" Saved to {filename} — open it in Excel!")

if __name__ == "__main__":
    print("=" * 55)
    print("      REFERRAL RADAR v2.0 — Find Your In     ")
    print("=" * 55)
    
    job_title = input("\n Job title to search: ")
    top_n     = input(" Companies to show (default 10): ")
    top_n     = int(top_n) if top_n.strip().isdigit() else 10
    
    find_referral_targets(job_title, top_n)