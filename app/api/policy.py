from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db.base import get_db
from app.db.crud import CRUDBase
from app.services.oauth2 import get_current_user_info


policy_router = APIRouter(prefix='/policy', tags=['Policy'])
policy_crud = CRUDBase(model=models.CasbinRule)


@policy_router.post('', response_model=schemas.CasbinRolePolicy)
def create_policy(
    new_policy: schemas.CasbinRolePolicy,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_info)
):
    new_policy.model_dump()
    policy = policy_crud.create(db=db, obj_in=new_policy)
    return policy


@policy_router.delete('')
def create_policy(
    id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user_info)
):
    policy_crud.remove(db=db, id=id)
    return 'Deleted'
