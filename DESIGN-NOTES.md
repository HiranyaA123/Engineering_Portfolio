# DESIGN-NOTES.md

Running record of design decisions, as `DESIGN-RULES.md` section 14 asks for. Read this before changing the look of anything, so the next pass does not drift back toward the average.

## The brief

```
Subject:                 Portfolio for a second year UNSW mechanical engineering student
                         who co-founded a hospitality software company. Real hardware:
                         competition robots, an autonomous agricultural drone, CubeSat
                         ground station mounts, plus software in production.
Audience:                Graduate recruiters and engineering managers screening for
                         2026/27 vacation programs. They skim, and they have seen
                         several hundred student portfolios.
The page's single job:   Prove that this person has built physical things that work,
                         show who he is in under a minute, and make it trivial to
                         contact him.
Tone:                    Direct, warm, a little dry.
Aesthetic direction:     Print magazine (section 3), engineering edition.
Signature element:       Numbered callouts pinned to real photographs of the hardware.
Locale:                  en-AU.
Constraints:             Static HTML and CSS, GitHub Pages, no build step,
                         no framework, no dependencies.
```

## Why the September 2026 rebuild happened

The previous build (technical drawing sheet direction: grey-green drafting paper, mono labels on everything, line drawings, a title block on every page) was consistent and rule-abiding, and Hiranya's verdict was that it looked like a generic AI portfolio. He was right. The tells were:

- Mono uppercase labels on every section, which is the single most common LLM portfolio habit.
- Abstract line drawings standing in front of real photographs that already existed.
- A hero that described the person instead of showing anything.
- No person anywhere on the page. No voice in the copy. A recruiter could not have said one specific thing about him after reading it.
- A muted palette with the accent used so sparingly that nothing on the page was highlighted.

A survey of portfolios that recruiters and design juries actually remember (Bruno Simon, Raphael Chang, Thanh Tran, the Awwwards and Muzli portfolio lists, hardware portfolio directories) turned up the same handful of devices: open with the real thing at full size; big type with a first person voice; one memorable interactive device; honest, specific copy including what is not finished; a timeline or story; and a contact section that is impossible to miss. The rebuild uses all six.

## Palette

| Token | Hex | Role |
|---|---|---|
| `--bone` | `#efede7` | Ground. Warm bone, not cream. |
| `--bone-2` / `--bone-3` | `#e5e2da` / `#d6d2c7` | Lightness shifts for photo mats and list panels. |
| `--ink` / `--ink-2` / `--ink-3` | `#15171a` / `#3e4247` / `#5c6167` | Text. 15.1:1, 9.4:1, 5.2:1 on bone. |
| `--red` | `#c4301c` | The accent. The colour of the 41103A number plate. 5.9:1 on bone; white on it 5.1:1. |
| `--red-deep` | `#9e2414` | Hover state of red. |
| `--navy` | `#0e1b2e` | Inverted panels (Now, About, callouts, drawing plates). The Pedare uniform. |
| `--red-lift` | `#ff6b4e` | Red on navy only. 6.0:1 there. Never on bone. |

Three hues: bone, ink/navy, red. No gradients. No pure white or black surfaces.

**Rules section 3 check.** The banned reflex is cream near `#F4F1EA` with a serif display and terracotta near `#D97757`. This build has a bone ground that is greyer and cooler than that cream, a heavy grotesque display face, and a true competition red rather than terracotta. The red is derived from the subject: it is on the robot's number plate, the VEX branding and the high strength gears.

## Type

- **Display: Bricolage Grotesque**, weight 800, `wdth` 78 to 92, `opsz` 96. Heavy, slightly eccentric, not on the banned list and not yet a tell. Used for every heading, the index numerals, the timeline years, the email address, buttons, tags and navigation, so the page has one loud voice.
- **Body: Source Serif 4** at 18px, line height 1.6. Kept from the previous build. A serif body under a heavy grotesque is what stops the page reading as a SaaS template.
- **Mono: IBM Plex Mono**, now confined to the callout numbers and the `Sheet 03 of 06` lines on case studies. Everywhere else the mono labels were replaced with the display face in sentence case.

Scale ratio 1.333 from an 18px body. The h1 runs to 7.5rem on a wide screen.

## Signature element

Numbered callouts pinned to a real photograph. The hero photograph of the Over Under robot carries five markers (intake rollers, the 41103A plate, the gear train, pneumatics and wiring, the drivetrain). Each marker is a real `<button>` with `aria-expanded`, so it works on keyboard and touch. Hover and focus reveal the note through CSS alone; a tap toggles it through 40 lines of script. A legend under the photograph repeats the five notes so nobody has to hover to read them. The component is `.annotated` in `base.css` and is reusable on case study pages.

## The one aesthetic risk

The hero headline is a first person sentence with a coloured phrase in it ("I build things that have to work on the day"), sitting over a full width photograph of a robot on a pit table. Both halves are risks by the rules: coloured words in a headline are close to the italic-serif-word tell, and a hero that is one photograph can read as a stock template. Justification: the phrase is the thesis of the whole page (competition, a live venue, a flight test), and the photograph is his robot with his team's number plate on it, annotated with what he built. Neither could be swapped onto someone else's portfolio.

## Copy rules applied

- First person throughout. The hero, the Right now band, the story and the About section are all in his voice.
- Every claim on the page is something already established elsewhere on the site or in the resume. No invented anecdotes, no invented numbers. Where a project has no measured result the page says so.
- Personality comes from specifics rather than jokes: "one drone that is currently being talked into flying straight", "Bugs get found during service, not in a sprint review", the Ask me about list.
- No em dashes or en dashes. No emoji. en-AU spelling.

## Layout decisions worth keeping

- **Rhythm varies down the page**: tall hero with a full width photograph; a thin navy band; deep work section with three alternating spreads and a short ruled list; a year by year story register; a navy About panel; a contact section with a headline sized email address.
- **Six projects, three treatments.** Spreads for the three that are running (CentralPass, VEX, the drone), a ruled list for the three that are finished or being proved. The index numerals encode a real order.
- **The story section is the personality.** Eight rows, 2018 to 2026, with the two earlier robot photographs and the Dallas pit photograph. It is the section a recruiter will remember.
- **No mono labels on section heads.** Eyebrows use `.kicker` in the display face with a short red rule.
- **Pill radius for buttons and tags, 20px for large photographs, 14px for panels, 3px for chips.** Concentric maths on `.photo` (14 outer minus 8 padding).
- **No card borders.** Photo mats are a lightness shift. Tags use a hairline because they are the only element small enough to need one.

## Motion budget

One moment. The five hero markers pop onto the photograph in sequence 500ms after load, once. Everything else is interaction state at 160ms to 320ms. No scroll reveal, and none should be added.

## Photographs

The same five VEX photographs and three CentralPass screenshots as before, all at three widths with `srcset`. The hero eagerly loads the robot at 1000 or 1600 wide with a preload hint; everything else is lazy. The VEX case study leads with the robot photograph under its facts strip. The drone, BlueSat, Sculpt Showdown and trading pages have no photograph. The old placeholder line drawings were removed in September 2026 at Hiranya's request: where there is no photograph the page shows a spec plate (`.spread-media.is-plate`) that lists the real hardware and says a photograph will follow, and the social cards for those projects are typographic. Do not draw stand-in diagrams again.

## Rules from Hiranya, September 2026

- No GitHub link anywhere on the site or the resume. LinkedIn, CentralPass and the resume PDF are the only outbound contact links.
- He is based in Sydney and Adelaide and moves between them. Do not write "Sydney" alone.
- CentralPass is proprietary software he wrote himself over several months, built so venues can replace Uber Eats with direct ordering. The copy must make clear it is hand built, not a template, a no-code tool or a wrapper. The case study's "Built by hand" section lists the subsystems for that reason.
- Every link worth copying (email, LinkedIn, CentralPass, resume) carries `data-copy` and gets a Copy button from `site.js`. The button only appears when the clipboard API exists.

## Things to add when the material exists

- (Done, September 2026) A photograph of Hiranya now sits in the About section: the IAC 2025 portrait in `assets/img/portrait/`.
- A photograph or short clip of ADA2M in the air. Replace the `.spread-media.is-plate` block on the landing page and add a `.case-lead` figure to the drone page.
- Callouts on the CentralPass screenshots and the drone photograph, using `.annotated`.
- A short clip of the robot's autonomous routine or the drone hovering. Video is the one thing the strongest hardware portfolios have that this one does not.

## Things not to do next time

- Do not add a scroll reveal.
- Do not put mono uppercase labels back on section heads.
- Do not add a fourth hue. Extend with tints of bone, ink and red.
- Do not put `--red-lift` on the bone surface. It fails contrast there.
- Do not add a hamburger menu. Five links wrap fine at 320px.
- Do not add invented metrics, anecdotes or quotes to fill space.
