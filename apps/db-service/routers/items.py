from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import ItemAssignment, Receipt, ReceiptItem, User
from schemas import AssignmentOut, ReceiptItemCreate, ReceiptItemOut, ReceiptItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.post("/", response_model=ReceiptItemOut, status_code=201)
def create_item(payload: ReceiptItemCreate, db: Session = Depends(get_db)):
    if not db.get(Receipt, payload.receipt_id):
        raise HTTPException(status_code=404, detail="Receipt not found")
    item = ReceiptItem(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/{item_id}", response_model=ReceiptItemOut)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(ReceiptItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.patch("/{item_id}", response_model=ReceiptItemOut)
def update_item(item_id: int, payload: ReceiptItemUpdate, db: Session = Depends(get_db)):
    item = db.get(ReceiptItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.get(ReceiptItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()


# ── Assignments ───────────────────────────────────────────────────────────────

@router.get("/{item_id}/assignments", response_model=list[AssignmentOut])
def list_assignments(item_id: int, db: Session = Depends(get_db)):
    item = db.get(ReceiptItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item.assignments


@router.post("/{item_id}/assignments/{user_id}", response_model=AssignmentOut, status_code=201)
def assign_item(item_id: int, user_id: int, db: Session = Depends(get_db)):
    if not db.get(ReceiptItem, item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    if not db.get(User, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if db.get(ItemAssignment, (item_id, user_id)):
        raise HTTPException(status_code=409, detail="Assignment already exists")
    assignment = ItemAssignment(item_id=item_id, user_id=user_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


@router.delete("/{item_id}/assignments/{user_id}", status_code=204)
def remove_assignment(item_id: int, user_id: int, db: Session = Depends(get_db)):
    assignment = db.get(ItemAssignment, (item_id, user_id))
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(assignment)
    db.commit()
