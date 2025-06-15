from fastapi import APIRouter, Depends, HTTPException, status
from app.config.db import get_db
from app.models.form import FormIn, Form
from app.models.form_response import FormResponse
from motor.motor_asyncio import AsyncIOMotorDatabase

router = APIRouter(prefix="/admin", tags=["Admin"])

async def _forms_collection(db: AsyncIOMotorDatabase):
    return db.forms

async def _responses_collection(db: AsyncIOMotorDatabase):
    return db.form_responses

@router.post("/forms", response_model=Form, status_code=status.HTTP_201_CREATED)
async def create_form(
    payload: FormIn,
    db: AsyncIOMotorDatabase = Depends(get_db),
):
    form_doc = Form(**payload.dict())
    await (await _forms_collection(db)).insert_one(form_doc.dict())
    # insert empty shared response
    resp_doc = FormResponse(form_id=form_doc.form_id)
    await (await _responses_collection(db)).insert_one(resp_doc.dict())
    return form_doc

@router.get("/forms/{form_id}", response_model=Form)
async def get_form(form_id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    doc = await (await _forms_collection(db)).find_one({"form_id": form_id})
    if not doc:
        raise HTTPException(404, detail="Form not found")
    return Form(**doc)
