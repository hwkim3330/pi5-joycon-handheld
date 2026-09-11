# Assembly — v8, as ordered

Applies to **`out/acrylic/v8_clear_straightguide_ordered/`**, the configuration that was
actually sent for fabrication
(`KETI_Acrylic_Order_REV4_StraightGuide_Transparent_2T_3T.dxf`).

**Fabrication submitted. Physical fit — Joy-Con and display — is NOT yet verified.**

## Parts
| # | part | thickness | note |
|---|---|---|---|
| 1 | front | 2T | window 112.0 × 63.5 at x −2.47; no groove |
| 2 | L1 | 2T | glass pocket 144.40 × 92.46; straight groove |
| 3 | L2 | **3T** | ledge cavity; straight groove; 3.2 × 6.8 blind wire recess, both sides |
| 4 | L3 | 2T | ledge cavity; straight groove |
| 5 | L4 | 2T | ledge cavity; straight groove |
| 6 | L5 | 2T | ledge cavity; straight groove |

6 clear-acrylic pieces, **13.0 mm** total, body **164.4 × 108.5 mm**, open rear.

Hardware: **4 × M2.5 × 18** silver button-head (17.0 mm needed; use ×20 with nyloc),
4 × M2.5 washer, 4 × M2.5 nut. **No acrylic glue anywhere** — the stack is held only by
the four through-bolts.

## Order, front to rear
```
M2.5 button-head  ──►  front 2T
                       Touch Display 2   (cover glass seated IN the L1 pocket)
                       L1 2T
                       L2 3T
                       L3 2T
                       L4 2T
                       L5 2T
                       washer + nut  ◄──
```

**The display is not sandwiched between two flat sheets.** L1 is a pocket 144.40 × 92.46
that the 0.70 mm cover glass drops into; L2–L5 have a smaller, frame-shaped cavity
126.24 × 74.46 (offset x −3.47), so the glass border rests on that step while the
display's rear frame passes through. The front plate stops the display moving forward,
the ledge stops it moving back. Take up the slack behind the glass border with a soft
gasket strip on the ledge (~1.0 mm uncompressed, 4 mm wide) so the glass is held against
the front plate rather than rattling.

## Steps
1. Peel both protective films from all six pieces.
2. Dry-stack L5 → L1 on a flat surface, pass the four bolts through, check the holes line
   up and the grooves in L1–L5 are flush on both sides. Correct a mis-ordered layer now.
3. Lay the gasket ring on the ledge (front face of L2), around the cavity.
4. Drop the display glass into the L1 pocket, glass forward.
5. Put the front plate on. Feed the four M2.5 bolts from the front, washer + nut at the
   back. Tighten in a cross pattern, snug only — acrylic cracks if you keep going.
6. Mount the **Raspberry Pi 5** on the display's four rear corner stand-offs with the
   **four M2.5 screws supplied with the display**. Those are Raspberry Pi's own screws,
   a different set from the case bolts above, and they hold the Pi to the display — not
   the display to the case. Connect the 22→15-way FFC and the J1 → GPIO power cable.
7. The Pi, its Active Cooler / NVMe HAT and all cables stay outside the open rear.

## Joy-Con guide
Each side has a plain straight groove: **3.4 mm deep**, open at the top edge, **91.5 mm**
of guide with a **6 mm contact bay** below it (97.5 mm of groove, ~11 mm of solid acrylic
under that). The channel is the 11 mm of L1–L5; the front plate closes its front face,
the rear is open.

This is a **guide, not a lock** — there is no undercut, so some lateral play is expected
and the Joy-Con is not retained against being pulled straight off. That was the accepted
trade for dropping the fragile 1 mm lip (see the design history in the README). After a
physical fit test you can line the groove faces with thin clear PET or tape to take up
play; add it in small steps and check after each.

The 3.2 × 6.8 mm recess in L2 sits in the contact bay for a future Joy-Con charging
contact block. As drawn it is **blind** — it does not break through to the display
cavity, so routing a wire from the inside needs a small extra opening that is not in the
ordered drawing.

## Before you power anything
* Confirm the display sits square in the pocket and the window lines up with the viewing
  area (the window is deliberately off-centre by 2.47 mm because the panel is).
* Check the Pi's underside and its connectors clear the rear face of L5.
* Slide a Joy-Con in and judge the fit before deciding on liners.
