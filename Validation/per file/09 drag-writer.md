# 09 DRAG Assistive Writer (kit of 3)

- file: `Full Plates/09 DRAG Assistive Writer (kit of 3) - PLA x2.3mf`
- source: https://makerworld.com/en/models/869468-drag-assistive-writing-and-drawing-device#profileId-821115
- reference 3mf: `DRAG Assistive Writer (PLA)/DRAG+v2 (1).3mf`
- designer: PrintLab
- material: PLA (Bambu PLA Basic @BBL A1)
- on the plate: 2 kits (6 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 2 | 15% zig-zag | off | no_brim | 5/3 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `brim_type` | auto_brim | **no_brim** |
| `initial_layer_infill_speed` | 105 | **50** |
| `initial_layer_speed` | 50 | **15** |
| `overhang_totally_speed` | 10 | **50** |
| `sparse_infill_pattern` | grid | **zig-zag** |
| `support_type` | tree(auto) | **normal(auto)** |
| `tree_support_wall_count` | -1 | **0** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 4h 5m 12s, 146.5 g, 116.2 cm3
- per kit: 58.12 cm3
- the designer's own file slices at 58.06 cm3 per copy (100% of that here)
- the model page quotes 76 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 2 kits, 3h 39m 32s, 146.4 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Advisories (nothing changed)
- DRAG left plate: 98 mm2 of steep overhang with air under it (max drop 6.1 mm at z=9 mm) while supports are off in the designer's profile - worth a look at the preview
- DRAG right plate: 93 mm2 of steep overhang with air under it (max drop 12.9 mm at z=13 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- One kit = left + right + centre plate, as the maker guide specifies (plus 3x M3x20 screws, not printed).

