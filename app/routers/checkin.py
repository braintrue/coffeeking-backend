from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.checkin import CheckIn
from app.schemas.checkin import CheckInCreate, CheckInResponse, CheckInStatus
from app.utils.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=CheckInResponse, status_code=status.HTTP_201_CREATED)
def check_in(
    checkin_data: CheckInCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    체크인 - 위치 기반 격리
    
    - 기존 체크인 자동 비활성화
    - 4시간 유효
    - 이후 테이블 조회 시 이 위치만 필터링
    """
    # 기존 활성 체크인 모두 비활성화
    db.query(CheckIn).filter(
        CheckIn.user_id == current_user.id,
        CheckIn.is_active == True
    ).update({"is_active": False})
    
    # 새 체크인 생성
    new_checkin = CheckIn(
        user_id=current_user.id,
        location_code=checkin_data.location_code,
        expires_at=datetime.utcnow() + timedelta(hours=4),
        is_active=True
    )
    
    db.add(new_checkin)
    db.commit()
    db.refresh(new_checkin)
    
    return new_checkin

@router.get("/status", response_model=CheckInStatus)
def get_checkin_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """현재 체크인 상태 조회"""
    active_checkin = db.query(CheckIn).filter(
        CheckIn.user_id == current_user.id,
        CheckIn.is_active == True,
        CheckIn.expires_at > datetime.utcnow()
    ).first()
    
    if active_checkin:
        return CheckInStatus(
            is_checked_in=True,
            location_code=active_checkin.location_code,
            checked_in_at=active_checkin.checked_in_at,
            expires_at=active_checkin.expires_at
        )
    
    return CheckInStatus(is_checked_in=False)

@router.delete("/checkout")
def check_out(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """체크아웃 - 모든 활성 체크인 비활성화"""
    updated = db.query(CheckIn).filter(
        CheckIn.user_id == current_user.id,
        CheckIn.is_active == True
    ).update({"is_active": False})
    
    db.commit()
    
    return {
        "message": "체크아웃 완료",
        "deactivated_count": updated
    }

@router.get("/locations")
def get_available_locations():
    """체크인 가능한 위치 목록"""
    return {
        "locations": [
            {"code": "company-12f", "name": "회사 12층", "icon": "🏢"},
            {"code": "company-13f", "name": "회사 13층", "icon": "🏢"},
            {"code": "cafe-gangnam", "name": "강남 카페", "icon": "☕"},
            {"code": "cafe-hongdae", "name": "홍대 카페", "icon": "☕"}
        ]
    }
