# 19 Arthritis Toothbrush Grip

- file: `Full Plates/19 Arthritis Toothbrush Grip - PLA x17.3mf`
- source: https://www.myminifactory.com/object/3d-print-arthritis-toothbrush-grip-77601
- reference 3mf: `Toothbrush Grip (PLA)/6066726cbda58_arthritis-toothbrush-grip/toofbrushgrip.stl`
- designer: MyMiniFactory
- material: PLA (Bambu PLA Basic @BBL A1)
- on the plate: 17 copies (17 objects)
- print-time cap: 25 copies fit on the plate; trimmed to 17 to stay under 14 h on the A1

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 2 | 15% grid | off | outer_only | 5/3 |

## Validation
- Orca slice: passed - 13h 40m 56s, 538.3 g, 427.2 cm3
- per copie: 25.13 cm3
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 19 copies, 13h 23m 17s, 599.3 g
- 19 copies ran 15h 13m 25s on the A1, over the 14 h cap: trimmed to 17, keeping the ones nearest the middle of the plate; nothing that stayed was moved
- Arthritis Toothbrush Grip: outer brim added (the A1 moves the bed under the part, and this one is tall for its footprint)
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Notes
- No designer profile exists; A1 0.20 mm Standard used.
- Heavy part: check the reported filament weight before starting a full plate.

