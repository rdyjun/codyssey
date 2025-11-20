import os
import sys
from typing import List, Dict

# 프로젝트 디렉터리를 `sys.path`에 추가하여 uvicorn이 서브프로세스를 리로드할 때에도
# 모듈 임포트가 정상 동작하도록 함
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import Depends, FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import database
import models


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# 앱 시작 시 테이블이 없으면 생성
models.Base.metadata.create_all(bind=database.engine)


def question_to_dict(q: models.Question) -> Dict:
    return {
        'id': q.id,
        'subject': q.subject,
        'content': q.content,
        'create_date': q.create_date.isoformat(),
    }


@app.post('/questions')
def create_question(payload: Dict = Body(...), db: Session = Depends(database.get_db)):
    subject = payload.get('subject')
    content = payload.get('content')
    if not subject or not content:
        raise HTTPException(status_code=400, detail='subject and content required')
    q = models.Question(subject=subject, content=content)
    db.add(q)
    db.commit()
    db.refresh(q)
    return question_to_dict(q)


@app.get('/questions')
def list_questions(db: Session = Depends(database.get_db)) -> List[Dict]:
    qs = db.query(models.Question).order_by(models.Question.create_date.desc()).all()
    return [question_to_dict(q) for q in qs]


@app.get('/questions/{question_id}')
def get_question(question_id: int, db: Session = Depends(database.get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if q is None:
        raise HTTPException(status_code=404, detail='Question not found')
    return question_to_dict(q)


@app.put('/questions/{question_id}')
def update_question(question_id: int, payload: Dict = Body(...), db: Session = Depends(database.get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if q is None:
        raise HTTPException(status_code=404, detail='Question not found')
    subject = payload.get('subject')
    content = payload.get('content')
    if subject:
        q.subject = subject
    if content:
        q.content = content
    db.commit()
    db.refresh(q)
    return question_to_dict(q)


@app.delete('/questions/{question_id}')
def delete_question(question_id: int, db: Session = Depends(database.get_db)):
    q = db.query(models.Question).filter(models.Question.id == question_id).first()
    if q is None:
        raise HTTPException(status_code=404, detail='Question not found')
    db.delete(q)
    db.commit()
    return {'ok': True}
