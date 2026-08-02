# DESIGN-NOTES.md

Running record of design decisions, as `DESIGN-RULES.md` section 14 asks for. Read this before changing the look of anything, so the next pass does not drift back toward the average.

## The brief

```
Subject:                 Portfolio for a second year UNSW mechanical engineering student.
                         Real hardware: CubeSat ground station mounts, an autonomous
                         agricultural drone, competition robots, plus shipped software.
Audience:                Graduate recruiters and engineering managers screening for
                         2026/27 vacation programs. They skim, and they have seen
                         several hundred student portfolios.
The page's single job:   Prove that this person has built physical things that work,
                         and make it trivial to contact them.
Tone:                    Measured, specific, unembellished.
Aesthetic direction:     Technical / instrumentation (section 3).
Signature element:       The drawing title block, carried on every sheet.
Locale:                  en-AU.
Constraints:             Static HTML and CSS, GitHub Pages, no build step,
                         no framework, no dependencies.
```

## Palette

Three active hues. Dominant surface, neutral ink, one accent.

| Token | Hex | Role |
|---|---|---|
| `--paper` | `#e7e8e3` | Dominant surface. Cool grey-green drafting stock. |
| `--paper-raised` / `--paper-sunk` | `#eff0ec` / `#dcded7` | 3 to 5 percent lightness shifts, used instead of borders. |
| `--graphite` | `#14181a` | Ink. 14.5:1 on paper. |
| `--graphite-mid` / `--graphite-soft` | `#3c464b` / `#525e64` | 7.9:1 and 5.4:1 on paper. |
| `--slate` | `#1b2226` | Inverted panels and drawing plates. |
| `--oxide` | `#a63a17` | The accent. 5.3:1 on paper, so it can carry small text. |
| `--oxide-lift` | `#e0703f` | Accent on slate only. 5.0:1 there, 2.6:1 on paper. Never use it on paper. |

No pure black or white on any large surface. No gradient anywhere in the system.

**Deliberate near-miss on rules section 3.** The banned default is cream near `#F4F1EA`, a high contrast serif display face, and terracotta near `#D97757`. This palette holds an oxide accent, which is adjacent to that family. It clears the tell on the other two axes: the ground is a cool grey-green rather than cream, and the display face is a wide grotesque rather than a serif. Oxide is also true to the subject, being the colour of steel primer and competition field hardware. If this ever starts to read as the default, move the accent toward a deeper drafting blue rather than diluting it.

## Type

Three families, which is the ceiling.

- **Display: Archivo** (variable, `wdth` 100 to 125). Wide grotesque, signage flavoured. Used at 100 to 112 percent width so headings read as stencilled rather than condensed.
- **Body: Source Serif 4** at 18px, line height 1.6, measure capped at 68ch. A serif body against a wide grotesque display gives hierarchy without a third voice.
- **Data: IBM Plex Mono** at 11 to 14px. Reserved for measured things only: labels, sheet numbers, dates, revisions, status. Never used as decoration.

Scale ratio 1.25 from an 18px body. None of the banned display faces appear, and the previous build's Space Grotesk was removed for that reason.

## Signature element

The drawing title block. A ruled strip of real fields with real values, appearing four times in the system:

1. Under the hero copy: discipline, current role, location, set size.
2. Inside the hero drawing itself, as the sheet's own title block.
3. Directly under every case study `h1`, in its own band.
4. As `Sheet NN/06` markers on every project entry.

Supporting the same idea: a fine 24px and 96px graph substrate fixed behind the page, corner registration crosses available as `.ticks`, and drawings that use real drafting conventions (centre lines as dash-dot, section hatching, dimension lines with tick terminators, numbered leader notes).

## The one aesthetic risk

The hero is a two view orthographic drawing of the antenna pointing assembly, complete with its own title block, rather than a photograph or an abstract diagram. Justification: this person's actual output is engineering drawings, so the page opens with the artefact instead of a description of it. Dimension lines carry **labels rather than numbers**, because inventing dimensions would be a fabricated stat.

## Photographs

Rules section 9 says one real image beats six illustrations, so where a real photograph exists it wins over a drawing. The VEX sheet carries five: the robot in the pit, the seven person team with the national trophies, the world championship pit floor, and two earlier season builds under a **Previous builds** section. The VEX card on the landing page now leads with the robot photograph instead of its drawing.

Drawings stay where there is no photograph (BlueSat, the drone, and the VEX side elevation on its own sheet). They are honest stand-ins, not decoration, and the design notes above still govern them.

Every photograph ships at three widths (600, 1000, 1600) with `srcset` and `sizes`. A 390px phone pulls the 600w file, 55 to 113KB. The 1600w file is only fetched when someone opens the lightbox. Product screenshots use the same component at 800 and 1280.

Both plates in the paired cards hold a 3:2 aspect so the two cards stay in step whether the sheet leads with a drawing or a photograph.

## Motion budget

One moment. The hero drawing plots itself on load: outlines, then section hatching, then dimension lines, then the annotation inks in. Roughly 1.5 seconds, once, never repeated.

Everything else is interaction state only, 140 to 220ms, eased. There is deliberately **no scroll-triggered fade** anywhere. The previous build faded in every block on scroll, which is the pattern rules section 8 names.

The lightbox is interaction, not decoration: photographs of hardware reward a closer look. It is progressive enhancement built on `<dialog>`, and the **Enlarge** control stays hidden unless the script has run and the browser supports `showModal`, so a dead button never ships. Cleanup (clearing the image, returning focus to the control that opened it) is driven explicitly rather than from the dialog `close` event, which does not fire reliably in every engine. Clicking the image itself is a pointer convenience layered on top of the real button, never instead of it.

## Layout decisions worth keeping

- **Section rhythm varies on purpose.** Tall asymmetric hero, then a thin edge to edge band, then a deep work section, then a shallow reference list, then a register, then a full bleed inverted about, then a left anchored contact. Vertical padding is not uniform.
- **The six projects are presented three different ways**, because they do not deserve equal weight: sheet 01 as a large split panel, sheets 02 and 03 as a pair, sheets 04 to 06 as register rows. This also avoids the row of three equal cards.
- **Numbering encodes something true.** Sheets are ordered by how much of the mechanical work was Hiranya's, which is stated in the section intro. `Sheet 04 of 06` is a real position in a real set.
- **No card borders.** Separation is space first, then a 3 to 5 percent background shift, then soft elevation. Elevation appears only on things that move on hover.
- **Radius scales with element size**: 2px chips, 4px buttons and small media, 8px panels, 12px full sheets. The hero sheet uses the concentric formula, 12px outer minus 8px padding gives a 4px inner radius.

## Copy rules applied

- No em dashes or en dashes anywhere, and none of the hyphen-as-dash workaround the previous build used.
- No emoji. Arrows are HTML entities inside `aria-hidden` spans.
- en-AU spelling and conventions.
- Every number on the site is real. Where a project has no measured result yet, the page says so explicitly instead of filling the gap. This appears on four of the six sheets.
- The hero names the person, the institution, the three concrete artefacts and the thing being asked for, so swapping in another name breaks it.

## Things not to do next time

- Do not add a scroll reveal. It was removed on purpose.
- Do not add a fourth hue. Extend with tints of the existing three.
- Do not put `--oxide-lift` on the paper surface. It fails contrast there.
- Do not add a hamburger menu. Six nav links wrap fine down to 320px.
- Do not add invented metrics to make the sheets look fuller.
