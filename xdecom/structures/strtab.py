def dump(data: bytes):
    strtab = data.decode("ascii").split("\0")
    assert strtab[-1] == ""
    strtab.pop()
    return strtab


def dump_all(data: bytes):
    strtab_data = data.split(b"\0\0")
    assert strtab_data[-1] == b""
    strtab_data.pop()
    strtabs = [dump(d + b"\0") for d in strtab_data]
    return strtabs


if __name__ == "__main__":
    import json
    OFFSET_START = 0x1494ce
    OFFSET_END = 0x154e36
    with open("UFO2P.EXE", "rb") as f:
        f.seek(OFFSET_START, 0)
        data = f.read(OFFSET_END - OFFSET_START)
    sections = dump_all(data)
    print(json.dumps(sections, indent=4))
