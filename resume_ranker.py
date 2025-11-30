import re

# ---------------------------------------------
# 1. STOPWORDS (remove useless common words)
# ---------------------------------------------
STOPWORDS = {
    "and","or","but","the","a","an","is","are","was","were","with","for","to","in",
    "on","of","also","apply","can","this","that","as","be","have","has","had","by",
    "from","at","it","its","you","your","their","they","we","our","i"
}


# ----------------------------------------------------
# 2. TECH SKILLS DICTIONARY (expand anytime you want)
# ----------------------------------------------------
TECH_KEYWORDS = {
    # Languages
    "python","java","javascript","typescript","c","c++","c#","go","rust","kotlin",
    "swift","php","ruby",

    # Web Dev
    "html","css","react","node","express","django","flask","fastapi","angular",
    "bootstrap","nextjs","rest","api","apis","json","xml",

    # Databases
    "sql","mysql","postgres","mongodb","redis","sqlite","nosql",

    # Cloud
    "aws","azure","gcp","cloud","lambda","docker","kubernetes","k8s","devops",
    "ci","cd","jenkins",

    # ML & AI
    "ml","ai","machine","learning","deep","neural","model","models","training",
    "testing","data","nlp","opencv","pandas","numpy","sklearn","tensorflow",
    "pytorch",

    # Backend
    "backend","frontend","fullstack","microservices","authentication",
    "authorization","jwt"
}


# ----------------------------------------------------
# Clean Text
# ----------------------------------------------------
def clean_text(text):
    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ----------------------------------------------------
# Extract Meaningful Keywords
# ----------------------------------------------------
def extract_keywords(text):
    words = text.split()
    keywords = set()

    for w in words:
        w = w.strip()

        # skip small words
        if len(w) < 3:
            continue

        # skip stopwords
        if w in STOPWORDS:
            continue

        # keep only real tech terms
        if w in TECH_KEYWORDS:
            keywords.add(w)

    return keywords


# ----------------------------------------------------
# Skill Match Score
# ----------------------------------------------------
def skill_match_score(job_keywords, resume_keywords):
    matched = job_keywords.intersection(resume_keywords)
    missing = job_keywords - resume_keywords

    score = (len(matched) / len(job_keywords)) * 100 if len(job_keywords) > 0 else 0

    return score, matched, missing


# ----------------------------------------------------
# Recommendation
# ----------------------------------------------------
def get_recommendation(score):
    if score >= 85:
        return "Strong fit"
    elif score >= 60:
        return "Good fit"
    elif score >= 40:
        return "Possible fit"
    else:
        return "Not a fit"


# ----------------------------------------------------
# Rank Resume (MAIN FUNCTION)
# ----------------------------------------------------
def rank_resume(resume_text, job_description):

    job_clean = clean_text(job_description)
    resume_clean = clean_text(resume_text)

    job_keywords = extract_keywords(job_clean)
    resume_keywords = extract_keywords(resume_clean)

    score, matched, missing = skill_match_score(job_keywords, resume_keywords)

    explanation = (
        f"The resume matches {len(matched)} out of {len(job_keywords)} "
        f"important technical skills from the job description."
    )

    return {
        "score": round(score, 2),
        "strengths": sorted(list(matched))[:10],
        "gaps": sorted(list(missing))[:10],
        "explanation": explanation,
        "recommendation": get_recommendation(score),
    }