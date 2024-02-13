from fastapi import Request, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.services.oauth2 import get_current_user, get_current_user_authorization

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/oauth-login")


def casbin_auth_middleware(
    request: Request,
    call_next,
    data: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    open_paths = ["/api/login", "/api/oauth-login"]
    
    current_user = get_current_user(data, db)
    
    print('\n\n\n\n current user: ', current_user, '\n\n\n')

    if request.url.path not in open_paths:
        user = get_current_user_authorization(request, current_user)

    response = call_next(request)
    return response
