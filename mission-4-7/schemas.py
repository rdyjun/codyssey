from datetime import datetime
from pydantic import BaseModel


class QuestionSchemaOrmTrue(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        orm_mode = True


class QuestionSchemaOrmFalse(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime

    class Config:
        orm_mode = False
