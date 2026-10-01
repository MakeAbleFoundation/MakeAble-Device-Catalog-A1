# 07 OPENSESAME3000 Jar Tool

- file: `Full Plates/07 OPENSESAME3000 Jar Tool - PETG x2.3mf`
- source: https://makerworld.com/en/models/90424-opensesame3000-jar-tool#profileId-96804
- reference 3mf: `Jar Opener (PETG)/opensesame.3mf`
- designer: cartyski
- material: PETG (PETG A1 Tuned)
- on the plate: 2 copies (2 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.12mm Fine @BBL A1 | 0.12 mm | 0.2 mm | 3 | 15% gyroid | off | auto_brim | 5/5 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `infill_combination` | 0 | **1** |
| `initial_layer_speed` | 50 | **40** |
| `overhang_totally_speed` | 10 | **50** |
| `sparse_infill_pattern` | grid | **gyroid** |
| `support_on_build_plate_only` | 0 | **1** |
| `support_type` | tree(auto) | **normal(auto)** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_loops` | 2 | **3** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 6h 26m 19s, 145.5 g, 116.4 cm3
- per copie: 58.22 cm3
- the designer's own file slices at 58.94 cm3 per copy (99% of that here)
- the model page quotes 74 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 2 copies, 5h 57m 26s, 147.1 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Notes
- Linked profile is the PLA one (0.12 mm, 3 walls, 15% gyroid). The designer publishes the same settings as a PETG profile, which is what this file is set up for since the folder says PETG.

