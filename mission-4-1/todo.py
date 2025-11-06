from __future__ import annotations

import csv
import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse

# 데이터 파일 경로(CSV) - 각 행에 JSON 문자열로 todo 항목을 저장합니다
DATA_FILE = os.path.join(os.path.dirname(__file__), 'todo_data.csv')

# 메모리 상의 todo 리스트
todo_list: List[Dict[str, Any]] = []

router = APIRouter()


def _load_todos() -> None:
    """CSV 파일에서 todo 항목을 불러와 메모리 리스트에 적재합니다.

    CSV의 각 행은 [id, json_string] 형태로 되어 있습니다. 파일이 없으면
    아무 작업도 수행하지 않습니다.
    """
    todo_list.clear()
    if not os.path.exists(DATA_FILE):
        return

    with open(DATA_FILE, 'r', encoding='utf-8', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue
            try:
                # 첫 번째 열은 id, 두 번째 열은 JSON 문자열입니다
                parsed_id = int(row[0]) if row[0] else None
                data = json.loads(row[1])
            except Exception:
                # 형식이 이상한 행은 건너뜁니다
                continue
            # 저장된 id가 JSON 내부에 없으면 파일의 id를 사용합니다
            if parsed_id is not None and 'id' not in data:
                data['id'] = parsed_id
            todo_list.append(data)


def _append_todo_to_csv(item: Dict[str, Any]) -> None:
    """단일 todo 항목을 CSV 파일에 추가(append)합니다.

    항목은 JSON 문자열로 두 번째 열에 저장되며, 첫 번째 열은 내부에서 부여한
    숫자 id를 기록합니다.
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    # 현재 파일에 존재하는 최대 id를 계산하여 중복을 피합니다.
    max_id = 0
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if not row:
                        continue
                    try:
                        row_id = int(row[0])
                        if row_id > max_id:
                            max_id = row_id
                    except Exception:
                        continue
        except Exception:
            # 파일을 읽는 동안 문제가 생기면 append로 진행하되 id 계산은 0 기반으로 합니다
            max_id = 0

    new_id = max_id + 1
    # item에 id가 없으면 새로 부여합니다
    if 'id' not in item:
        item = dict(item)
        item['id'] = new_id

    with open(DATA_FILE, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([new_id, json.dumps(item, ensure_ascii=False)])


@router.post('/add_todo')
async def add_todo(item: Dict[str, Any]) -> Dict[str, Any]:
    """새로운 todo 항목을 추가합니다.

    요청 본문으로 JSON 객체(dict)를 기대합니다. 빈 dict인 경우 경고를 반환합니다.
    정상 항목은 메모리 리스트와 CSV에 추가되며, 추가된 항목을 dict 형태로 응답합니다.
    """
    if not isinstance(item, dict):
        raise HTTPException(status_code=400, detail='payload must be a dict')

    if not item:
        # 보너스 요구사항: 빈 dict이면 경고 메시지를 JSON으로 반환합니다
        return JSONResponse(status_code=400, content={'warning': 'input dict is empty'})

    # id가 없으면 내부적으로 id를 부여합니다
    if 'id' not in item:
        item = dict(item)  # 얕은 복사
        item['id'] = len(todo_list) + 1

    todo_list.append(item)
    try:
        _append_todo_to_csv(item)
    except Exception:
        # 파일 쓰기 실패 시 메모리에서 방금 추가한 항목을 제거하여 상태를 일관되게 유지합니다
        todo_list.pop()
        raise HTTPException(status_code=500, detail='failed to persist todo')

    return {'todo': item}


@router.get('/retrieve_todo')
async def retrieve_todo() -> Dict[str, List[Dict[str, Any]]]:
    """저장된 모든 todo 항목을 반환합니다.

    반환 값은 요구사항에 맞춰 dict 형태로 todo 리스트를 감싸서 제공합니다.
    """
    return {'todo_list': todo_list}


app = FastAPI()
app.include_router(router)


@app.on_event('startup')
def _startup_event() -> None:
    _load_todos()


if __name__ == '__main__':
    # 로컬에서 간단히 실행해볼 때를 위한 안내 메시지입니다. 실제 서비스는 uvicorn으로 띄우세요.
    print('이 모듈은 uvicorn으로 실행해야 합니다:')
    print("uvicorn mission-4-1.todo:app --reload --port 8000")
