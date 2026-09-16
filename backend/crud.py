from sqlalchemy.orm import Session

import models
import schemas


# ---- Project CRUD ----

def get_projects(db: Session):
    return db.query(models.Project).order_by(models.Project.created_at.desc()).all()


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def create_project(db: Session, project: schemas.ProjectCreate):
    db_project = models.Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project_id: int, project: schemas.ProjectUpdate):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    for field, value in project.model_dump(exclude_unset=True).items():
        setattr(db_project, field, value)
    db.commit()
    db.refresh(db_project)
    return db_project


def delete_project(db: Session, project_id: int):
    db_project = get_project(db, project_id)
    if not db_project:
        return None
    db.delete(db_project)
    db.commit()
    return db_project


# ---- Milestone CRUD ----

def get_milestones(db: Session, project_id: int):
    return (
        db.query(models.Milestone)
        .filter(models.Milestone.project_id == project_id)
        .order_by(models.Milestone.created_at)
        .all()
    )


def create_milestone(db: Session, project_id: int, milestone: schemas.MilestoneCreate):
    db_milestone = models.Milestone(**milestone.model_dump(), project_id=project_id)
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone


def update_milestone(db: Session, milestone_id: int, milestone: schemas.MilestoneUpdate):
    db_milestone = (
        db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()
    )
    if not db_milestone:
        return None
    for field, value in milestone.model_dump(exclude_unset=True).items():
        setattr(db_milestone, field, value)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone


def delete_milestone(db: Session, milestone_id: int):
    db_milestone = (
        db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()
    )
    if not db_milestone:
        return None
    db.delete(db_milestone)
    db.commit()
    return db_milestone


# ---- Progress calculation ----
# This is real logic, not just a pass-through — worth highlighting in the walkthrough.

def get_project_progress(db: Session, project_id: int):
    milestones = get_milestones(db, project_id)
    total = len(milestones)
    completed = sum(1 for m in milestones if m.status == models.MilestoneStatus.done)
    percent = round((completed / total) * 100, 1) if total > 0 else 0.0
    return {
        "project_id": project_id,
        "total_milestones": total,
        "completed_milestones": completed,
        "percent_complete": percent,
    }
