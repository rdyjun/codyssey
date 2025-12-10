import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import database
import models
from domain.question.question_router import router as question_router


app = FastAPI()

# CORS 설정 (프론트엔드에서 API 호출 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# 애플리케이션 시작 시 테이블이 없으면 생성
models.Base.metadata.create_all(bind=database.engine)

# question 라우터 등록
app.include_router(question_router)

# 프론트엔드 정적 파일 서빙
app.mount('/frontend', StaticFiles(directory='frontend'), name='frontend')
