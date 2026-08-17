from sqlalchemy import Column, Integer, String, Float, Boolean
from api.db import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String, index=True, nullable=False)
    annual_revenue = Column(Float, default=0.0)
    score = Column(Integer, default=50)
    sellable = Column(Boolean, default=False)
