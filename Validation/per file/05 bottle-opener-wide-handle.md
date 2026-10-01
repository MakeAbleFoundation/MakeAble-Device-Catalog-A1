# 05 Bottle Opener (three sizes, wide handle)

- file: `Full Plates/05 Bottle Opener (three sizes, wide handle) - PETG x4.3mf`
- source: https://makerworld.com/en/models/712423-bottle-opener-three-sizes-wider-handle#profileId-642822
- reference 3mf: `Bottle Opener (PETG)/Bottle+Opener+remix+without+support+material.3mf`
- designer: val
- material: PETG (PETG A1 Tuned)
- on the plate: 4 copies (4 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Strength @BBL A1 | 0.2 mm | 0.2 mm | 5 | 15% honeycomb | on normal(auto) | auto_brim | 5/3 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `independent_support_layer_height` | 1 | **0** |
| `overhang_totally_speed` | 10 | **50** |
| `sparse_infill_pattern` | grid | **cubic** |
| `support_type` | tree(auto) | **normal(auto)** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_sequence` | inner wall/outer wall | **outer wall/inner wall** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 7h 9m 44s, 139.6 g, 111.7 cm3
- per copie: 27.92 cm3
- the designer's own file slices at 29.40 cm3 per copy (95% of that here)
- the model page quotes 35 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 4 copies, 6h 46m 6s, 141.1 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Notes
- The designer's per-object settings (5 walls, 15% honeycomb, supports on, seam at the back) are carried over per object, as in the original.

