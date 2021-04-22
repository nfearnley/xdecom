from typing import Tuple
from enum import Enum
from dataclasses import dataclass
from struct import Struct

from xdecom.utils import chunk_data, noneif


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
class ResearchEntry:
    labSize: LabSize            # 0 = small, 1 = large
    unknown1: int
    anyall: AnyAllUnknown
    prereqType: int         # 0 = craft equipment, 1 = agent equipment, 3 = alien life form, 0xff = nune
    unknown3: int
    prereq: int
    leadsTo1: int
    leadsTo2: int
    prereqTech: Tuple[int, int, int]   # IDX into research list, 0xffff for none
    score: int
    skillHours: int
    researchGroup: ResearchGroup      # 0 = BioChem, 1 = Quantum Phys
    ufopaediaGroup: int
    ufopaediaEntry: int
    id: int = None
    name: str = ""
    description: str = ""


struct = Struct("BBBBHHHH3HHIBBH")


def dump(data: bytes):
    (
        labSize,
        unknown1,
        anyall,
        prereqType,
        unknown3,
        prereq,
        leadsTo1,
        leadsTo2,
        prereqTech1,
        prereqTech2,
        prereqTech3,
        score,
        skillHours,
        researchGroup,
        ufopaediaGroup,
        ufopaediaEntry
    ) = struct.unpack(data)
    return ResearchEntry(
        LabSize(labSize),
        unknown1,
        AnyAllUnknown(anyall),
        PrereqType(prereqType),
        unknown3,
        noneif(prereq, 0xFFFF),
        noneif(leadsTo1, 0xFFFF),
        noneif(leadsTo2, 0xFFFF),
        (noneif(prereqTech1, 0xFFFF), noneif(prereqTech2, 0xFFFF), noneif(prereqTech3, 0xFFFF)),
        score,
        skillHours,
        ResearchGroup(researchGroup),
        ufopaediaGroup,
        ufopaediaEntry
    )


def dump_all(data: bytes):
    entries = [dump(d) for d in chunk_data(data, struct.size)]
    for id, e in enumerate(entries):
        e.id = id
    return entries
