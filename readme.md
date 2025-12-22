# tet
테트리스 봇 대전

[예시 봇](https://github.com/minufy/tet_minu_bot)

# 정보 
## 서버 -> 봇 데이터
### 설명
| 항목 | 타입 | 설명 |
| - | - | - |
| state | `str` | 게임 진행 여부 (`started`/`not_started`) |
| grid | `list[list[str]]` | 게임 판. 각 셀은 공백, 미노 타입 또는 X(가비지) 중 하나 |
| queue | `list[str]` | 넥스트 |
| mino_type | `str` | 현재 미노 타입 |
| hold_mino_type | `str` | 홀드 미노 타입. 없는 경우 빈 문자열 |
미노 타입: `"Z", "L", "O", "S", "I", "J", "T"`

### 예시 데이터
```py
data = {
    "state": "started",
    "grid": [
        [" ", " ", ... , " ", " "],
        [" ", " ", ... , " ", " "],
        ...
        [" ", " ", ... , " ", " "],
        [" ", " ", ... , " ", " "],
    ],
    "queue": ["L", "O", "S", "I", "J", "T"],
    "mino_type": "Z",
    "hold_mino_type": ""
}
```

## 봇 -> 서버 데이터
### 설명
| 항목 | 타입 | 설명 |
| - | - | - |
| events | `list[str]` | 보낼 이벤트 리스트 |
| index | `int` | 제어할 플레이어 인덱스. 0 또는 1 |

### 예시 데이터
```py
data = {
  "events": ["keydown.right", "keyup.right"],
  "index": 0
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