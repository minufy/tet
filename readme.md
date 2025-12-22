# tet
테트리스 봇 대전

[예시 봇](https://github.com/minufy/tet_minu_bot)

# 정보 
## 서버 -> 봇 데이터
```py
미노_종류 = ["Z", "L", "O", "S", "I", "J", "T"]

data = {
    "grid": 2차원 배열,
    "queue": 미노_종류들이 들어있는 배열,
    "mino_type": 미노_종류 중 하나,
}
```

## 봇 -> 서버 데이터
```py
data = {
  "events": []
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