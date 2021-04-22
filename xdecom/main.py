from pathlib import Path
import json
from enum import Enum
from xdecom import offsets
from xdecom.utils import read_data
from xdecom.structures import strtab, researchdata, facilitydata


def to_json(o):
    if isinstance(o, Enum):
        return o.name
    return o.__dict__


def dump_json(o, f):
    return json.dump(o, f, indent=4, default=to_json)


def decom(f):
    outpath = Path("out")
    outpath.mkdir(parents=True, exist_ok=True)
    names = strtab.dump(read_data(f, *offsets.RESEARCH_NAME_STRTAB))
    descriptions = strtab.dump(read_data(f, *offsets.RESEARCH_DESCRIPTION_STRTAB))
    entries = researchdata.dump_all(read_data(f, *offsets.RESEARCH_DATA))
    for n, r in enumerate(entries):
        r.name = names[n]
        r.description = descriptions[n]
    with (outpath / "research.json").open("w") as outf:
        dump_json(entries, outf)

    equipment = strtab.dump(read_data(f, *offsets.AGENT_EQUIPMENT_NAMES))
    with (outpath / "equipment.json").open("w") as outf:
        dump_json(equipment, outf)

    agents = strtab.dump(read_data(f, *offsets.AGENT_TYPE_NAMES))
    with (outpath / "agents.json").open("w") as outf:
        dump_json(agents, outf)

    strtabs = strtab.dump_all(read_data(f, *offsets.STRTABS))
    with (outpath / "strtabs.json").open("w") as outf:
        dump_json(strtabs, outf)

    facilitydatas = facilitydata.dump_all(read_data(f, *offsets.FACILITY_DATA))
    with (outpath / "facilitydata.json").open("w") as outf:
        dump_json(facilitydatas, outf)


def main():
    exepath = Path("data/UFO2P.EXE")
    with exepath.open("rb") as f:
        decom(f)


if __name__ == "__main__":
    main()
