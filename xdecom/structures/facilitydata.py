from xdecom.utils import chunk_data
from struct import Struct
from dataclasses import dataclass
from enum import Enum


class LabSize(Enum):
    SMALL = 0
    LARGE = 1


class PrereqType(Enum):
    CRAFT_EQUIPMENT = 0
    AGENT_EQUIPMENT = 1
    ALIEN_LIFEFORM = 3
    NONE = 0xFF


class ResearchGroup(Enum):
    BIOCHEM = 0
    PHYSICS = 1


class AnyAllUnknown(Enum):
    ANY = 0
    ALL = 1
    UNKNOWN = 4


@dataclass
class FacilityData:
    cost: int
    image_offset: int
    size: int
    build_time: int
    maintainance_cost: int
    capacity: int
    unknown1: int
    unknown2: int
    id: int = None


struct = Struct("IBBHHHHH")


def dump(data: bytes):
    (
        cost,
        image_offset,
        size,
        build_time,
        maintainance_cost,
        capacity,
        unknown1,
        unknown2
    ) = struct.unpack(data)
    return FacilityData(
        cost,
        image_offset,
        size,
        build_time,
        maintainance_cost,
        capacity,
        unknown1,
        unknown2
    )


def dump_all(data: bytes):
    entries = [dump(d) for d in chunk_data(data, struct.size)]
    for id, e in enumerate(entries):
        e.id = id
    return entries
