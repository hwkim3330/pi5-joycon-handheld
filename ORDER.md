# ORDER — clear cast acrylic + silver hardware

Everything is **clear (transparent) CAST acrylic**. No black, no smoked. All case
hardware is **silver / stainless M2.5**. Hand the shop `out/acrylic/<version>/sheet_<thickness>.dxf`
— one DXF per thickness.

> **What was actually ordered is v8 (below).** v7 is kept as the earlier reference design.
>
> **Cut a fit coupon first.** Each version has one in `out/acrylic/test_coupon_<version>/`:
> a 40 mm section of the side guide with the identical layer order and geometry, two M2.5
> clamp bolts, slide a Joy-Con in from the open end. The guide has never been cut in
> acrylic — for the ordered v8 the coupon is `test_coupon_ordered` (5 pieces, 2T + 3T).

## v8_clear_straightguide_ordered — AS ORDERED / AS FABRICATED

Submitted as `KETI_Acrylic_Order_REV4_StraightGuide_Transparent_2T_3T.dxf`.
**Fabrication submitted; physical fit not yet verified.**

| part | thickness | qty | material | color | notes |
|---|---|---|---|---|---|
| front | 2T | 1 | cast acrylic | **clear** | window 112.0 × 63.5 at x −2.47; no groove |
| L1 | 2T | 1 | cast acrylic | clear | glass pocket 144.40 × 92.46; straight groove |
| L2 | **3T** | 1 | cast acrylic | clear | ledge cavity; groove; 3.2 × 6.8 blind wire recess both sides |
| L3 | 2T | 1 | cast acrylic | clear | ledge cavity; straight groove |
| L4 | 2T | 1 | cast acrylic | clear | ledge cavity; straight groove |
| L5 | 2T | 1 | cast acrylic | clear | ledge cavity; straight groove |

**6 acrylic pieces, 13.0 mm total, body 164.4 × 108.5 mm, open rear, no glue.**
Sheets: `sheet_2T.dxf` (front, L1, L3, L4, L5) and `sheet_3T.dxf` (L2).

Side guide: plain straight groove **3.4 mm** deep, open at the top edge, **91.5 mm** guide
+ **6 mm** contact bay. No T-lip. Lateral play is accepted; thin clear PET/tape may be
added after a fit test.

Hardware: **4 × M2.5 × 18** silver button-head (17.0 mm needed; ×20 with nyloc),
4 × M2.5 washer, 4 × M2.5 nut. Plus the gasket strip listed in the BOM below.

> The same fabrication sheet also carried a separate project — 20 × LAN9692 frame plates
> (A/B/C/D, 3T, 5 each, 250 × 180 mm). Nothing to do with this case.

## The two earlier v7 reference versions
| | v7_clear_exact | v7_clear_acrylzip |
|---|---|---|
| Joy-Con pocket layers (L1, L4) | **1.5T** | **2T** |
| raw Joy-Con inner width | 10.0 mm (reference 10.1) | 11.0 mm |
| liners | none | 0.45 mm clear PET on each pocket face → ~10.1 |
| body / total acrylic thickness | 11.5 / **13.5 mm** | 11.0 / **13.0 mm** |
| sheets | 1.5T · 2T · 5T | 2T · 5T |
| use when | the shop can supply 1.5T clear cast | standard-thickness auto-quote (Acrylzip 아크리애) |

These were the T-slot designs that preceded the ordered revision. If 1.5T clear cast is available, **exact** is the closer of the two to the reference geometry. The acrylzip version is the
standard-thickness fallback; its 11.0 mm inner width is not "close enough" on its
own — fit the liners.

## v7_clear_exact — parts (6 acrylic pieces)
| part | thickness | qty | material | color | notes |
|---|---|---|---|---|---|
| front | 2T | 1 | cast acrylic | clear | window 112.0 × 63.5 at x −2.47 (viewing area + 0.25/side), 4 × Ø2.8 |
| L1_gpocket | **1.5T** | 1 | cast acrylic | clear | glass pocket 144.40 × 92.46 R5.5 **+** Joy-Con slot pocket + lock notch |
| L2_mouth | 5T | 1 | cast acrylic | clear | frame-size ledge cavity 126.24 × 74.46 (x −3.47) + slot mouth + 3.2 wire slot |
| L3_mouth | 2T | 1 | cast acrylic | clear | ledge cavity + slot mouth |
| L4_pocket | **1.5T** | 1 | cast acrylic | clear | ledge cavity + slot pocket + lock notch |
| L5_plain | 1.5T | 1 | cast acrylic | clear | ledge cavity; the STEP glass/frame body ends 1.1 mm inside the case back |

Sheets: `sheet_1.5T.dxf` (L1, L4, L5), `sheet_2T.dxf` (front, L3), `sheet_5T.dxf` (L2).

## v7_clear_acrylzip — parts (5 acrylic pieces)
| part | thickness | qty | material | color | notes |
|---|---|---|---|---|---|
| front | 2T | 1 | cast acrylic | clear | as above |
| L1_gpocket | **2T** | 1 | cast acrylic | clear | glass pocket + slot pocket; liner on the slot face |
| L2_mouth | 5T | 1 | cast acrylic | clear | ledge + mouth + wire slot |
| L3_mouth | 2T | 1 | cast acrylic | clear | ledge + mouth |
| L4_pocket | **2T** | 1 | cast acrylic | clear | ledge + slot pocket; liner on the slot face. STEP glass/frame body ends 0.6 mm inside |

Sheets: `sheet_2T.dxf` (front, L1, L3, L4), `sheet_5T.dxf` (L2).

## Fit coupons (cut these first)
| folder | pieces | thicknesses |
|---|---|---|
| **`test_coupon_ordered`** | **5** — C1 2T, C2 3T, C3 2T, C4 2T, C5 2T | **2T, 3T** (matches the ordered build) |
| `test_coupon_exact` | **5** — C1 1.5T, C2 5T, C3 2T, C4 1.5T, C5 1.5T | 1.5T, 2T, 5T |
| `test_coupon_acrylzip` | **4** — C1 2T, C2 5T, C3 2T, C4 2T | 2T, 5T |

16 × 40 mm each, slot open at the top, 6 mm stop at the bottom, two Ø2.8 clamp holes.
Clamp with 2 × M2.5 × 20 + nuts.

## Hardware BOM (case) — separate from the display's own screws
| item | qty | spec | note |
|---|---|---|---|
| button-head screw | 4 | **M2.5 × 18**, silver / A2 stainless | computed: v8/acrylzip stack 13.0 + washer 0.5 + nut 2.0 + 1.5 stick-out = 17.0 → 18 (v7 exact 17.5 → 18). Nyloc (≈3.0): **M2.5 × 20** |
| washer | 4 | M2.5, stainless | under the nut, on the rear face of the last layer |
| nut | 4 | M2.5 hex or nyloc, stainless | |
| glass gasket | 1 ring | soft foam or silicone tape, 4 mm wide, **1.0 mm** uncompressed (v8 and v7 exact; 1.5 mm for v7 acrylzip) | on the ledge behind the glass border; takes up the pocket depth beyond the 0.70 glass, keeps the glass pressed to the front plate |
| clear PET liner | 4 | 0.45 mm × ~3 × 90 mm | **v7 acrylzip only** (for v8, add liner/tape only after a fit test); 0.5 mm PET gives 10.0 — decide on the coupon |
| Joy-Con charging rail part | 2 | L + R | optional; 6 mm pocket below the seat, 5 V/GND via the wire slot (pin 4 = 5 V, pins 1–2 = GND, small buck) |

**Not in this BOM:** the four M2.5 screws in the Touch Display 2 box. Those mount the
Raspberry Pi directly to the display's four rear corner stand-offs (the official
method); they have nothing to do with this case.

## Notes for the shop
* **Clear cast acrylic** (캐스트 투명), not extruded.
* DXF is **nominal finished geometry**. Apply your normal cutter compensation, do
  **not** add kerf on top. Ø2.8 holes are already M2.5 clearance.
* v8: the side guide is a plain 3.4 mm groove, so its depth comes from the cut and its
  width from the sheet stack (11.0 mm of L1–L5). No thin acrylic tongues anywhere.
* v7 only: mouth (7.0) and inner width come from sheet thickness; L1/L4 carry a 1.0 mm
  lip along the slot and must be handled gently until bolted. That fragility is exactly
  why v8 exists.
