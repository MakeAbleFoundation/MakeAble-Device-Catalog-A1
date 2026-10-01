# 43 Hand Press / Grip Strengthener (Hard)

- file: `Full Plates/43 Hand Press - Grip Strengthener (Hard) - PETG x5.3mf`
- source: https://makerworld.com/en/models/531052-hand-press-grip-strengthening#profileId-447870
- reference 3mf: `New Devices/Fingergrip+Press (1).3mf`
- designer: Sakul
- license: MakerWorld Standard Digital File License
- material: PETG (PETG A1 Tuned)
- on the plate: 5 copies (5 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 6 | 15% triangles | off | auto_brim | 6/6 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `bottom_shell_layers` | 3 | **6** |
| `brim_object_gap` | 0.1 | **0** |
| `brim_width` | 5 | **7** |
| `detect_thin_wall` | 0 | **1** |
| `ironing_flow` | 10% | **20%** |
| `overhang_totally_speed` | 10 | **50** |
| `sparse_infill_pattern` | grid | **triangles** |
| `support_on_build_plate_only` | 0 | **1** |
| `support_type` | tree(auto) | **normal(auto)** |
| `top_shell_layers` | 5 | **6** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_loops` | 2 | **5** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |
| `top_area_threshold` | 100% | **200%** |

## Validation
- Orca slice: passed - 8h 29m 26s, 241.4 g, 193.1 cm3
- per copie: 38.62 cm3
- the designer's own file slices at 39.21 cm3 per copy (99% of that here)
- the model page quotes 49 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 5 copies, 8h 13m 43s, 243.9 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Advisories (nothing changed)
- Fingergrip Press Hard.stl: 67 mm2 of steep overhang with air under it (max drop 4.0 mm at z=10 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- The hard grip: 6 walls (the designer's per-object setting).
- Designer: print it in PETG, PLA tends to deform.

