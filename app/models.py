from sqlalchemy import Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str | None] = mapped_column(String(255))
    email: Mapped[str | None] = mapped_column(String(255))
    phone: Mapped[str | None] = mapped_column(String(64))
    skills: Mapped[str | None] = mapped_column(Text)
    education: Mapped[str | None] = mapped_column(Text)
    experience_years: Mapped[float | None] = mapped_column(Float)
    source_filename: Mapped[str | None] = mapped_column(String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "skills": self.skills.split(",") if self.skills else [],
            "education": self.education.split("\n") if self.education else [],
            "experience_years": self.experience_years,
            "source_filename": self.source_filename,
        }
