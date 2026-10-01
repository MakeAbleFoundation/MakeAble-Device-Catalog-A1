# 08 KeyWings

- file: `Full Plates/08 KeyWings - PETG x73.3mf`
- source: https://makerworld.com/en/models/1688156-keywings-for-mobility-needs#profileId-1789186
- reference 3mf: `Key Holder (PETG)/KeyWings+v6+Bambu.3mf`
- designer: AlbertMakes
- material: PETG (PETG A1 Tuned)
- on the plate: 73 copies (73 objects)
- print-time cap: 88 copies fit on the plate; trimmed to 73 to stay under 14 h on the A1

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 3 | 20% grid | off | no_brim | 5/3 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `bridge_speed` | 50 | **30** |
| `brim_type` | auto_brim | **no_brim** |
| `enable_arc_fitting` | 1 | **0** |
| `enable_prime_tower` | 1 | **0** |
| `inner_wall_line_width` | 0.45 | **0.5** |
| `max_travel_detour_distance` | 0 | **50** |
| `outer_wall_line_width` | 0.42 | **0.5** |
| `outer_wall_speed` | 200 | **100** |
| `overhang_2_4_speed` | 50 | **100** |
| `overhang_3_4_speed` | 30 | **100** |
| `overhang_4_4_speed` | 10 | **100** |
| `overhang_totally_speed` | 10 | **100** |
| `reduce_crossing_wall` | 0 | **1** |
| `skeleton_infill_density` | 15% | **20%** |
| `skin_infill_density` | 15% | **20%** |
| `sparse_infill_density` | 15% | **20%** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_generator` | classic | **arachne** |
| `wall_loops` | 2 | **3** |
| `wall_sequence` | inner wall/outer wall | **outer wall/inner wall** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `elefant_foot_compensation` | 0 | **0.075** |
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |

## Validation
- Orca slice: passed - 13h 50m 0s, 225.3 g, 180.2 cm3
- per copie: 2.47 cm3
- the designer's own file slices at 2.63 cm3 per copy (94% of that here)
- the model page quotes 4 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 76 copies, 13h 56m 36s, 237.0 g
- 76 copies ran 14h 22m 29s on the A1, over the 14 h cap: trimmed to 74, keeping the ones nearest the middle of the plate; nothing that stayed was moved
- 74 copies ran 14h 0m 33s on the A1, over the 14 h cap: trimmed to 73, keeping the ones nearest the middle of the plate; nothing that stayed was moved
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Advisories (nothing changed)
- Body_05*: tall and narrow (21 mm on a 6 mm footprint) with brim off in the designer's profile

## Notes
- Designer recommends PETG or nylon; brim is deliberately off in their profile.

