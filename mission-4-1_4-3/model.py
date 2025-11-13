from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class TodoItem(BaseModel):
    """업데이트 요청에 사용할 TodoItem 모델.

    모든 필드는 선택적(optional)로 정의하여 부분 업데이트(또는 전체 교체)
    에서 유연하게 사용될 수 있습니다.
    """

    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
