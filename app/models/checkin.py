from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class CheckIn(Base):
    """사용자 체크인 기록"""
    __tablename__ = "checkins"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_code = Column(String, nullable=False, index=True)  # 예: "company-12f"
    
    # 체크인 시간
    checked_in_at = Column(DateTime, default=datetime.utcnow)
    
    # 자동 체크아웃 (선택, 나중에 확장 가능)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # 관계
    user = relationship("User", back_populates="checkins")

    def __repr__(self):
        return f"<CheckIn user_id={self.user_id} location={self.location_code}>"
