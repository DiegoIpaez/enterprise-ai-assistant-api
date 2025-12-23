from fastapi import APIRouter

import src.app.ai_knowledge.ai_knowledge_controller as ai_knowledge

router = APIRouter(prefix="/api/v1")

router.include_router(ai_knowledge.router)
