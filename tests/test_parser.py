from app.parser import extract_email_phone, extract_skills, estimate_experience_years

def test_email_phone():
    text = "John Doe\nEmail: john@example.com\nPhone: +1 555-123-4567"
    email, phone = extract_email_phone(text)
    assert email == "john@example.com"
    assert "555" in phone

def test_skills():
    text = "Experienced with Python, Flask, Docker, and Kubernetes."
    skills = extract_skills(text)
    assert set(["python", "flask", "docker", "kubernetes"]).issubset(set(skills))

def test_exp_years():
    text = "I have 1.5 years at X and 3 years at Y."
    exp = estimate_experience_years(text)
    assert exp == 3.0
