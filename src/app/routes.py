from fastapi import APIRouter

import src.app.ai_knowledges.ai_knowledges_controller as ai_knowledges_router

router = APIRouter(prefix="/api/v1")

router.include_router(ai_knowledges_router.router)
