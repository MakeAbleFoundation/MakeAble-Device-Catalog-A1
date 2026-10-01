# 17 Quick-Slip Shoe Horn

- file: `Full Plates/17 Quick-Slip Shoe Horn - PETG x12.3mf`
- source: https://makerworld.com/en/models/1024414-quick-slip-shoe-horn#profileId-1006338
- reference 3mf: `Shoe Horn (PETG)/Shoe+Horn+3MF.3mf`
- designer: Stag 3D
- material: PETG (PETG A1 Tuned)
- on the plate: 12 copies (12 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 2 | 15% grid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `ironing_flow` | 10% | **15%** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `default_acceleration` | 10000 | **6000** |
| `flush_multiplier` | 1 | **0.75** |
| `smooth_coefficient` | 4 | **80** |
| `sparse_infill_speed` | 350 | **270** |
| `travel_speed` | 1000 | **700** |

## Validation
- Orca slice: passed - 12h 22m 53s, 293.4 g, 234.7 cm3
- per copie: 19.56 cm3
- the model page quotes 25 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 12 copies, 11h 46m 18s, 296.5 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Notes
- Designer: PETG or stronger is required.
- Profile came from an H2S; speeds and accelerations rebased to the A1.

