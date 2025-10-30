from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.database import SessionLocal
import app.models as models
import app.schemas as schemas
from app.utils import decode_token
from typing import List
from fastapi import Header

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=401, detail='Missing Authorization header')
    parts = authorization.split()
    token = parts[1] if len(parts) > 1 else parts[0]
    try:
        data = decode_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail='Invalid token')
    user = db.query(models.User).filter(models.User.id == data.get('id')).first()
    if not user:
        raise HTTPException(status_code=401, detail='User not found')
    return user

@router.post('/', response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task_obj = models.Task(title=task.title, description=task.description, owner_id=current_user.id)
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.get('/', response_model=List[schemas.TaskOut])
def list_tasks(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role == 'admin':
        tasks = db.query(models.Task).all()
    else:
        tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks

@router.put('/{task_id}', response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task_obj = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail='Task not found')
    if task_obj.owner_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Forbidden')
    task_obj.title = task.title
    task_obj.description = task.description
    db.commit()
    db.refresh(task_obj)
    return task_obj

@router.delete('/{task_id}')
def delete_task(task_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    task_obj = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail='Task not found')
    if task_obj.owner_id != current_user.id and current_user.role != 'admin':
        raise HTTPException(status_code=403, detail='Forbidden')
    db.delete(task_obj)
    db.commit()
    return {'msg': 'deleted'}
