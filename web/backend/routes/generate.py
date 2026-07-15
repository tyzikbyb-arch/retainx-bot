import json
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import User, Generation, Transaction
from routes.auth import get_current_user

router = APIRouter(prefix="/generate", tags=["generate"])

MODELS = {
    "sora":     {"type": "video", "credits": 10, "fal_id": "fal-ai/sora"},
    "kling":    {"type": "video", "credits": 6,  "fal_id": "fal-ai/kling-video/v2/master/text-to-video"},
    "seedance": {"type": "video", "credits": 5,  "fal_id": "fal-ai/seedance-1-lite"},
    "wan":      {"type": "video", "credits": 4,  "fal_id": "fal-ai/wan/v2.1/1.3b/text-to-video"},
    "ltx":      {"type": "video", "credits": 3,  "fal_id": "fal-ai/ltx-video"},
    "minimax":  {"type": "video", "credits": 5,  "fal_id": "fal-ai/minimax/video-01"},
    "heygen":   {"type": "video", "credits": 10, "fal_id": "fal-ai/heygen-labs/video-translate"},
    "grok":     {"type": "image", "credits": 1,  "fal_id": "fal-ai/grok-aurora"},
    "flux":     {"type": "image", "credits": 2,  "fal_id": "fal-ai/flux-pro/v1.1"},
    "sdxl":     {"type": "image", "credits": 1,  "fal_id": "fal-ai/stable-diffusion-xl"},
    "eleven":   {"type": "audio", "credits": 2,  "fal_id": "fal-ai/elevenlabs/tts/turbo-v2"},
    "cartesia": {"type": "audio", "credits": 2,  "fal_id": "fal-ai/cartesia/tts"},
}


class GenerateRequest(BaseModel):
    model: str
    prompt: str
    settings: Optional[dict] = None
    is_public: bool = True


class GenerationResponse(BaseModel):
    id: int
    type: str
    model: str
    prompt: str
    credits_used: int
    status: str
    result_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


async def _run_generation(gen_id: int, fal_id: str, prompt: str, settings: dict, db: Session):
    import fal_client

    gen = db.query(Generation).filter(Generation.id == gen_id).first()
    if not gen:
        return

    try:
        gen.status = "processing"
        db.commit()

        result = await fal_client.run_async(fal_id, arguments={"prompt": prompt, **(settings or {})})

        url = None
        if isinstance(result, dict):
            url = (
                result.get("video", {}).get("url")
                or (result.get("images", [{}])[0].get("url") if result.get("images") else None)
                or result.get("audio", {}).get("url")
                or result.get("url")
            )

        gen.status = "done"
        gen.result_url = url
        gen.completed_at = datetime.utcnow()
        db.commit()

    except Exception:
        gen.status = "failed"
        db.commit()


@router.post("", response_model=GenerationResponse, status_code=202)
async def create_generation(
    body: GenerateRequest,
    background_tasks: BackgroundTasks,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if body.model not in MODELS:
        raise HTTPException(status_code=422, detail=f"Unknown model: {body.model}")

    meta = MODELS[body.model]
    cost = meta["credits"]

    if user.credits < cost:
        raise HTTPException(status_code=402, detail=f"Insufficient credits. Need {cost}, have {user.credits}.")

    user.credits -= cost
    gen = Generation(
        user_id=user.id,
        type=meta["type"],
        model=body.model,
        prompt=body.prompt,
        credits_used=cost,
        status="pending",
        is_public=body.is_public,
        settings=json.dumps(body.settings or {}),
    )
    db.add(gen)
    db.add(Transaction(user_id=user.id, type="spend", credits=-cost, description=f"{meta['type'].capitalize()} — {body.model}"))
    db.commit()
    db.refresh(gen)

    background_tasks.add_task(_run_generation, gen.id, meta["fal_id"], body.prompt, body.settings or {}, db)
    return gen


@router.get("/{gen_id}", response_model=GenerationResponse)
def get_generation(gen_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    gen = db.query(Generation).filter(Generation.id == gen_id, Generation.user_id == user.id).first()
    if not gen:
        raise HTTPException(status_code=404, detail="Generation not found")
    return gen


@router.get("", response_model=list[GenerationResponse])
def list_generations(skip: int = 0, limit: int = 20, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Generation).filter(Generation.user_id == user.id).order_by(Generation.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/gallery/public", response_model=list[GenerationResponse])
def public_gallery(skip: int = 0, limit: int = 30, db: Session = Depends(get_db)):
    return db.query(Generation).filter(Generation.is_public == True, Generation.status == "done").order_by(Generation.created_at.desc()).offset(skip).limit(limit).all()
