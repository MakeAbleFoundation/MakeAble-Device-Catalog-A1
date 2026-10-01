# 02 Bag Carrier (Small)

- file: `Full Plates/02 Bag Carrier (Small) - PLA x4.3mf`
- source: https://makerworld.com/en/models/1715311-bag-carrier
- reference 3mf: `Bag Carrier (PLA)/Bag+Carrier+Medium.3mf`
- designer: MakeAble
- material: PLA (Bambu PLA Basic @BBL A1)
- on the plate: 4 copies (4 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 2 | 15% grid | off | auto_brim | 5/3 |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `flush_multiplier` | 0.62 | **0.75** |

## Validation
- Orca slice: passed - 3h 1m 10s, 112.5 g, 89.3 cm3
- per copie: 22.32 cm3
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 4 copies, 2h 41m 50s, 112.5 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Notes
- Mesh from All+bag+carriers.3mf; settings from the linked Medium profile (the designer uses the same 0.2 mm / 2 walls / 15% profile for all sizes).

