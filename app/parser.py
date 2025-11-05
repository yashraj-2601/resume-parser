import re
import pdfplumber
import spacy
from typing import Dict, List, Tuple
from .utils import COMMON_SKILLS, DEGREE_PATTERNS

_nlp = spacy.load("en_core_web_sm")

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\\+?\\d{1,3}[ -]?)?(?:\\(?\\d{3}\\)?[ -]?\\d{3}[ -]?\\d{4})")
DEGREE_RE = re.compile("|".join(DEGREE_PATTERNS), re.IGNORECASE)

def extract_text_from_pdf(file_path: str) -> str:
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def extract_name(doc: spacy.tokens.Doc) -> str | None:
    lines = [l.strip() for l in doc.text.split("\n") if l.strip()][:10]
    head_text = "\n".join(lines)
    head_doc = _nlp(head_text)
    for ent in head_doc.ents:
        if ent.label_ == "PERSON" and 2 <= len(ent.text.split()) <= 4:
            return ent.text
    for l in lines:
        tokens = l.split()
        caps = [t for t in tokens if t[:1].isupper()]
        if 2 <= len(caps) <= 4:
            return " ".join(tokens[:len(caps)])
    return None

def extract_email_phone(text: str) -> Tuple[str | None, str | None]:
    email = EMAIL_RE.search(text)
    phone = PHONE_RE.search(text)
    return (email.group(0) if email else None, phone.group(0) if phone else None)

def extract_skills(text: str) -> List[str]:
    low = text.lower()
    return sorted({s for s in COMMON_SKILLS if s in low})

def extract_education(text: str) -> List[str]:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    return [l for l in lines if DEGREE_RE.search(l)]

def estimate_experience_years(text: str) -> float | None:
    matches = re.findall(r"(\\d+(?:\\.\\d+)?)\\s+years?", text.lower())
    if not matches:
        return None
    return max(float(m) for m in matches)

def parse_pdf_to_dict(file_path: str) -> Dict:
    text = extract_text_from_pdf(file_path)
    doc = _nlp(text)
    name = extract_name(doc)
    email, phone = extract_email_phone(text)
    skills = extract_skills(text)
    education = extract_education(text)
    exp = estimate_experience_years(text)
    return {
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience_years": exp,
    }
