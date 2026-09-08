# Pi 5 + 5" Touch Display 2 + Joy-Con
## Clear Laser-Cut Acrylic Handheld

**Status: DESIGN VALIDATED AGAINST REFERENCE DIMENSIONS (official 5" STEP + Cuttlephone) —
PHYSICAL FIT NOT YET VERIFIED.** Nothing has been cut. Cut the fit coupon before the case
(`ORDER.md`).

| front | rear (open back) |
|---|---|
| ![front](out/acrylic/v7_clear_exact/preview_front.png) | ![back](out/acrylic/v7_clear_exact/preview_back.png) |

| exploded | corner: glass pocket → ledge |
|---|---|
| ![exploded](out/acrylic/v7_clear_exact/preview_exploded.png) | ![ledge](out/acrylic/v7_clear_exact/preview_ledge.png) |

![slot](out/acrylic/v7_clear_exact/preview_slot.png)

## What it is
A **13.5 mm** stack of **clear cast acrylic** around the official **Raspberry Pi Touch
Display 2 (5")**, open at the back so the **Raspberry Pi 5**, its Active Cooler / NVMe
HAT and cables stay visible. Real first-generation **Joy-Cons slide down into female
T-slots** cut into the side walls — no 3D printing, no glue. All case fasteners are
**silver M2.5 button-heads** on the front, washer + nut on the rear face.

Body 164.4 × 108.5 mm. Source of truth for every number: `acrylic_panels.py`;
`verify_dxf.py` re-measures the exported DXFs against it.

## Versions
| version | pocket layers | raw Joy-Con inner | total | sheets | use when |
|---|---|---|---|---|---|
| **v7_clear_exact** | 1.5T | 10.0 mm | 13.5 mm | 1.5T · 2T · 5T | the shop can cut 1.5T clear cast |
| **v7_clear_acrylzip** | 2T | 11.0 mm → **~10.1 with 0.45 mm PET liners** | 13.0 mm | 2T · 5T | standard-thickness quotes (Acrylzip 아크리애) |

Fit coupons: `out/acrylic/test_coupon_exact/`, `out/acrylic/test_coupon_acrylzip/`.

## The display, measured from the official STEP
`reference/td2_5in.step` is Raspberry Pi's own 5" model (RP-009152-DD-1, public on the
Product Information Portal). Read with CadQuery; landscape here = display long axis
along case X, origin at the glass centre.

| feature | mm | in code |
|---|---|---|
| cover glass | 143.40 × 91.46 × **0.70**, corners **R5.0** | `GLASS_*` |
| rear frame (largest rear body) | 124.74 × 72.96, centre **x −3.47** from the glass centre, **9.70** behind the glass back | `FRAME_*` |
| total module depth | **10.40** — the "16 mm" in the docs is not the bare module | `DISP_D` |
| active-area (panel) centre | **x −2.47** from the glass centre → bezel 13.5 mm one end, 18.4 the other | `PANEL_DX` → `ACT_DX` |
| rear M2.5 points | four, at (±51.85, ±25.5) = **103.7 × 51.0** — *not* a Pi hole pattern | `POST_XY` |
| anything outside the frame footprint or behind its rear plane | none | |
| active / viewing area (product brief) | 110.4 × 62.1 / 111.5 × 63.0 | `ACTIVE_*`, `VIEW_*` |

The window is cut to the **viewing** area + 0.25 mm/side = 112.0 × 63.5, centred on the
panel (x −2.47), not on the glass. Active and viewing areas are separate variables.
Official drawings are reference-only: **measure a real display before any volume order**
(the sign of `ACT_DX` flips if you rotate the display the other way).

### How the display is held (like every bezel)
```
front 2T  ────────────────────────   clear, window over the viewing area
L1 1.5T   glass pocket 144.4 × 92.46 : the 0.70 glass sits here, gasket ring behind its border
L2…       ledge cavity 126.24 × 74.46: the glass border rests on this step (≥ 4.6 mm wide)
          the 9.7 mm rear frame passes through; open back
```
Forward: front plate. Backward: the ledge. Nothing else is needed — the earlier
"rear retaining bars" idea was wrong: at the module's edge there is only 0.7 mm of glass,
no rear surface to press on. The module rear ends 1.1 mm (exact) / 0.6 mm (acrylzip)
inside the case back.

### Pi 5 mounting — read this
The documentation says the Pi 5 screws to "four stand-offs" with the supplied M2.5 screws.
The **5" STEP shows four rear M2.5 points 103.7 × 51.0 mm apart, which is not the Pi 5's
58 × 49 pattern** — so on the 5" a bracket must be involved. Those screws hold the Pi
(or bracket) to the LCD; they have nothing to do with this case. The preview draws a
generic bracket + Pi block as illustration only. Cables: 22→15-way FFC, display J1 → Pi
GPIO power.

## Joy-Con slot
Nintendo puts the **female slot on the console** and the **male rail on the Joy-Con**.
Reference geometry is derived from the field-tested
[Cuttlephone](https://github.com/SiloCityLabs/Cuttlephone) design (`phone_case.scad`):
mouth 7.1, inner 10.1, cavity 2.4, lock notch 3.8 wide 9.4 from the top, rail 91.5.
Laser kerf and actual sheet thickness still require a physical fit test.

Built from the layer stack, so it is only 2-D cuts:
```
 outer face →                            ← inside
 L1 gpocket 1.5T |▒▒|░░░░░░░░░░░|  lip 1.0 + hidden cavity 2.4 (lip removed 3.8 mm at the notch)
 L2 mouth   5T   |░░░░░░░░░░░░░░|  full 3.4 cut, open at the top edge, + wire slot
 L3 mouth   2T   |░░░░░░░░░░░░░░|
 L4 pocket  1.5T |▒▒|░░░░░░░░░░░|
```
mouth = 5T + 2T = 7.0 (0.1 under reference — tight on purpose: sand, never loosen);
inner = 7.0 + 2 × pocket. Lip 1.0 instead of Nintendo's 0.7 (acrylic). The slot runs
out through the top edge; the Joy-Con seats 91.5 mm below it; a 6 mm zone below takes a
Joy-Con charging-rail part fed through the 3.2 mm wire slot (pin 4 = 5 V, pins 1–2 = GND).

## Bezel (cosmetic, optional)
The front is clear, so the display's black bezel shows through it — that is the design.
To hide it, put black vinyl / masking film on the **back** of the front plate, leaving the
112.0 × 63.5 window open. No extra sheet.

## Kerf
DXF geometry is nominal finished geometry; the shop applies cutter compensation; do not
add your own offset. Slot widths come from sheet thickness, hence the coupon.

## Still to verify on hardware
1. Joy-Con fit on **your** Joy-Cons — cut a coupon.
2. Real glass/frame dimensions vs the STEP on your unit (reference-only drawings).
3. How the Pi actually mounts to the 5" (bracket in the box?) and rear clearances.

## Files
```
acrylic_panels.py    all geometry + design checks (raises before exporting on failure)
verify_dxf.py        re-measures the exported DXFs against the code
render_previews.py   preview PNGs (VTK) + slot section (matplotlib)
ORDER.md             what to order, per version, plus hardware BOM
reference/td2_5in.step   official Raspberry Pi 5" Touch Display 2 model (validation)
out/acrylic/v7_clear_exact/        DXFs, sheet_*.dxf, manifest.txt, previews (front/back/exploded/slot/ledge), stack_preview.stl
out/acrylic/v7_clear_acrylzip/     standard-thickness fallback
out/acrylic/test_coupon_exact/     fit coupon (cut first)
out/acrylic/test_coupon_acrylzip/  fit coupon, standard thicknesses
legacy/                            earlier drafts — NOT FOR FABRICATION
```
`pip install cadquery ezdxf`, then `python3 acrylic_panels.py && python3 verify_dxf.py && python3 render_previews.py`.
