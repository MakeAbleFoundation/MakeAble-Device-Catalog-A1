# 01 Bag Carrier (Medium)

- file: `Full Plates/01 Bag Carrier (Medium) - PLA x4.3mf`
- source: https://makerworld.com/en/models/1715311-bag-carrier#profileId-1820526
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
- Orca slice: passed - 3h 22m 9s, 125.4 g, 99.5 cm3
- per copie: 24.88 cm3
- the designer's own file slices at 24.93 cm3 per copy (100% of that here)
- the model page quotes 32 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 4 copies, 3h 0m 37s, 125.4 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

