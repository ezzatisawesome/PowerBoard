from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

STALE_FOOTPRINT_UUIDS = {
    # Duplicate PCB footprints that do not match the current schematic/BOM.
    "c2b082c0-cbe0-49fb-b7d8-9f3308b01e7e",  # R24, stale 33k
    "9df02c5c-3266-4f0e-83ed-10f95c1778d7",  # R25, stale 33k
    "eeaed5f6-28ea-46b7-8112-2131a9ba0f7f",  # R39, stale generic R
    "2b3dc3e4-18af-4d3a-9173-bcaca6699c77",  # R41, stale generic R
}

CLEARANCE_VIA_UUIDS = {
    # Ground stitching vias called out by DRC as 0.10 mm from SY_B.PGOOD.
    "039ca915-0285-4f67-8e48-ff4517b4dfed",
    "07678364-9241-477c-971e-c7688b62853a",
    "917d504f-bac2-44f4-9167-f5547db0bbe8",
}

DANGLING_SEGMENT_UUIDS = {
    # Leftover stubs after stale duplicate footprints and USB-C duplicate-pin cleanup.
    "e41f6cc8-f862-4c06-a573-643a9e5a2222",
    "9b69aeaa-28b1-439f-a1fb-03f452acc083",
    "e288bab8-b0d5-4ab4-ba43-b206f551aa1c",
    "c914d47c-6e81-4e5b-ba67-ffe9b6f374a2",
    "8ebad9da-51fe-4d03-940d-b436a265f65d",
    "65e89cd7-b701-4f2c-b9a9-05c9e5d0f214",
    "c2e7422e-b1b0-425a-a9d3-2a24138d91e2",
    "71f0ecc4-84c9-4db8-8577-a76326a1e601",
    "a69adc6a-1676-4a86-825e-6e68484cbd5b",
    "b573e6d6-7b7e-40b3-93d2-88de61c7c48a",
}

DUPLICATE_VIA_UUIDS = {
    # Exact co-located duplicate via; keep the other via at the same coordinate/net.
    "e1d0ca53-a5c9-498f-8574-de38e797b304",
}

DNP_REFS = {"TP1", "TP2", "J6", "J7", "J11", "J12"}

USB_LABEL_UUIDS = {
    "6845b5ef-7a2b-4fd5-83f0-a9ce55fd2001",
    "d8c06335-7b59-4b3c-91e1-877f98b4e031",
    "f8395330-0897-49e3-a57b-83b5998d3a1c",
    "3d48ba9d-fb45-44dd-ae54-e8076b46b419",
    "f5c1d8f4-474b-4f27-b71a-1915318f970c",
    "e62ef08f-c7d5-4820-bf45-0f950a69908d",
    "d11c1254-cefb-4e51-9d5f-9578397197cf",
    "c43d5e74-b131-4c05-b639-7c3087f25eac",
}

USB_REPAIR_UUIDS = {
    f"4ab4707c-53cd-426d-a95a-fb1053efc00{x}" for x in "123456789abcdef"
} | {
    "4ab4707c-53cd-426d-a95a-fb1053efc010",
    "4ab4707c-53cd-426d-a95a-fb1053efc011",
    "4ab4707c-53cd-426d-a95a-fb1053efc012",
    "4ab4707c-53cd-426d-a95a-fb1053efc013",
}

USB_REPAIR_SEGMENTS = """
	(segment
		(start 126.17 101.9)
		(end 127.9 101.9)
		(width 0.2)
		(layer "F.Cu")
		(net 204)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc001")
	)
	(segment
		(start 125.4 101.9)
		(end 126.17 101.9)
		(width 0.2)
		(layer "F.Cu")
		(net 204)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc002")
	)
	(segment
		(start 125.4 104.4)
		(end 127.9 104.4)
		(width 0.2)
		(layer "F.Cu")
		(net 204)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc013")
	)
	(via
		(at 125.4 104.4)
		(size 0.5)
		(drill 0.25)
		(layers "F.Cu" "B.Cu")
		(net 204)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc003")
	)
	(via
		(at 125.4 101.9)
		(size 0.5)
		(drill 0.25)
		(layers "F.Cu" "B.Cu")
		(net 204)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc004")
	)
	(segment
		(start 125.4 104.4)
		(end 125.4 101.9)
		(width 0.2)
		(layer "In2.Cu")
		(net 204)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc012")
	)
	(segment
		(start 127.9 105.9)
		(end 129.19 105.55)
		(width 0.2)
		(layer "F.Cu")
		(net 1)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc005")
	)
	(segment
		(start 126.17 105.9)
		(end 124.89 105.55)
		(width 0.2)
		(layer "F.Cu")
		(net 1)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc006")
	)
	(segment
		(start 126.17 103.4)
		(end 126.95 103.6)
		(width 0.1)
		(layer "F.Cu")
		(net 208)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc007")
	)
	(via
		(at 126.95 103.6)
		(size 0.5)
		(drill 0.25)
		(layers "F.Cu" "B.Cu")
		(net 208)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc008")
	)
	(segment
		(start 126.95 103.6)
		(end 132 104.5)
		(width 0.1)
		(layer "In1.Cu")
		(net 208)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc009")
	)
	(via
		(at 132 104.5)
		(size 0.5)
		(drill 0.25)
		(layers "F.Cu" "B.Cu")
		(net 208)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc00a")
	)
	(segment
		(start 132 104.5)
		(end 132.4 105.181802)
		(width 0.1)
		(layer "F.Cu")
		(net 208)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc00b")
	)
	(segment
		(start 126.17 102.9)
		(end 127.9 103.4)
		(width 0.1)
		(layer "F.Cu")
		(net 209)
		(uuid "4ab4707c-53cd-426d-a95a-fb1053efc00c")
	)
"""


def sexpr_end(text: str, start: int) -> int:
    depth = 0
    in_string = False
    escape = False
    for i in range(start, len(text)):
        ch = text[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue
        if ch == '"':
            in_string = True
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return i + 1
    raise ValueError(f"unclosed s-expression at {start}")


def rewrite_top_blocks(text: str, token: str, edit):
    out = []
    pos = 0
    marker = f"\n\t({token}"
    while True:
        idx = text.find(marker, pos)
        if idx < 0:
            break
        start = idx + 1
        end = sexpr_end(text, start)
        out.append(text[pos:start])
        block = text[start:end]
        repl = edit(block)
        if repl is not None:
            out.append(repl)
        pos = end
    out.append(text[pos:])
    return "".join(out)


def remove_blocks_by_uuid(text: str, token: str, uuids: set[str]):
    removed = []

    def edit(block):
        m = re.search(r'\(uuid "([^"]+)"\)', block)
        if m and m.group(1) in uuids:
            removed.append(m.group(1))
            return None
        return block

    return rewrite_top_blocks(text, token, edit), removed


def edit_usb2_footprint(block: str) -> str:
    if '(property "Reference" "USB2"' not in block:
        return block

    replacements = {
        "A4": ('(net 204 "USB_VBUS_CONN")', "unspecified"),
        "A9": ('(net 204 "USB_VBUS_CONN")', "unspecified"),
        "B4": ('(net 204 "USB_VBUS_CONN")', "unspecified"),
        "B9": ('(net 204 "USB_VBUS_CONN")', "unspecified"),
        "A12": ('(net 1 "GND")', "unspecified"),
        "B1": ('(net 1 "GND")', "unspecified"),
        "B6": ('(net 208 "USB_D_P")', "unspecified"),
        "B7": ('(net 209 "USB_D_N")', "unspecified"),
    }

    def edit_pad(pin, m):
        pad = m.group(0)
        net, pintype = replacements[pin]
        pad = re.sub(r'\(net \d+ "[^"]*"\)', net, pad, count=1)
        pad = re.sub(r'\(pintype "[^"]*"\)', f'(pintype "{pintype}")', pad, count=1)
        return pad

    for pin in replacements:
        block = re.sub(
            rf'\(pad "{re.escape(pin)}"[\s\S]*?\n\t\t\)',
            lambda m, pin=pin: edit_pad(pin, m),
            block,
            count=1,
        )

    block = block.replace(
        "/Users/omarreyes/Desktop/PowerBoard/.claude/worktrees/bold-ellis-d5c4e0/libs/",
        "${KIPRJMOD}/libs/",
    )
    return block


def fill_lcsc_in_block(block: str) -> str:
    supplier = re.search(r'\(property "Supplier_1 P/N" "(C\d+)"', block)
    if not supplier:
        return block
    part = supplier.group(1)
    if re.search(r'\(property "LCSC Part" ""', block):
        return re.sub(r'\(property "LCSC Part" ""', f'(property "LCSC Part" "{part}"', block, count=1)
    if '(property "LCSC Part"' not in block:
        prop_start = block.find('(property "Supplier_1 P/N"')
        prop_end = sexpr_end(block, prop_start)
        prop = block[prop_start:prop_end]
        new_prop = prop.replace('Supplier_1 P/N', 'LCSC Part', 1)
        block = block[:prop_end] + "\n\t\t" + new_prop + block[prop_end:]
    return block


def edit_release_footprint(block: str) -> str:
    block = edit_usb2_footprint(block)
    block = fill_lcsc_in_block(block)
    ref = re.search(r'\(property "Reference" "([^"]+)"', block)
    if ref and ref.group(1) in DNP_REFS:
        block = re.sub(
            r'\(attr ([^)]*)\)',
            lambda m: m.group(0) if "dnp" in m.group(1).split() else f'(attr {m.group(1)} dnp)',
            block,
            count=1,
        )
    return block


def mark_dnp_symbols(text: str) -> str:
    def edit(block):
        ref = re.search(r'\(property "Reference" "([^"]+)"', block)
        if ref and ref.group(1) in DNP_REFS:
            block = block.replace("(dnp no)", "(dnp yes)", 1)
        return fill_lcsc_in_block(block)

    return rewrite_top_blocks(text, "symbol", edit)


def mark_usb_no_connects(text: str) -> str:
    # Keep SBU pins no-connect. Tie orientation-duplicate D+/D-, VBUS, and GND pins.
    text, _ = remove_blocks_by_uuid(text, "global_label", USB_LABEL_UUIDS)
    text, _ = remove_blocks_by_uuid(text, "label", USB_LABEL_UUIDS)
    for x, y in [
        ("48.26", "95.25"),   # A9 VBUS
        ("48.26", "97.79"),   # A12 GND
        ("48.26", "100.33"),  # B1 GND
        ("48.26", "102.87"),  # B4 VBUS
        ("48.26", "107.95"),  # B6 DP2
        ("48.26", "110.49"),  # B7 DN2
        ("48.26", "115.57"),  # B9 VBUS
    ]:
        text = re.sub(
            rf'\n\t\(no_connect\n\t\t\(at {x} {y}\)\n\t\t\(uuid "[^"]+"\)\n\t\)',
            "",
            text,
        )
    additions = """
	(global_label "USB_VBUS_CONN"
		(shape passive)
		(at 48.26 82.55 180)
		(effects (font (size 1.27 1.27)) (justify right))
		(uuid "6845b5ef-7a2b-4fd5-83f0-a9ce55fd2001")
	)
	(global_label "USB_VBUS_CONN"
		(shape passive)
		(at 48.26 95.25 180)
		(effects (font (size 1.27 1.27)) (justify right))
		(uuid "d8c06335-7b59-4b3c-91e1-877f98b4e031")
	)
	(global_label "GND"
		(shape input)
		(at 48.26 97.79 180)
		(effects (font (size 1.27 1.27)) (justify right))
		(uuid "f8395330-0897-49e3-a57b-83b5998d3a1c")
	)
	(global_label "GND"
		(shape input)
		(at 48.26 100.33 180)
		(effects (font (size 1.27 1.27)) (justify right))
		(uuid "3d48ba9d-fb45-44dd-ae54-e8076b46b419")
	)
	(global_label "USB_VBUS_CONN"
		(shape passive)
		(at 48.26 102.87 180)
		(effects (font (size 1.27 1.27)) (justify right))
		(uuid "f5c1d8f4-474b-4f27-b71a-1915318f970c")
	)
	(global_label "USB_D_P"
		(shape input)
		(at 48.26 107.95 180)
		(effects (font (size 1.27 1.27)) (justify right))
		(uuid "e62ef08f-c7d5-4820-bf45-0f950a69908d")
	)
	(global_label "USB_D_N"
		(shape input)
		(at 48.26 110.49 180)
		(effects (font (size 1.27 1.27)) (justify right))
		(uuid "d11c1254-cefb-4e51-9d5f-9578397197cf")
	)
	(global_label "USB_VBUS_CONN"
		(shape passive)
		(at 48.26 115.57 180)
		(effects (font (size 1.27 1.27)) (justify right))
		(uuid "c43d5e74-b131-4c05-b639-7c3087f25eac")
	)
"""
    insert_at = text.find("\n\t(no_connect")
    if insert_at != -1:
        text = text[:insert_at] + additions + text[insert_at:]
    return text


def ensure_usb_repair_copper(pcb: str) -> str:
    if "4ab4707c-53cd-426d-a95a-fb1053efc010" in pcb:
        return pcb
    insert_at = pcb.find("\n\t(zone")
    if insert_at == -1:
        raise ValueError("could not find zone section for USB repair copper insertion")
    return pcb[:insert_at] + USB_REPAIR_SEGMENTS + pcb[insert_at:]


def main():
    pcb_path = ROOT / "PowerBoard.kicad_pcb"
    pcb = pcb_path.read_text()
    pcb, removed_fp = remove_blocks_by_uuid(pcb, "footprint", STALE_FOOTPRINT_UUIDS)
    pcb, removed_via = remove_blocks_by_uuid(pcb, "via", CLEARANCE_VIA_UUIDS)
    pcb, removed_dup_via = remove_blocks_by_uuid(pcb, "via", DUPLICATE_VIA_UUIDS)
    pcb, removed_seg = remove_blocks_by_uuid(pcb, "segment", DANGLING_SEGMENT_UUIDS)
    pcb, _ = remove_blocks_by_uuid(pcb, "via", USB_REPAIR_UUIDS)
    pcb, _ = remove_blocks_by_uuid(pcb, "segment", USB_REPAIR_UUIDS)
    pcb = rewrite_top_blocks(pcb, "footprint", edit_release_footprint)
    pcb = pcb.replace('"Net-(D9-K)"', '"USB_VBUS_CONN"')
    pcb = ensure_usb_repair_copper(pcb)
    pcb = pcb.replace('(copper_finish "None")', '(copper_finish "ENIG")')
    pcb = pcb.replace(
        "/Users/omarreyes/Desktop/PowerBoard/.claude/worktrees/bold-ellis-d5c4e0/libs/",
        "${KIPRJMOD}/libs/",
    )
    pcb_path.write_text(pcb)

    pro_path = ROOT / "PowerBoard.kicad_pro"
    pro = pro_path.read_text()
    pro = re.sub(r'("zones": \{\n\s+"min_clearance": )(?:0\.0|0\.09|0\.099|0\.15|0\.159)(?=,|\n)', r"\g<1>0.09", pro)
    pro = re.sub(r'("rules": \{[\s\S]*?"min_clearance": )(?:0\.0|0\.09|0\.099|0\.15|0\.159)(?=,|\n)', r"\g<1>0.09", pro, count=1)
    pro_path.write_text(pro)

    for sch_path in ROOT.glob("*.kicad_sch"):
        text = sch_path.read_text()
        text = mark_dnp_symbols(text)
        if sch_path.name == "io.kicad_sch":
            text = mark_usb_no_connects(text)
        sch_path.write_text(text)

    print(f"removed stale footprints: {sorted(removed_fp)}")
    print(f"removed clearance vias: {sorted(removed_via)}")
    print(f"removed duplicate vias: {sorted(removed_dup_via)}")
    print(f"removed dangling segments: {sorted(removed_seg)}")


if __name__ == "__main__":
    main()
