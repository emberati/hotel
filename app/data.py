from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List
from app.models import *
from sqlalchemy import select


def dec(val):
    return Decimal(str(val))


@dataclass
class TenantInfoData:
    room_id: int = None
    full_name: str = None
    date_of_birth: date = None


@dataclass
class TenantsListData:
    tenants: List[TenantInfoData] = field(default_factory=list)

    @classmethod
    def get_tenants_list_data(cls, user):
        tenants_db = user.tenants

        tenants_list_dto = TenantsListData()
        for tenant_db in tenants_db:
            tenants_list_dto.tenants.append(
                TenantInfoData(
                    full_name=tenant_db.full_name,
                    date_of_birth=tenant_db.date_of_birth
                )
            )
        return tenants_list_dto

@dataclass
class RoomData:
    id: int = None
    busy: bool = None
    cost: Decimal = None
    double_beds: int = None
    single_beds: int = None
    showers: int = None
    toilets: int = None


@dataclass
class RentData:
    available_rooms: List[RoomData] = field(default_factory=list)
    available_room_ids: List[int] = field(default_factory=list)
    selected_room_ids: List[int] = field(default_factory=list)


def get_rent_data():
    stmt = select(Room).where(Room.busy == 0)
    resp = sess.execute(stmt).scalars()
    #rooms_db = [room_db for room_db in resp]

    rent_dto = RentData()
    for room_db in resp:
        rent_dto.available_room_ids.append(room_db.id)
        rent_dto.available_rooms.append(
            RoomData(
                id=room_db.id,
                busy=room_db.busy,
                cost=dec(room_db.cost),
                double_beds=room_db.double_beds,
                single_beds=room_db.single_beds,
                showers=room_db.showers,
                toilets=room_db.toilets
            )
        )
    return rent_dto
