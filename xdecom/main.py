import json
from enum import Enum
from xdecom import offsets
from xdecom.utils import read_data
from xdecom.structures import strtab, research, facilitydata


def to_json(o):
    if isinstance(o, Enum):
        return o.name
    return o.__dict__


def dump_json(o, f):
    return json.dump(o, f, indent=4, default=to_json)


def decom(f):
    names = strtab.dump(read_data(f, *offsets.RESEARCH_NAME_STRTAB))
    descriptions = strtab.dump(read_data(f, *offsets.RESEARCH_DESCRIPTION_STRTAB))
    entries = research.dump_all(read_data(f, *offsets.RESEARCH_DATA))
    for n, r in enumerate(entries):
        r.name = names[n]
        r.description = descriptions[n]
    with open("out/research.json", "w") as f:
        dump_json(entries, f)

    equipment = strtab.dump(read_data(f, *offsets.AGENT_EQUIPMENT_NAMES))
    with open("out/equipment.json", "w") as f:
        dump_json(equipment, f)

    agents = strtab.dump(read_data(f, *offsets.AGENT_TYPE_NAMES))
    with open("out/agents.json", "w") as f:
        dump_json(agents, f)

    strtabs = strtab.dump_all(read_data(f, *offsets.STRTABS))
    with open("out/strtabs.json", "w") as f:
        dump_json(strtabs, f)

    facilitydatas = facilitydata.dump_all(read_data(f, *offsets.FACILITY_DATA))
    with open("out/facilitydata.json", "w") as f:
        dump_json(facilitydatas, f)


def main():
    with open("data/UFO2P.EXE", "rb") as f:
        decom(f)


if __name__ == "__main__":
    main()
