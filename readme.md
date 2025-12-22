# tet
테트리스 봇 대전

[예시 봇](https://github.com/minufy/tet_minu_bot)

# 정보 
## 서버 -> 봇 데이터
```py
미노_종류 = ["Z", "L", "O", "S", "I", "J", "T"]

data = {
    "state": "started" 아니면 "not_started",
    "grid": 2차원 배열,
    "queue": 미노_종류들이 들어있는 배열,
    "mino_type": 미노_종류 중 하나
}
```

## 봇 -> 서버 데이터
```py
data = {
  "events": [],
  "index": 제어할 플레이어 인덱스 (0 아니면 1)
}
```

## 이벤트 형식
형식
```
타입.키
```

타입
```
keydown
keyup
```

키
```
hold
cw
ccw
180
left
right
harddrop
softdrop
```