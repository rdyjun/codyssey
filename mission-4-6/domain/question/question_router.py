from typing import List, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models

router = APIRouter(prefix='/api/question')


@router.get('/', response_model=List[Dict])
def question_list(db: Session = Depends(get_db)) -> List[Dict]:
    """질문 목록을 조회하여 반환한다."""
    qs = db.query(models.Question).order_by(models.Question.create_date.desc()).all()
    result: List[Dict] = []
    for q in qs:
        result.append({
            'id': q.id,
            'subject': q.subject,
            'content': q.content,
            'create_date': q.create_date.isoformat(),
        })
    return result
