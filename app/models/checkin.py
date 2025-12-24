from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base

class CheckIn(Base):
    """사용자 체크인 - 위치 기반 격리"""
    __tablename__ = "checkins"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    location_code = Column(String, nullable=False, index=True)  # "company-12f"
    
    checked_in_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)  # 4시간 후
    is_active = Column(Boolean, default=True, index=True)
    
    # 관계
    user = relationship("User", back_populates="checkins")
    
    def __repr__(self):
        return f"<CheckIn user={self.user_id} location={self.location_code} active={self.is_active}>"
