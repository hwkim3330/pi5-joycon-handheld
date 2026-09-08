# reference — official Raspberry Pi 5" Touch Display 2 model

`td2_5in.step` is **not committed** (5.2 MB binary). Fetch it, then re-run the
measurement to reproduce every display number in `acrylic_panels.py`:

```bash
curl -L -o reference/td2_5in.step \
 'https://pip-assets.raspberrypi.com/categories/1083-raspberry-pi-touch-display-2/documents/RP-009152-DD-1-raspberry-pi-touch-display-2-step-5inch.step'
python3 reference/measure_step.py
```
(Product Information Portal → Raspberry Pi Touch Display 2 → *raspberry-pi-touch-display-2-step-5inch*, RP-009152-DD-1, no login.)

## Measured 2026-09-08 — what the design uses
Portrait STEP coordinates, origin as authored; **+Z is the front**.

| feature | value |
|---|---|
| cover glass | 91.46 × 143.40 × **0.70**, corner **R5.0** (8 circular edges), centre (0, +2.47) |
| rear frame (largest rear body) | 72.96 × 124.74 × 7.00, centre (0, −1.00), z[−5.48, +1.52] |
| active panel body | 71.16 × 120.94 × 2.57, centre (0, 0) |
| frame centre vs glass centre | **−3.47** along the long axis |
| panel centre vs glass centre | **−2.47** along the long axis |
| total depth (glass front → rearmost) | **10.40** (4.92 → −5.48) |
| four rear M2.5-size bosses | 4 × (±25.50, −49.38 / +54.32) → pitch **51.00 × 103.70**; boss r1.75, hole r1.25, z[−5.48, −1.98]. Display assembly, *not* Pi mounting |
| FFC connector block | 21.00 × 8.90 × 2.70 at (0.03, +37.37) |
| J1 power connector block | 16.40 × 5.20 × 2.00 at (+4.13, −30.19) |
| outside the frame footprint | none |
| behind the frame rear plane | none |

Two consequences the documentation does not spell out:

1. **The STEP models the glass + frame body only: a 10.40 mm envelope.** The
   documented depth of the complete product is **16 mm** — the difference is the rear
   mounting stand-offs and whatever is bolted to them. The acrylic pocket is sized to
   10.40; the stand-offs and the Pi pass through the open back.
2. **The stand-offs are not in the STEP.** Its four rear M2.5-size bosses are
   103.70 × 51.00 apart, which is no Pi hole pattern, so they are display assembly
   features. Per Raspberry Pi's documentation an SBC-form-factor Pi mounts directly to
   the display's four corner stand-offs with the four supplied M2.5 screws. Do not
   derive case geometry from the 103.70 × 51.00 bosses (this repo does not).

Official drawings are reference-only. Measure a real display before a volume order.
