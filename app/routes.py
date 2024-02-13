from fastapi import APIRouter
from app.api.user import user_router
from app.api.auth import auth_router
from app.api.blog import blog_router
from app.api.token import token_router
from app.api.mail import mail_router
from app.api.invitation import invitation_router
from app.api.policy import policy_router


router = APIRouter(prefix='/api')
router.include_router(user_router)
router.include_router(auth_router)
router.include_router(blog_router)
router.include_router(token_router)
router.include_router(mail_router)
router.include_router(invitation_router)
router.include_router(policy_router)