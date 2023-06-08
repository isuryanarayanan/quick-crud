from pydantic import BaseModel, Field
from typing import List
import datetime

class Chapter(BaseModel):
    name: str
    text: str
    ratings: 'Ratings'


class Ratings(BaseModel):
    positive: int = 0
    negative: int = 0

class Course(BaseModel):
    name: str = Field(..., alias='_id')
    date: datetime.datetime
    description: str
    domain: str
    chapters: List[Chapter]
    rating: int

