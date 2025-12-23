from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class CheckInCreate(BaseModel):
    """체크인 요청"""
    location_code: str  # 예: "company-12f"

class CheckInResponse(BaseModel):
    """체크인 응답"""
    id: int
    user_id: int
    location_code: str
    checked_in_at: datetime
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)

class CheckInStatus(BaseModel):
    """현재 체크인 상태"""
    is_checked_in: bool
    location_code: Optional[str] = None
    checked_in_at: Optional[datetime] = None
