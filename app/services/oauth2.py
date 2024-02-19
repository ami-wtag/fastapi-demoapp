from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.services import token
from app.db.base import engine
from app.db.base import get_db

import casbin
import casbin_sqlalchemy_adapter


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/oauth-login")
adapter = casbin_sqlalchemy_adapter.Adapter(engine)


def get_current_user(
    data,
    db
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    ret = token.verify_token(data, credentials_exception, db)
    return ret


def get_current_user_authorization(request, current_user):
    enforcer = casbin.Enforcer("core/model.conf", adapter)
    sub = current_user.email
    dom = current_user.organization_name
    obj = request.url.path
    act = request.method
    if not (enforcer.enforce(sub, dom, obj, act)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Method not authorized for this user")
    return current_user


def add_new_role_in_org(email: str, role: str, dom: str, db: Session = Depends(get_db)) -> None:
    enforcer = casbin.Enforcer("core/model.conf", adapter)
    enforcer.add_role_for_user_in_domain(email, role, dom)
    db.commit()  # Ensure changes are persisted


def get_current_user_info(
    data: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    ret = token.get_user(data, db)
    return ret