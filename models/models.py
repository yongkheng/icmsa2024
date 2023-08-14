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

    copy_right_filename = Column(String, index=True)
    copy_right_content = Column(LargeBinary, index=True)
    copy_right_receipt = Column(LargeBinary, index=True)

class Registration(Base):
    __tablename__ = "registration"
    id = Column(Integer, primary_key=True)
    submission_id = Column(String, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    affiliation = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)

    payment_proof_filename = Column(String, index=True)
    payment_proof_content = Column(LargeBinary, index=True)
    payment_proof_receipt = Column(LargeBinary, index=True)

    student_status_proof_filename = Column(String, index=True)
    student_status_proof_content = Column(LargeBinary, index=True)
    student_status_proof_receipt = Column(LargeBinary, index=True)

    participant_type = Column(String, index=True)
    join_dinner = Column(String, index=True)
    diet_allergic = Column(String, index=True)
    additional_dinner_ticket = Column(Integer, index=True)