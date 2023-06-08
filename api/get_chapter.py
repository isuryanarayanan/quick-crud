from fastapi import APIRouter
from db.mongodb import db

get_chapter_router = APIRouter()

@get_chapter_router.get("/courses/{course_name}/chapter/{chapter_name}", tags=["chapter"])
async def get_chapter(course_name: str, chapter_name: str):
    """
    This endpoint returns the chapter with the given name from the course with the given name.
    If the course or chapter does not exist, it returns a 404 error.
    """

    course = db.courses.find_one({"name": course_name})
    if course is None:
        return {"error": "Course not found"}
    

    chapter = next((chapter for chapter in course["chapters"] if chapter["name"] == chapter_name), None)
    chapter["url"] = f"http://localhost:8000/courses/{course_name}/chapter/{chapter_name}"
    chapter["course_url"] = f"http://localhost:8000/courses/{course_name}"
    chapter["rate_positive_url"] = f"http://localhost:8000/courses/{course_name}/chapter/{chapter_name}/rate?rate=positive"
    chapter["rate_negative_url"] = f"http://localhost:8000/courses/{course_name}/chapter/{chapter_name}/rate?rate=negative"

    if chapter is None:
        return {"error": "Chapter not found"}
    
    return chapter
