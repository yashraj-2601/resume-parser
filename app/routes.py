import os
import tempfile
from flask import Blueprint, request, jsonify, abort
from sqlalchemy import select
from .database import get_session
from .models import Candidate
from .parser import parse_pdf_to_dict

api_bp = Blueprint("api", __name__)

@api_bp.post("/parse")
def parse_resume():
    if "file" not in request.files:
        abort(400, "file is required")
    f = request.files["file"]
    if not f.filename.lower().endswith(".pdf"):
        abort(400, "only PDF supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        f.save(tmp.name)
        data = parse_pdf_to_dict(tmp.name)
    os.unlink(tmp.name)

    sess = get_session()
    candidate = Candidate(
        name=data.get("name"),
        email=data.get("email"),
        phone=data.get("phone"),
        skills=",".join(data.get("skills", [])) or None,
        education="\n".join(data.get("education", [])) or None,
        experience_years=data.get("experience_years"),
        source_filename=f.filename,
    )
    sess.add(candidate)
    sess.commit()
    return jsonify(candidate.to_dict()), 201

@api_bp.get("/candidates")
def list_candidates():
    skill = request.args.get("skill")
    degree = request.args.get("degree")
    min_exp = request.args.get("min_exp", type=float)

    sess = get_session()
    rows = sess.execute(select(Candidate)).scalars().all()

    def match(c: Candidate):
        if skill and skill.lower() not in (c.skills or "").lower():
            return False
        if degree and degree.lower() not in (c.education or "").lower():
            return False
        if min_exp and (not c.experience_years or c.experience_years < min_exp):
            return False
        return True

    return jsonify([c.to_dict() for c in rows if match(c)])

@api_bp.get("/candidates/<int:id>")
def get_candidate(id):
    sess = get_session()
    obj = sess.get(Candidate, id)
    if not obj:
        abort(404, "not found")
    return jsonify(obj.to_dict())
