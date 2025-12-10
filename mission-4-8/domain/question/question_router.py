from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
import models
from schemas import QuestionCreate, QuestionRead


router = APIRouter(prefix='/api/question')


@router.post('/', response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
def question_create(question: QuestionCreate, db: Session = Depends(get_db)) -> QuestionRead:
    """질문을 등록한다."""
    q = models.Question(subject=question.subject, content=question.content)
    db.add(q)
    db.commit()
    db.refresh(q)
    return q


@router.get('/', response_model=List[QuestionRead])
def question_list(db: Session = Depends(get_db)) -> List[QuestionRead]:
    """질문 목록을 조회한다."""
    qs = db.query(models.Question).order_by(models.Question.create_date.desc()).all()
    return qs
