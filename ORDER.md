# ORDER — clear cast acrylic + silver hardware

Everything is **clear (transparent) CAST acrylic**. No black, no smoked. All case
hardware is **silver / stainless M2.5**. Hand the shop `out/acrylic/<version>/sheet_<thickness>.dxf`
— one DXF per thickness.

> **Cut a fit coupon first.** `out/acrylic/test_coupon_exact/` or `…_acrylzip/`
> is a 40 mm section of the Joy-Con slot with the identical layer order and
> geometry: six small pieces, two M2.5 clamp bolts, slide a Joy-Con in from the
> open end. Only then order the case. The slot has never been cut in acrylic.

## Which version
| | v7_clear_exact | v7_clear_acrylzip |
|---|---|---|
| Joy-Con pocket layers (L1, L4) | **1.5T** | **2T** |
| raw Joy-Con inner width | 10.0 mm (reference 10.1) | 11.0 mm |
| liners | none | 0.45 mm clear PET on each pocket face → ~10.1 |
| body / total thickness | 11.5 / **13.5 mm** | 11.0 / **13.0 mm** |
| sheets | 1.5T · 2T · 5T | 2T · 5T |
| use when | the shop can supply 1.5T clear cast | standard-thickness auto-quote (Acrylzip 아크리애) |

If 1.5T clear cast is available, order **exact**. The acrylzip version is the
standard-thickness fallback; its 11.0 mm inner width is not "close enough" on its
own — fit the liners.

## v7_clear_exact — parts (7 pieces)
| part | thickness | qty | material | color | notes |
|---|---|---|---|---|---|
| front | 2T | 1 | cast acrylic | clear | window 112.0 × 63.5 at x −2.47 (viewing area + 0.25/side), 4 × Ø2.8 |
| L1_gpocket | **1.5T** | 1 | cast acrylic | clear | glass pocket 144.40 × 92.46 R5.5 **+** Joy-Con slot pocket + lock notch |
| L2_mouth | 5T | 1 | cast acrylic | clear | frame-size ledge cavity 126.24 × 74.46 (x −3.47) + slot mouth + 3.2 wire slot |
| L3_mouth | 2T | 1 | cast acrylic | clear | ledge cavity + slot mouth |
| L4_pocket | **1.5T** | 1 | cast acrylic | clear | ledge cavity + slot pocket + lock notch |
| L5_plain | 1.5T | 1 | cast acrylic | clear | ledge cavity; module rear ends 1.1 mm inside |

Sheets: `sheet_1.5T.dxf` (L1, L4, L5), `sheet_2T.dxf` (front, L3), `sheet_5T.dxf` (L2).

## v7_clear_acrylzip — parts (6 pieces)
| part | thickness | qty | material | color | notes |
|---|---|---|---|---|---|
| front | 2T | 1 | cast acrylic | clear | as above |
| L1_gpocket | **2T** | 1 | cast acrylic | clear | glass pocket + slot pocket; liner on the slot face |
| L2_mouth | 5T | 1 | cast acrylic | clear | ledge + mouth + wire slot |
| L3_mouth | 2T | 1 | cast acrylic | clear | ledge + mouth |
| L4_pocket | **2T** | 1 | cast acrylic | clear | ledge + slot pocket; liner on the slot face. Module rear ends 0.6 mm inside |

Sheets: `sheet_2T.dxf` (front, L1, L3, L4), `sheet_5T.dxf` (L2).

## Fit coupons (cut these first)
| folder | pieces | thicknesses |
|---|---|---|
| `test_coupon_exact` | C1 1.5T, C2 5T, C3 2T, C4 1.5T, C5 1.5T | 1.5T, 2T, 5T |
| `test_coupon_acrylzip` | C1 2T, C2 5T, C3 2T, C4 2T | 2T, 5T |

16 × 40 mm each, slot open at the top, 6 mm stop at the bottom, two Ø2.8 clamp holes.
Clamp with 2 × M2.5 × 20 + nuts.

## Hardware BOM (case) — separate from the display's own screws
| item | qty | spec | note |
|---|---|---|---|
| button-head screw | 4 | **M2.5 × 18**, silver / A2 stainless | computed: stack 13.5 (exact) + washer 0.5 + nut 2.0 + 1.5 stick-out = 17.5 → 18 (acrylzip 17.0 → 18). Nyloc (≈3.0): **M2.5 × 20** |
| washer | 4 | M2.5, stainless | under the nut, on the rear face of the last layer |
| nut | 4 | M2.5 hex or nyloc, stainless | |
| glass gasket | 1 ring | soft foam or silicone tape, 4 mm wide, **1.0 mm** (exact) / **1.5 mm** (acrylzip) uncompressed | on the ledge behind the glass border; takes up the pocket depth beyond the 0.70 glass, keeps the glass pressed to the front plate |
| clear PET liner | 4 | 0.45 mm × ~3 × 90 mm | **acrylzip only**; 0.5 mm PET gives 10.0 — decide on the coupon |
| Joy-Con charging rail part | 2 | L + R | optional; 6 mm pocket below the seat, 5 V/GND via the wire slot (pin 4 = 5 V, pins 1–2 = GND, small buck) |

**Not in this BOM:** the four M2.5 screws in the Touch Display 2 box. They are for
mounting a Raspberry Pi to the display's rear M2.5 points (103.7 × 51.0 apart on
the 5"), not for this case.

## Notes for the shop
* **Clear cast acrylic** (캐스트 투명), not extruded.
* DXF is **nominal finished geometry**. Apply your normal cutter compensation, do
  **not** add kerf on top. Ø2.8 holes are already M2.5 clearance.
* Slot mouth (7.0) and inner width come from sheet thickness (5T + 2T + pockets),
  not from the cut — sheet tolerance is exactly why the coupon comes first.
* L1 and L4 carry a 1.0 mm lip along the slot; handle gently until bolted.
