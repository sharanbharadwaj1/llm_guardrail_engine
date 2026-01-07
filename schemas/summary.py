from pydantic import BaseModel, Field, field_validator
import re


class SummaryOutput(BaseModel):
    title: str = Field(..., min_length=5, max_length=220)
    summary: str = Field(..., min_length=20, max_length=1000)

    @field_validator("summary")
    @classmethod
    def must_be_two_sentences(cls, v: str) -> str:
        # Simple sentence split heuristic
        # sentences = re.split(r"[.!?]+", v.strip())
        charcount = len(v.strip())
        sentences = re.split(r"(?<!Mr)(?<!Mrs)(?<!Dr)[.!?]+", v.strip())

        sentences = [s for s in sentences if s.strip()]
        print(f"Length: {len(sentences)}")
        if len(sentences) != 2:
            raise ValueError("Summary must contain exactly two sentences")

        return v.strip()
