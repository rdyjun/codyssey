from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models
from schemas import QuestionSchemaOrmTrue, QuestionSchemaOrmFalse

router = APIRouter(prefix='/api/question')


@router.get('/', response_model=List[QuestionSchemaOrmTrue])
def question_list(db: Session = Depends(get_db)) -> List[QuestionSchemaOrmTrue]:
    """질문 목록을 ORM으로 조회하여 반환한다.

    응답은 `QuestionSchemaOrmTrue`(orm_mode=True)를 사용하므로
    SQLAlchemy 모델 인스턴스를 직접 반환해도 Pydantic이 변환한다.
    """
    qs = db.query(models.Question).order_by(models.Question.create_date.desc()).all()
    return qs


@router.get('/raw', response_model=List[QuestionSchemaOrmFalse])
def question_list_raw(db: Session = Depends(get_db)) -> List[QuestionSchemaOrmFalse]:
    """ORM 객체를 직접 반환했을 때 `orm_mode=False` 스키마 사용 시 실패 예시용 엔드포인트.

    (보너스) `QuestionSchemaOrmFalse`는 orm_mode=False 설정이므로
    SQLAlchemy 모델 인스턴스를 직접 response로 반환하면 검증 오류가 발생할 수 있다.
    """
    qs = db.query(models.Question).order_by(models.Question.create_date.desc()).all()
    # Pydantic이 ORM 객체를 처리하지 못하므로 dict로 변환하여 반환하면 동작한다.
    result = []
    for q in qs:
        result.append({
            'id': q.id,
            'subject': q.subject,
            'content': q.content,
            'create_date': q.create_date,
        })
    return result
