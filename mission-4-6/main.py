import os
import sys
from typing import List, Dict

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI

import database
import models
from domain.question.question_router import router as question_router


app = FastAPI()

# 애플리케이션 시작 시 테이블이 없으면 생성
models.Base.metadata.create_all(bind=database.engine)

# question 라우터 등록
app.include_router(question_router)


def question_to_dict(q: models.Question) -> Dict:
    return {
        'id': q.id,
        'subject': q.subject,
        'content': q.content,
        'create_date': q.create_date.isoformat(),
    }
