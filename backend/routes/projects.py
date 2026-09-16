from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=list[schemas.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)


@router.post("/", response_model=schemas.ProjectOut, status_code=201)
def create_project(project: schemas.ProjectCreate, db: Session = Depends(get_db)):
    return crud.create_project(db, project)


@router.get("/{project_id}", response_model=schemas.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.patch("/{project_id}", response_model=schemas.ProjectOut)
def update_project(project_id: int, project: schemas.ProjectUpdate, db: Session = Depends(get_db)):
    db_project = crud.update_project(db, project_id, project)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.delete("/{project_id}", status_code=204)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.delete_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")


@router.get("/{project_id}/progress", response_model=schemas.ProjectProgress)
def project_progress(project_id: int, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.get_project_progress(db, project_id)


# ---- Milestones (nested under a project) ----

@router.get("/{project_id}/milestones", response_model=list[schemas.MilestoneOut])
def list_milestones(project_id: int, db: Session = Depends(get_db)):
    return crud.get_milestones(db, project_id)


@router.post("/{project_id}/milestones", response_model=schemas.MilestoneOut, status_code=201)
def create_milestone(project_id: int, milestone: schemas.MilestoneCreate, db: Session = Depends(get_db)):
    db_project = crud.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return crud.create_milestone(db, project_id, milestone)


@router.patch("/milestones/{milestone_id}", response_model=schemas.MilestoneOut)
def update_milestone(milestone_id: int, milestone: schemas.MilestoneUpdate, db: Session = Depends(get_db)):
    db_milestone = crud.update_milestone(db, milestone_id, milestone)
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return db_milestone


@router.delete("/milestones/{milestone_id}", status_code=204)
def delete_milestone(milestone_id: int, db: Session = Depends(get_db)):
    db_milestone = crud.delete_milestone(db, milestone_id)
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
