from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import time
from sqlalchemy.orm import Session
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from app.db.base import get_db
from app.services.oauth2 import get_current_user, get_current_user_authorization

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/oauth-login")


class CustomAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self,
            request: Request,
            call_next: RequestResponseEndpoint,
            data: str = Depends(oauth2_scheme),
            db: Session = Depends(get_db)):
        open_paths = ["/api/login", "/api/oauth-login"]
        print('\n\n\n\n Data: ', data, '\n\n\nDB: ', db, '\n\n\n')
        # if data and db and request.url.path not in open_paths:
        #     current_user = get_current_user(data, db)
        #     print('\n\n\n\n current user: ', current_user, '\n\n\n')
        #     user = get_current_user_authorization(request, current_user)
        #     print('\n\n\n\n current user: ', user, '\n\n\n')
        print('\n\n\n\n Entered ... \n\n\n\n')
        start_time = time.time()
        response = await call_next(request)
        print(response)
        process_time = time.time() - start_time
        response.headers['X-Process-Time'] = str(process_time)
        print('\n\n\n\n Process Time: ', process_time, '\n\n\n\n')
        return response
