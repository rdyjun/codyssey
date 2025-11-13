from __future__ import annotations

import csv
import json
import os
from typing import Any, Dict, List

from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse

from model import TodoItem

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


def _write_all_todos_to_csv() -> None:
    """메모리의 전체 todo_list를 CSV로 덮어씁니다.

    각 행은 id와 JSON 문자열로 기록합니다.
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in todo_list:
            try:
                item_id = int(item.get('id')) if item.get('id') is not None else ''
            except Exception:
                item_id = ''
            writer.writerow([item_id, json.dumps(item, ensure_ascii=False)])


def _find_todo_index_by_id(todo_id: int) -> int:
    """id로 todo_list 내의 인덱스를 찾아 반환합니다. 없으면 -1을 반환."""
    for idx, item in enumerate(todo_list):
        try:
            if int(item.get('id')) == int(todo_id):
                return idx
        except Exception:
            continue
    return -1


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


@router.get('/todos/{todo_id}')
async def get_single_todo(todo_id: int) -> Dict[str, Any]:
    """경로 매개변수로 전달된 id에 해당하는 단일 todo 항목을 반환합니다."""
    idx = _find_todo_index_by_id(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail='todo not found')
    return {'todo': todo_list[idx]}


@router.put('/todos/{todo_id}')
async def update_todo(todo_id: int, item: TodoItem) -> Dict[str, Any]:
    """주어진 id의 todo를 업데이트합니다. 요청 본문은 TodoItem 모델입니다.

    부분 업데이트를 허용하기 위해 Pydantic의 exclude_unset 기능을 사용합니다.
    """
    idx = _find_todo_index_by_id(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail='todo not found')

    # 변경사항만 추출하여 기존 항목에 반영합니다
    update_data = item.dict(exclude_unset=True)
    if not update_data:
        return JSONResponse(status_code=400, content={'warning': 'no fields to update'})

    old_item = dict(todo_list[idx])
    new_item = dict(old_item)
    new_item.update(update_data)
    # id가 명시적으로 들어있다면 강제 변환/보호
    new_item['id'] = old_item.get('id')

    # 메모리와 파일 동기화
    todo_list[idx] = new_item
    try:
        _write_all_todos_to_csv()
    except Exception:
        # 실패하면 메모리 상태 복원
        todo_list[idx] = old_item
        raise HTTPException(status_code=500, detail='failed to persist update')

    return {'todo': new_item}


@router.delete('/todos/{todo_id}')
async def delete_single_todo(todo_id: int) -> Dict[str, Any]:
    """주어진 id의 todo 항목을 삭제합니다."""
    idx = _find_todo_index_by_id(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail='todo not found')

    removed = todo_list.pop(idx)
    try:
        _write_all_todos_to_csv()
    except Exception:
        # 파일 쓰기에 실패하면 메모리에 다시 삽입
        todo_list.insert(idx, removed)
        raise HTTPException(status_code=500, detail='failed to persist deletion')

    return {'deleted': True, 'todo': removed}


app = FastAPI()
app.include_router(router)


@app.on_event('startup')
def _startup_event() -> None:
    _load_todos()


if __name__ == '__main__':
    # 로컬에서 간단히 실행해볼 때를 위한 안내 메시지입니다. 실제 서비스는 uvicorn으로 띄우세요.
    print('이 모듈은 uvicorn으로 실행해야 합니다:')
    print("uvicorn mission-4-1.todo:app --reload --port 8000")
