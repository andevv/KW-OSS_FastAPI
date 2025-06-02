from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from decimal import Decimal, ROUND_HALF_UP

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# 학점 → 평점 매핑 (4.5 만점)
grade_to_point = {
    "A+": Decimal("4.5"),
    "A0":  Decimal("4.0"),
    "B+": Decimal("3.5"),
    "B0":  Decimal("3.0"),
    "C+": Decimal("2.5"),
    "C0":  Decimal("2.0"),
    "D+": Decimal("1.5"),
    "D0":  Decimal("1.0"),
    "F":  Decimal("0.0")
}

class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str

class Student(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

@app.post("/student_summary")
async def calculate_gpa(student: Student):
    total_credits = 0
    total_points = Decimal("0.0")

    for course in student.courses:
        credit = course.credits
        grade_point = grade_to_point.get(course.grade, Decimal("0.0"))
        total_credits += credit
        total_points += grade_point * Decimal(credit)

    if total_credits > 0:
        raw_gpa = total_points / Decimal(total_credits)
        gpa = raw_gpa.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        gpa = Decimal("0.00")

    return {
        "student_summary": {
            "student_id": student.student_id,
            "name": student.name,
            "gpa": float(gpa),
            "total_credits": total_credits
        }
    }