from fastapi import APIRouter, Query
from db.mongodb import db
from models.courses import Course, Chapter, Ratings

get_courses_router = APIRouter()

@get_courses_router.get("/courses")
async def get_courses(
    sort_by: str = Query("alphabetical", description="Sort courses by 'alphabetical', 'date', or 'rating'"),
    domain: str = Query(None, description="Filter courses by domain")
):
    """
    This endpoint returns a list of all courses.
    """

    collection = db['courses']

    # Define the sort key and direction based on the provided sort_by parameter
    sort_key = None
    sort_direction = None

    if sort_by == "alphabetical":
        sort_key = "name"
        sort_direction = 1
    elif sort_by == "date":
        sort_key = "date"
        sort_direction = -1
    elif sort_by == "rating":
        sort_key = "rating"
        sort_direction = -1

    # Define the filter based on the provided domain parameter
    filter_query = {}
    if domain:
        filter_query["domain"] = domain
    
    courses = list(collection.find(filter_query, {
        '_id': 0,
        'name': 1,
        'date': 1,
        'description': 1,
        'domain': 1,
        'rating': 1,
        'course_url': {
            '$concat': ['http://localhost:8000/courses/', '$name']
        },
    }).sort(sort_key, sort_direction))

    return courses
