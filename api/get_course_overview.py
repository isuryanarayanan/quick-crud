from fastapi import APIRouter
from db.mongodb import db

get_course_overview_router = APIRouter()

@get_course_overview_router.get("/courses/{course_name}", tags=["course_overview"])
async def get_course_overview(course_name: str):
    """
    This endpoint returns the course overview for a given course name.
    """

    course_overview = db.courses.find_one({
        'name': course_name
    },{
        '_id':0,
        'name': 1,
        'course_url': {
            '$concat': ['http://localhost:8000/courses/', '$name']
        },
        'date': 1,
        'description': 1,
        'domain': 1,
        'chapters': {
            "$map": {
                "input": "$chapters",
                "as": "chapter",
                "in": {
                    'name': '$$chapter.name',
                    'url': {
                        '$concat': ['http://localhost:8000/courses/', '$name', '/chapter/', '$$chapter.name']
                    },
                    'text': '$$chapter.text',
                    'ratings': '$$chapter.ratings',
                    'rate_positive_url': {
                        '$concat': ['http://localhost:8000/courses/', '$name', '/chapter/', '$$chapter.name', '/rate?rate=positive']
                    },
                    'rate_negative_url': {
                        '$concat': ['http://localhost:8000/courses/', '$name', '/chapter/', '$$chapter.name', '/rate?rate=negative']
                    },

                }
            }
        },
        'rating': 1
    })

    return course_overview
