import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from database import Base


class Stage(str, enum.Enum):
    idea = "idea"
    mvp = "mvp"
    beta = "beta"
    launch = "launch"


class MilestoneStatus(str, enum.Enum):
    pending = "pending"
    done = "done"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    stage = Column(Enum(Stage), default=Stage.idea, nullable=False)
    target_launch_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    milestones = relationship(
        "Milestone", back_populates="project", cascade="all, delete-orphan"
    )


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    title = Column(String, nullable=False)
    stage = Column(Enum(Stage), nullable=False)
    status = Column(Enum(MilestoneStatus), default=MilestoneStatus.pending)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="milestones")
