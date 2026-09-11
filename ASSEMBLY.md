# Assembly — the parts you have

For the fabricated build, `KETI_Acrylic_Order_REV4_StraightGuide_Transparent_2T_3T.dxf`
= `out/acrylic/v8_clear_straightguide_ordered/`.

**Read the Joy-Con section first.** The case assembles and works, but the side guide as
built does **not** lock a Joy-Con on. That is a consequence of the straight-groove
revision, not a fabrication error.

---

## 1. Check what came back

Six clear plates. Identify them by their cutouts, not by guesswork:

| plate | thickness | how to recognise it |
|---|---|---|
| **front** | 2T | one big window (112.0 × 63.5), **no groove** on the side edges |
| **L1** | 2T | large pocket 144.4 × 92.46 (nearly full width) + side grooves |
| **L2** | **3T** | the only 3 mm plate; smaller cavity + a small notch inside each groove |
| **L3 / L4 / L5** | 2T | identical: smaller cavity 126.24 × 74.46 + side grooves |

L3, L4 and L5 are the same part — order among them does not matter.
The smaller cavity is **offset 3.47 mm** toward one end; all of L2–L5 must face the same
way. Stack them and check the cavity edges line up before you bolt anything.

Also needed: 4 × **M2.5 × 18** button-head + 4 washers + 4 nuts (×20 if nyloc), and a
soft gasket strip — thin foam tape or 1 mm silicone, ~4 mm wide, about 480 mm of it.

## 2. Dry-fit
1. Peel the protective film off **both** faces of all six plates.
2. Stack L5 → L1 (no front plate, no display), push the four bolts through.
3. Look down the sides: the grooves in L1–L5 must form one clean straight channel,
   11 mm wide. If one plate is flipped the cavity offset will be obvious.
4. Drop a Joy-Con into a groove from the top and slide it down. It should run freely and
   stop 91.5 mm down. Note how it feels — you will decide about liners later.
5. Take it apart again.

## 3. The display
The glass is **not** sandwiched between flat sheets. L1 is a pocket; the glass sits in it.

1. Lay the gasket strip on the front face of **L2**, as a ring around the cavity, roughly
   over where the glass border will land. It fills the 1.3 mm between the back of the
   glass and L2, so the glass is pressed against the front plate instead of rattling.
2. Put L1 on top of L2.
3. Drop the **Touch Display 2** into the L1 pocket, glass toward the front. Its rear frame
   passes through the cavities in L2–L5; the glass border rests on the ledge.
4. Put the front plate on. Check the window sits over the picture — it is deliberately
   **2.47 mm off centre** because the panel is, so a perfectly centred window would be wrong.

## 4. Bolt it
Front plate → L1 → L2 → L3 → L4 → L5, bolts from the **front**, washer and nut at the
**back**.

Tighten in a cross pattern, **snug only**. Acrylic has no give: if the plate creaks, you
have already gone too far. There is no glue anywhere in this design — the four bolts are
the whole structure.

## 5. Raspberry Pi 5
1. Align the Pi with the **four corner stand-offs on the back of the display** and fix it
   with the **four M2.5 screws that came in the display box**. Those are Raspberry Pi's
   own screws for exactly this, and they are a different set from the case bolts.
2. 22→15-way FFC between display and Pi; J1 on the display → Pi GPIO pins 2 and 6 for power.
3. The Pi, its Active Cooler / NVMe HAT and all cables live outside the open rear. Nothing
   in the acrylic holds them.

---

## 6. Joy-Con — read this

**As built the Joy-Con drops into the groove and slides down, but nothing holds it on.**

The numbers: a first-gen Joy-Con's rail is a T — a head about **10.1 mm wide × 2.4 deep**
behind a neck about **7.1 wide × 0.7 deep**, ~3.1 mm of total protrusion. The ordered
groove is a plain rectangle **11.0 mm wide × 3.4 deep**, the same depth in every layer.

* head 10.1 ≤ channel 11.0 → it goes in ✔
* protrusion 3.1 ≤ depth 3.4 → deep enough ✔
* mouth 11.0 is **wider** than the head 10.1 → nothing overhangs it ✘

So it locates and aligns, and gravity keeps it down in the groove, but pull the Joy-Con
away from the case — which is what your hand does when you hold the thing as a handheld —
and it comes straight off. The straight groove was chosen on purpose to get rid of the
1 mm lip; retention was the price. It is working as drawn.

### What you can do, cheapest first

**a) Leave it. Use the Joy-Cons wirelessly.**
First-gen Joy-Cons pair over Bluetooth; the groove carries no power and no data, so it
was only ever going to *hold* them. Set the unit down or dock it and the grooves position
the Joy-Cons nicely. This costs nothing and nothing is wrong with it — it is just not a
hold-in-your-hands handheld.

**b) Tape lip — free, 10 minutes, do this before spending money.**
Run a strip of strong clear tape along the **front edge** and the **rear edge** of each
groove so roughly **2 mm** of tape overhangs the opening from each side. That narrows the
mouth from 11.0 to about 7 and gives the head something to catch on. It will tell you
whether the fit and the guide length are right before you order anything. Tape will not
survive real use, but it answers the question.

**c) Re-cut two plates — the actual fix.**
`out/acrylic/v8r_liplayers_recut/` has exactly two replacement plates, **L1r** and **L5r**.
They are the same outline, the same holes, the same cavities, but their side groove is a
**blind pocket** (1.0 mm of material left at the outer face, 2.4 mm cavity behind it)
instead of an open 3.4 mm slot. Put them in place of L1 and L5 and the stack becomes a
real T-slot again:

```
front 2T | L1r 2T lip | L2 3T | L3 2T | L4 2T | L5r 2T lip
mouth = L2+L3+L4 = 7.0     inner = 11.0     (reference 7.1 / 10.1)
```

**Keep the front plate, L2, L3 and L4 you already have.** Same 13.0 mm, same four
M2.5 × 18 bolts, same assembly order. Only two small plates to buy.

> Cut those two in **clear polycarbonate or PETG, not acrylic**. Each carries a 1.0 mm ×
> 97 mm lip along the groove, attached only at its lower end — precisely the thin rib the
> straight-guide revision was meant to avoid. In 2 mm acrylic it is brittle; in PC or PETG
> it flexes instead of snapping. If your shop will only do acrylic, expect to treat those
> two plates as consumables.

Fore-aft play will still be 0.9 mm (inner 11.0 vs 10.1). If it rattles, line the pocket
faces with 0.45 mm clear PET — add it a layer at a time and re-check.

**d) Nothing else is worth doing.** Gluing lips onto the finished parts has nowhere solid
to bond: along the side face only the 2 mm front plate is unbroken, everything behind it
is open groove.

---

## Before you power it up
* Display square in the pocket, window over the picture, no gap at the front.
* Pi's underside and its connectors clear the rear face of L5.
* Bolts snug, no creaking, no stress marks radiating from the holes.
* Decide on Joy-Con retention from section 6 — do the tape test first.

**Status: nothing in this document has been verified on the real parts.** The fit of the
display and of the Joy-Cons is still unknown; the numbers above come from the fabrication
drawing and the official display model, not from measurement of a built unit.
