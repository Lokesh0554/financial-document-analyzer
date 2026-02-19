from sqlalchemy import Column, Integer, String, Text
from database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String)
    file_name = Column(String)
    query = Column(Text)
    result = Column(Text)
    status = Column(String)

