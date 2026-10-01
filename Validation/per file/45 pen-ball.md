# 45 Pen Ball (kit)

- file: `Full Plates/45 Pen Ball (kit) - PETG x4.3mf`
- source: https://www.thingiverse.com/thing:2810069
- source files: `New Devices/Pen Ball - 2810069/files/Pen_Ball_Top_v.1.0.0.STL`, `New Devices/Pen Ball - 2810069/files/Pen_Ball_Bottom_v.1.0.0.stl`
- designer: makersmakingchange (Thingiverse)
- license: CC BY-NC-SA
- material: PETG (PETG A1 Tuned)
- on the plate: 4 kits (8 objects)
- print-time cap: 6 kits fit on the plate; trimmed to 4 to stay under 14 h on the A1
- also needed: 5 x #6-32 x 3/4 in round-head screws + 5 x #6-32 hex nuts per ball

## Profile
| preset | layer | first layer | walls | infill | supports | brim | top/bottom |
|---|---|---|---|---|---|---|---|
| 0.20mm Standard @BBL A1 | 0.2 mm | 0.2 mm | 2 | 50% grid | on tree(auto) | auto_brim | 5/3 |

### Deliberate changes
- `enable_support`: 0 -> **1**
- `skeleton_infill_density`: 15% -> **50%**
- `skin_infill_density`: 15% -> **50%**
- `sparse_infill_density`: 15% -> **50%**
- `support_on_build_plate_only`: 0 -> **1**

## Validation
- Orca slice: passed - 12h 18m 32s, 258.7 g, 206.9 cm3
- per kit: 51.73 cm3
- geometry check: clean
- clamped for Orca only (the delivered file keeps Bambu's values): tree_support_wall_count, raft_first_layer_expansion

## Converted from the P1S file
- on the P1S: 4 kits, 11h 36m 55s, 261.4 g
- `default_acceleration`: 10000 (X1C/P1S preset) -> **6000** (A1 preset)
- `elefant_foot_compensation`: 0.15 (X1C/P1S preset) -> **0.075** (A1 preset)
- `smooth_coefficient`: 150 (X1C/P1S preset) -> **80** (A1 preset)
- `travel_speed`: 500 (X1C/P1S preset) -> **700** (A1 preset)

## Notes
- Designer's spec sheet: 0.2 mm layers, 50% infill, supports only in the centre cavity, both halves printed together. Build-plate-only supports reach just that cavity.
- Designer used ABS; PETG is the closest of the two filaments here.

