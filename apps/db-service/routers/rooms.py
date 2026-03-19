from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Room, RoomParticipant, User
from schemas import ParticipantOut, RoomCreate, RoomOut, RoomUpdate

router = APIRouter(prefix="/rooms", tags=["rooms"])


@router.post("/", response_model=RoomOut, status_code=201)
def create_room(payload: RoomCreate, db: Session = Depends(get_db)):
    if not db.get(User, payload.creator_id):
        raise HTTPException(status_code=404, detail="Creator user not found")
    room = Room(**payload.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room


@router.get("/{room_id}", response_model=RoomOut)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room


@router.patch("/{room_id}", response_model=RoomOut)
def update_room(room_id: int, payload: RoomUpdate, db: Session = Depends(get_db)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(room, field, value)
    db.commit()
    db.refresh(room)
    return room


@router.delete("/{room_id}", status_code=204)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(room)
    db.commit()


# ── Participants ──────────────────────────────────────────────────────────────

@router.get("/{room_id}/participants", response_model=list[ParticipantOut])
def list_participants(room_id: int, db: Session = Depends(get_db)):
    room = db.get(Room, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room.participants


@router.post("/{room_id}/participants/{user_id}", response_model=ParticipantOut, status_code=201)
def add_participant(room_id: int, user_id: int, db: Session = Depends(get_db)):
    if not db.get(Room, room_id):
        raise HTTPException(status_code=404, detail="Room not found")
    if not db.get(User, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    existing = db.get(RoomParticipant, (room_id, user_id))
    if existing:
        raise HTTPException(status_code=409, detail="User already in room")
    participant = RoomParticipant(room_id=room_id, user_id=user_id)
    db.add(participant)
    db.commit()
    db.refresh(participant)
    return participant


@router.delete("/{room_id}/participants/{user_id}", status_code=204)
def remove_participant(room_id: int, user_id: int, db: Session = Depends(get_db)):
    participant = db.get(RoomParticipant, (room_id, user_id))
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    db.delete(participant)
    db.commit()
