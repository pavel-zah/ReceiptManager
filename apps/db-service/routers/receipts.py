from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Receipt, ReceiptItem
from schemas import ReceiptCreate, ReceiptItemOut, ReceiptOut, ReceiptUpdate

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.post("/", response_model=ReceiptOut, status_code=201)
def create_receipt(payload: ReceiptCreate, db: Session = Depends(get_db)):
    if db.get(Receipt, payload.id):
        raise HTTPException(status_code=409, detail="Receipt already exists")
    receipt = Receipt(**payload.model_dump())
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    return receipt


@router.get("/{receipt_id}", response_model=ReceiptOut)
def get_receipt(receipt_id: str, db: Session = Depends(get_db)):
    receipt = db.get(Receipt, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt


@router.patch("/{receipt_id}", response_model=ReceiptOut)
def update_receipt(receipt_id: str, payload: ReceiptUpdate, db: Session = Depends(get_db)):
    receipt = db.get(Receipt, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(receipt, field, value)
    db.commit()
    db.refresh(receipt)
    return receipt


@router.delete("/{receipt_id}", status_code=204)
def delete_receipt(receipt_id: str, db: Session = Depends(get_db)):
    receipt = db.get(Receipt, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    db.delete(receipt)
    db.commit()


@router.get("/{receipt_id}/items", response_model=list[ReceiptItemOut])
def list_receipt_items(receipt_id: str, db: Session = Depends(get_db)):
    receipt = db.get(Receipt, receipt_id)
    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt.items
