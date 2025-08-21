import csv
import os

SYNONYMS = {
    "ml": ["machine learning", "ai", "ml"],
    "excel": ["spreadsheet", "ms excel", "excel"],
    "python": ["py", "python3", "python"],
    "javascript": ["js", "javascript"],
    "sql": ["postgres", "mysql", "sqlite", "sql"],
}

def tokenize_csv_field(text):
    return [t.strip().lower() for t in text.split(',') if t.strip()]

def normalize(text):
    tokens = []
    for raw in text.lower().replace('\n', ' ').replace(',', ' ').split():
        t = raw.strip()
        if not t:
            continue
        tokens.append(t)
        for key, syns in SYNONYMS.items():
            if t in syns:
                tokens.append(key)
    return set(tokens)

def load_dataset(path=os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'careers.csv')):
    roles = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row['skills'] = tokenize_csv_field(row['skills'])
            row['interests'] = tokenize_csv_field(row['interests'])
            row['style'] = tokenize_csv_field(row['style'])
            roles.append(row)
    return roles

def match_details(profile_tokens, role):
    reasons = []
    for skill in role['skills']:
        if skill in profile_tokens:
            reasons.append(f"Matched skill: {skill}")
    for intr in role['interests']:
        if intr in profile_tokens:
            reasons.append(f"Matched interest: {intr}")
    for st in role['style']:
        if st in profile_tokens:
            reasons.append(f"Matched style: {st}")
    return reasons[:2]

def score_role(profile_tokens, role):
    score = 0
    for skill in role['skills']:
        if skill in profile_tokens:
            score += 2
    for intr in role['interests']:
        if intr in profile_tokens:
            score += 1
    for st in role['style']:
        if st in profile_tokens:
            score += 1
    return score

def recommend(user_text, profile=None):
    if not (user_text or profile):
        return []

    profile_text = (user_text or '')
    if profile:
        profile_text += ' ' + ' '.join(profile.values())

    tokens = normalize(profile_text)
    roles = load_dataset()

    scored = []
    for r in roles:
        s = score_role(tokens, r)
        if s > 0:
            reasons = match_details(tokens, r)
            scored.append((s, r, reasons))

    scored.sort(key=lambda x: x[0], reverse=True)
    top5 = scored[:5]

    results = []
    for score, role, reasons in top5:
        results.append({
            'role': role['role'],
            'score': score,
            'description': role['description'],
            'resources': role['resources'],
            'roadmap': role.get('roadmap', ''),
            'reasons': reasons
        })
    return results
