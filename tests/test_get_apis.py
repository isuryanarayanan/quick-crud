import pytest
from fastapi.testclient import TestClient
from app.main import create_application
from db.mongodb import db

client = TestClient(create_application())

@pytest.fixture(scope="module")
def setup_test_documents():
    course_name = "your_course_name"
    chapter_name = "your_chapter_name"

    # Set up the test documents
    test_course = {
        "name": course_name,
        "chapters": [
            {
                "name": chapter_name,
                "ratings": {
                    "positive": 0,
                    "negative": 0
                }
            }
        ],
        "rating": 0
    }

    # Insert the test course into the database
    db.courses.insert_one(test_course)

    yield

    # Clean up the test documents
    db.courses.delete_one({"name": course_name})


@pytest.fixture(autouse=True)
def clear_test_documents():
    # This fixture runs after each test automatically
    # Clean up the test documents
    db.courses.delete_many({
        "name": {
            "$in": [
                "your_course_name",
                "invalid_course_name"
            ]
        }

    })


def test_get_courses():
    response = client.get("/courses")
    assert response.status_code == 200


def test_rate_chapter_positive():
    course_name = "your_course_name"
    chapter_name = "your_chapter_name"

    response = client.get(f"/courses/{course_name}/chapter/{chapter_name}/rate?rate=positive")
    assert response.status_code == 200


def test_rate_chapter_negative():
    course_name = "your_course_name"
    chapter_name = "your_chapter_name"

    response = client.get(f"/courses/{course_name}/chapter/{chapter_name}/rate?rate=negative")
    assert response.status_code == 200


def test_rate_chapter_invalid_rate():
    course_name = "your_course_name"
    chapter_name = "your_chapter_name"

    response = client.get(f"/courses/{course_name}/chapter/{chapter_name}/rate?rate=invalid")
    assert response.json() == {"error": "Invalid rate value"}

def test_rate_chapter_invalid_course():
    course_name = "invalid_course_name"
    chapter_name = "your_chapter_name"

    response = client.get(f"/courses/{course_name}/chapter/{chapter_name}/rate?rate=positive")
    assert response.json() == {"error": "Course not found"}

def test_rate_chapter_invalid_chapter():
    course_name = "your_course_name"
    chapter_name = "invalid_chapter_name"

    response = client.get(f"/courses/{course_name}/chapter/{chapter_name}/rate?rate=positive")
    assert response.json() == {"error": "Course not found"}

