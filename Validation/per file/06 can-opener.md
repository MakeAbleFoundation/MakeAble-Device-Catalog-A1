# 06 Assistive Can Tab Opener

- file: `Full Plates/06 Assistive Can Tab Opener - PLA x30.3mf`
- source: https://makerworld.com/en/models/1797256-assistive-can-tab-opener#profileId-1916191
- reference 3mf: `Can Opener (PLA)/Base_Can_Opener.3mf`
- designer: MakeAble
- material: PLA (Bambu PLA Basic @BBL A1)
- on the plate: 30 copies (30 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 2 | 50% grid | on tree(auto) | outer_only | 5/3 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `enable_support` | 0 | **1** |
| `skeleton_infill_density` | 15% | **50%** |
| `skin_infill_density` | 15% | **50%** |
| `sparse_infill_density` | 15% | **50%** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `flush_multiplier` | 0.62 | **0.75** |

## Validation
- Orca slice: passed - 13h 11m 39s, 366.1 g, 290.6 cm3
- per copie: 9.69 cm3
- the designer's own file slices at 9.57 cm3 per copy (101% of that here)
- the model page quotes 12 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 30 copies, 11h 8m 48s, 358.8 g
- Base_Can_Opener.stl: outer brim added (the A1 moves the bed under the part, and this one is tall for its footprint)
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

