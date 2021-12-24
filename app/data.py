from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List
from app.models import *
from sqlalchemy import select


def dec(val):
    return Decimal(str(val))


def to_percents(all: int, partial: int):
    return round(dec(100) * dec(partial / all if all != 0 else 1), 2)


def get_age(born: date, at: date = date.today()):
    return at.year - born.year - ((at.month, at.day) < (born.month, born.day))


@dataclass
class TenantsStatisticData:
    count: int = 0
    ru_tenants_count: int = 0
    us_tenants_count: int = 0
    ua_tenants_count: int = 0

    ru_tenants_percentage: float = 0
    us_tenants_percentage: float = 0
    ua_tenants_percentage: float = 0

    age_0_13_count: int = 0
    age_14_20_count: int = 0
    age_21_35_count: int = 0
    age_36_50_count: int = 0
    age_51_70_count: int = 0
    age_71_99_count: int = 0

    age_0_13_percentage: float = 0
    age_14_20_percentage: float = 0
    age_21_35_percentage: float = 0
    age_36_50_percentage: float = 0
    age_51_70_percentage: float = 0
    age_71_99_percentage: float = 0

    @classmethod
    def create(cls, user_db=None):
        if not user_db:
            stmt = select(User)
            resp = sess.execute(stmt).scalars()
            print(resp)
        else: resp = [user_db]
        tenant_statistics_dto = TenantsStatisticData()
        for user in resp:
            for tenant in user.tenants:
                tenant_statistics_dto.count += 1
                # calculate doc_type count
                doc_type = tenant.doc_type.upper()
                if doc_type == 'Паспорт Российской Федерации'.upper():
                    tenant_statistics_dto.ru_tenants_count += 1
                elif doc_type == 'United States Passport'.upper():
                    tenant_statistics_dto.us_tenants_count += 1
                elif doc_type == 'Пасспорт України'.upper():
                    tenant_statistics_dto.ua_tenants_count += 1

                # calculate ages count
                age = get_age(tenant.date_of_birth)
                if age < 14:
                    tenant_statistics_dto.age_0_13_count += 1
                elif age < 21:
                    tenant_statistics_dto.age_14_20_count += 1
                elif age < 36:
                    tenant_statistics_dto.age_21_35_count += 1
                elif age < 51:
                    tenant_statistics_dto.age_36_50_count += 1
                elif age < 71:
                    tenant_statistics_dto.age_51_70_count += 1
                elif age < 100:
                    tenant_statistics_dto.age_71_99_count += 1

        # define doc_type percentage
        tenant_statistics_dto.ru_tenants_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.ru_tenants_count)
        tenant_statistics_dto.us_tenants_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.us_tenants_count)
        tenant_statistics_dto.ua_tenants_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.ua_tenants_count)

        # define ages percentage
        tenant_statistics_dto.age_0_13_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.age_0_13_count)
        tenant_statistics_dto.age_14_20_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.age_14_20_count)
        tenant_statistics_dto.age_21_35_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.age_21_35_count)
        tenant_statistics_dto.age_36_50_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.age_36_50_count)
        tenant_statistics_dto.age_51_70_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.age_51_70_count)
        tenant_statistics_dto.age_71_99_percentage = to_percents(tenant_statistics_dto.count, tenant_statistics_dto.age_71_99_count)

        return tenant_statistics_dto


@dataclass
class TenantInfoData:
    room_id: int = None
    full_name: str = None
    date_of_birth: date = None


@dataclass
class TenantsListData:
    tenants: List[TenantInfoData] = field(default_factory=list)

    @classmethod
    def create(cls, user):
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
