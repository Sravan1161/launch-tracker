from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel

from models import Stage, MilestoneStatus


# ---- Milestone schemas ----

class MilestoneBase(BaseModel):
    title: str
    stage: Stage
    status: MilestoneStatus = MilestoneStatus.pending
    notes: Optional[str] = None


class MilestoneCreate(MilestoneBase):
    pass


class MilestoneUpdate(BaseModel):
    title: Optional[str] = None
    stage: Optional[Stage] = None
    status: Optional[MilestoneStatus] = None
    notes: Optional[str] = None


class MilestoneOut(MilestoneBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ---- Project schemas ----

class ProjectBase(BaseModel):
    name: str
    stage: Stage = Stage.idea
    target_launch_date: Optional[date] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    stage: Optional[Stage] = None
    target_launch_date: Optional[date] = None


class ProjectOut(ProjectBase):
    id: int
    created_at: datetime
    milestones: List[MilestoneOut] = []

    class Config:
        from_attributes = True


class ProjectProgress(BaseModel):
    project_id: int
    total_milestones: int
    completed_milestones: int
    percent_complete: float
