# 16 Eating Utensil Aid (kit)

- file: `Full Plates/16 Eating Utensil Aid (kit) - PLA x5.3mf`
- source: https://makerworld.com/en/models/192317-eating-utensil-aid-no-supports-updated-v2-files-in#profileId-212499
- reference 3mf: `Eating Utensil Aid (PLA)/Eating+Utensil+Aid.3mf`
- designer: Keebitzenny
- material: PLA (Bambu PLA Basic @BBL A1)
- on the plate: 5 kits (10 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 2 | 60% gyroid | off | auto_brim | 5/3 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `sparse_infill_density` | 15% | **60%** |
| `sparse_infill_pattern` | grid | **gyroid** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `flush_multiplier` | 1 | **0.75** |

## Validation
- Orca slice: passed - 11h 39m 25s, 231.2 g, 183.5 cm3
- per kit: 36.70 cm3
- the designer's own file slices at 36.80 cm3 per copy (100% of that here)
- the model page quotes 45 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 5 kits, 9h 49m 52s, 231.2 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Advisories (nothing changed)
- Spoon Holder.stl: 610 mm2 of steep overhang with air under it (max drop 21.0 mm at z=23 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- Designer recommends ABS and supplies a PLA profile; PLA used per the folder.
- PETG would be the tougher option for a utensil aid that gets washed.

