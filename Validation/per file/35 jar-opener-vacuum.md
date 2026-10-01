# 35 Jar Opener / Vacuum Releaser

- file: `Full Plates/35 Jar Opener - Vacuum Releaser - PLA x8.3mf`
- source: https://makerworld.com/en/models/1642031-jar-opener-tuned-for-all-bambu-printers#profileId-1735123
- reference 3mf: `New Devices/Jar+Opener+Bambu+ULTRA+FAST.3mf`
- designer: AlbertMakes
- license: MakerWorld Standard Digital File License
- material: PLA (Bambu PLA Basic @BBL A1)
- on the plate: 8 copies (8 objects)

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.24mm Draft @BBL A1 | 0.24 mm | 0.24 mm | 2 | 10% gyroid | off | no_brim | 3/3 |

### Taken from the designer's file
| setting | A1 preset | designer |
|---|---|---|
| `brim_type` | auto_brim | **no_brim** |
| `enable_circle_compensation` | 0 | **1** |
| `enable_overhang_speed` | 1 | **0** |
| `enable_prime_tower` | 1 | **0** |
| `initial_layer_print_height` | 0.2 | **0.24** |
| `precise_z_height` | 0 | **1** |
| `reduce_crossing_wall` | 0 | **1** |
| `skeleton_infill_density` | 15% | **10%** |
| `skin_infill_density` | 15% | **10%** |
| `sparse_infill_density` | 15% | **10%** |
| `sparse_infill_pattern` | grid | **gyroid** |
| `top_one_wall_type` | all top | **not apply** |
| `top_shell_layers` | 4 | **3** |
| `tree_support_wall_count` | -1 | **0** |
| `wall_sequence` | inner wall/outer wall | **outer wall/inner wall** |
| `z_direction_outwall_speed_continuous` | 0 | **1** |

### Left at the A1 value (designer never changed it on their printer)
| setting | their file | A1 |
|---|---|---|
| `curr_bed_type` | High Temp Plate | **Textured PEI Plate** |
| `elefant_foot_compensation` | 0 | **0.075** |
| `flush_multiplier` | 1 | **0.75** |
| `raft_first_layer_expansion` | 2 | **-1** |

### Deliberate changes
- mesh: four mesh vertices forming a 0.36 mm spike under the flat base were moved up onto the base; the part stood on the spike, its first layer was empty and the slicer refused it (the designer's own file fails the same way in OrcaSlicer)

## Validation
- Orca slice: passed - 7h 13m 16s, 161.4 g, 128.1 cm3
- per copie: 16.02 cm3
- the model page quotes 22 g per copy
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 8 copies, 6h 20m 5s, 161.4 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Advisories (nothing changed)
- Body_03: 359 mm2 of steep overhang with air under it (max drop 14.3 mm at z=20 mm) while supports are off in the designer's profile - worth a look at the preview

## Notes
- Mesh fix: four vertices formed a 0.1 x 0.5 mm spike 0.36 mm below the flat base, so the part stood on the spike and its first layer was empty - the slicer refuses it (the designer's own file fails the same way in OrcaSlicer). Those four vertices were moved up onto the base; nothing else in the mesh changed.
- Profile was an A1 mini 0.24 mm Draft profile; rebased onto the A1 0.24 mm Draft.
- The page text suggests 0.2 mm, 6 walls, 60% infill; the downloaded profile uses 0.24 mm, 2 walls, 10% gyroid. The profile wins, as agreed.

