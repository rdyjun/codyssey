# mission-4-1 TODO service

간단한 TO-DO 웹 서비스입니다. FastAPI와 uvicorn으로 실행합니다.

간단 실행법

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn
uvicorn mission-4-1.todo:app --reload --port 8000
```

핵심 엔드포인트

- POST /add_todo

  - 요청: JSON 객체(dict)
  - 동작: todo를 저장하고, 정상 저장 시 `{'todo': {...}}` 형태로 반환
  - 빈 dict를 보낼 경우: HTTP 400, `{'warning': 'input dict is empty'}` 반환

- GET /retrieve_todo
  - 저장된 항목을 `{'todo_list': [...]} ` 형태로 반환

저장소

데이터는 `mission-4-1/todo_data.csv`에 저장됩니다. 각 행은 `[id, json_string]` 형식입니다.

간단한 예시 (curl)

```sh
# 빈 dict 전송 => 경고
curl -i -X POST -H 'Content-Type: application/json' -d '{}' http://127.0.0.1:8000/add_todo

# 정상 추가
curl -i -X POST -H 'Content-Type: application/json' -d '{"title":"buy milk"}' http://127.0.0.1:8000/add_todo

# 조회
curl -i http://127.0.0.1:8000/retrieve_todo
```
