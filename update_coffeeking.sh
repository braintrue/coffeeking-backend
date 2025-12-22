#!/bin/bash
set -euo pipefail

echo "🚀 CoffeeKing 업데이트 시작..."

# 0) 작업 전 상태 확인
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "❌ git 레포지토리 폴더에서 실행하세요."
  exit 1
fi

BRANCH="$(git rev-parse --abbrev-ref HEAD)"
echo "📌 현재 브랜치: $BRANCH"

# 1) .gitignore에 민감/로컬 파일 차단 (가장 먼저!)
echo "🛡️  .gitignore 업데이트..."
touch .gitignore
grep -qxF ".env" .gitignore || echo ".env" >> .gitignore
grep -qxF "*.db" .gitignore || echo "*.db" >> .gitignore
grep -qxF "*.db.backup.*" .gitignore || echo "*.db.backup.*" >> .gitignore

# 2) 변경사항 임시 백업 (main을 더럽히지 않게: stash 추천)
echo "📦 변경사항 stash..."
git stash push -u -m "WIP backup before update $(date +%Y%m%d_%H%M%S)" || true

# 3) requirements.txt 업데이트 (중복 방지)
echo "📝 requirements.txt 업데이트..."
touch requirements.txt
grep -q "^email-validator==" requirements.txt || echo "email-validator==2.1.1" >> requirements.txt
grep -q "^jinja2==" requirements.txt || echo "jinja2==3.1.4" >> requirements.txt

# 4) .env.example 생성 (커밋용)
echo "🔑 .env.example 생성..."
cat > .env.example << 'EOF'
DATABASE_URL=sqlite:///./coffeeking.db
JWT_SECRET_KEY=change-this-in-production-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DEBUG=True
EOF

# 5) 로컬 실행용 .env 생성 (없으면)
echo "🔑 .env 생성..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "✅ .env 생성됨(로컬 전용, 커밋 금지)"
else
  echo "⚠️  .env 이미 존재"
fi

# 6) 디렉토리 구조 보장
echo "📁 디렉토리 보장..."
mkdir -p templates static app/routers app/utils tests

# 7) DB 백업 (로컬 전용)
echo "💾 DB 백업..."
if [ -f coffeeking.db ]; then
  cp coffeeking.db "coffeeking.db.backup.$(date +%Y%m%d_%H%M%S)"
  echo "✅ DB 백업 완료"
fi

# 8) stash 복구(원하면)
echo "📦 stash 복구 시도..."
git stash pop || echo "⚠️  stash pop에서 충돌 가능. 필요 시 수동 해결하세요."

echo "✅ 스크립트 완료"
echo "다음: templates/index.html 추가 + app/main.py 템플릿 라우트 추가 + JS fetch 연동"
