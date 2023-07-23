from sqlalchemy import Column, Integer, String, TIMESTAMP, LargeBinary
from database.database import Base


class Submission(Base):
    __tablename__ = "submission"
    id = Column(Integer, primary_key=True)
    submission_id = Column(String, index=True)
    revision_version = Column(Integer, index=True)
    timestamp = Column(TIMESTAMP, index=True)
    corresponding_name = Column(String, index=True)
    corresponding_email = Column(String, index=True)
    submission_title = Column(String, index=True)
    submission_keywords = Column(String, index=True)
    submission_type = Column(String, index=True)
    submission_filename = Column(String, index=True)

    abstract_filename = Column(String, index=True)
    abstract_content = Column(LargeBinary, index=True)
    abstract_receipt = Column(LargeBinary, index=True)
    in_proceedings = Column(String, index=True)
    in_journal = Column(String, index=True)

    fullpaper_filename = Column(String, index=True)
    fullpaper_content = Column(LargeBinary, index=True)
    fullpaper_receipt = Column(LargeBinary, index=True)
    camera_ready_filename = Column(String, index=True)
    camera_ready_content = Column(LargeBinary, index=True)
    camera_ready_receipt = Column(LargeBinary, index=True)