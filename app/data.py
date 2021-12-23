from dataclasses import dataclass, field
from typing import List
from app.models import *
from sqlalchemy import select


@dataclass
class RoomData:
    pass


@dataclass
class RentData:
    available_room_ids: List[int] = field(default_factory=list)
    selected_room_ids: List[int] = field(default_factory=list)


def get_rent_data():
    sess = db.session
    stmt = select(Room).where(Room.busy == 0)
    resp = sess.execute(stmt).scalars()
    #rooms_db = [room_db for room_db in resp]

    rent_dto = RentData()
    for room_db in resp:
        rent_dto.available_room_ids.append(room_db.id)

    return rent_dto
