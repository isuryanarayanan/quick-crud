from fastapi import APIRouter
from db.mongodb import db
from models.courses import Course, Chapter, Ratings

rate_chapter_router = APIRouter()

@rate_chapter_router.get("/courses/{course_name}/chapter/{chapter_name}/rate", tags=["rate_chapter"])
async def rate_chapter(course_name: str, chapter_name: str, rate: str):
    """
    This endpoint allows you to rate a chapter.

    If the course or chapter does not exist, it returns a 404 error.

    rate can be one of the following values:
    - positive
    - negative

    If positive, update the positive field of the chapter rating with 1.
    If negative, update the negative field of the chapter rating with 1.
    """

    if rate not in ["positive", "negative"]:
        return {"error": "Invalid rate value"}

    # Get the course from the database
    course = db.courses.find_one({"name": course_name, "chapters.name": chapter_name}, {"_id": 0})
    if course is None:
        return {"error": "Course not found"}

    # Update the chapter rating
    db.courses.update_one(
        {"name": course_name, "chapters.name": chapter_name},
        {"$inc": {f"chapters.$.ratings.{rate}": 1}}
    )

    # Calculate the course rating based on the ratio of chapter ratings
    total_chapters = db.courses.count_documents({"name": course_name})
    chapter_ratings = db.courses.aggregate([
        {"$match": {"name": course_name}},
        {"$unwind": "$chapters"},
        {"$group": {
            "_id": "$name",
            "positive": {"$sum": "$chapters.ratings.positive"},
            "negative": {"$sum": "$chapters.ratings.negative"},
        }},
        {"$project": {
            "_id": 0,
            "rating": {
                "$divide": [
                    {"$subtract": ["$positive", "$negative"]},
                    {"$add": ["$positive", "$negative"]}
                ]
            }
        }}
    ])

    # Map the course rating to a scale of 0 to 5
    course_rating = next(chapter_ratings)["rating"]
    course_rating_scaled = (course_rating + 1) * 2.5

    # Update the course rating
    db.courses.update_one(
        {"name": course_name},
        {"$set": {"rating": course_rating_scaled}}
    )

    return {"message": "Chapter rated successfully"}
