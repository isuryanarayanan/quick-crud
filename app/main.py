from fastapi import FastAPI
from fastapi.responses import FileResponse
from api.get_courses import get_courses_router
from api.get_course_overview import get_course_overview_router
from api.get_chapter import get_chapter_router
from api.rate_chapter import rate_chapter_router

def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(get_courses_router)
    application.include_router(get_chapter_router)
    application.include_router(rate_chapter_router)
    application.include_router(get_course_overview_router)
    return application

app = create_application()

@app.get("/")
async def root():
    """
    This route will serve an index.html file from the templates directory.
    """
    return FileResponse("templates/index.html")




