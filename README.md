# CoffeeKing Backend

FastAPI 기반의 CoffeeKing 백엔드 MVP 스캐폴딩입니다. 로컬 개발 및 Docker 실행을 모두 지원하며 `/docs`에서 즉시 API를 테스트할 수 있습니다.

## 📁 프로젝트 구조
- `app/`
  - `main.py`: FastAPI 앱 엔트리포인트, 라우터 등록 및 시드 로직
  - `config.py`: 환경 변수 설정(`.env`)
  - `database.py`: SQLAlchemy 엔진/세션 팩토리
  - `models/`: SQLAlchemy 모델 정의
  - `schemas/`: Pydantic 스키마 정의
  - `routers/`: 인증·메뉴·테이블·주문·매칭 라우터
  - `utils/`: JWT/비밀번호 유틸, 시드 로더
- `data/menus_seed.json`: 초기 메뉴 데이터
- `Dockerfile`, `docker-compose.yml`: 컨테이너 실행 구성
- `requirements.txt`: Python 의존성 목록
- `.env.example`: 환경 변수 템플릿

## 🚀 빠른 시작
### 1) 의존성 설치 및 로컬 실행
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
`http://127.0.0.1:8000/docs` 에 접속해 바로 테스트할 수 있습니다.

### 2) Docker 실행
```bash
docker compose up --build
```
컨테이너가 뜨면 `http://localhost:8000/docs` 에서 OpenAPI UI를 확인하세요.

## 🔑 환경 변수
`.env.example`을 복사해 `.env`를 만든 후 필요값을 수정하세요.
```
DATABASE_URL=sqlite:///./coffeeking.db
JWT_SECRET_KEY=change-me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

## 🧰 기본 기능
- **인증**: 회원가입/로그인, JWT 발급, `/auth/me`로 토큰 검증
- **메뉴**: `/menus`에서 메뉴 조회·생성, 앱 시작 시 `menus_seed.json`으로 자동 시드
- **테이블**: 테이블 생성/목록/상태 업데이트
- **주문**: 간단한 주문 생성과 합계 계산
- **매칭**: 테이블 기반 매칭 생성 및 참가

추가 도메인 로직을 확장할 수 있도록 최소한의 구조와 유틸을 포함했습니다.
