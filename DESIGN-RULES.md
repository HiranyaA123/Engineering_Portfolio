# DESIGN-RULES.md

A portable ruleset for generating websites with an LLM (Claude, ChatGPT, Cursor, v0) that do not read as machine-made and do not fail basic usability.

**How to use it**
- Claude Code / Cursor: save this at the project root as `DESIGN-RULES.md` and reference it in `CLAUDE.md` or `.cursorrules` with "Read DESIGN-RULES.md before writing any UI code."
- Claude or ChatGPT chat: attach the file, or paste Section 1 alone if you are short on context.
- Fill in Section 2 before any code is written. Every rule below assumes those decisions exist.

---

## 1. The short version (paste this alone if nothing else)

You are the design lead at a studio known for work that could not be mistaken for anyone else's. The client has already rejected two templated proposals.

Hard rules:
1. No emoji anywhere: not in copy, not in headings, not as icons, not in commit messages or comments.
2. No em dashes or en dashes in prose. Use a full stop, a colon, a comma, or brackets. Rewrite the sentence if it resists.
3. No purple-to-blue gradients, no lavender accent, no glowing orbs behind the hero.
4. No Inter, Poppins, Geist, Space Grotesk, Manrope, Montserrat, or Roboto as the display face.
5. No row of exactly three equal feature cards with a thin-line icon on top.
6. No centred hero with a small pill badge above the H1.
7. No 1px grey border plus soft shadow on every card. No coloured 3px left-border strip.
8. No dark mode unless it was asked for.
9. No sharp corners in a rounded system. Set a radius scale and use concentric maths when nesting (Section 6).
10. No lorem ipsum, no placeholder stats, no stock photo of a diverse team at a laptop.
11. Commit to one aesthetic direction and hold it on every screen. "Clean and modern" is not a direction; it is the default that produces the problem.
12. Ship the quality floor without announcing it: responsive to 320px, visible keyboard focus, `prefers-reduced-motion` respected, real contrast, every interactive state designed.

Before you write code, state the direction, the palette, the type pairing, and the one signature element. If any of them is what you would produce for any other brief, change it and say what you changed.

---

## 2. Fill this in first (the brief)

Do not skip. If the human left something blank, choose it yourself and state the choice in one line.

```
Subject:                 [what this actually is, concretely]
Audience:                [who lands on it and what they already know]
The page's single job:   [one sentence, one job]
Tone:                    [three adjectives that are not "clean, modern, professional"]
Aesthetic direction:     [pick one from Section 3]
Signature element:       [the one thing this page is remembered by]
Locale:                  [en-AU / en-GB / en-US. Match spelling and currency to it]
Constraints:             [stack, CMS, existing brand, deadline]
```

Distinctive choices come from the subject's own world: its materials, instruments, artefacts, jargon, and physical objects. A structural engineering firm has load diagrams and hatching patterns. A café has menu boards, receipt paper, and tile. Use that, not a generic SaaS vocabulary.

---

## 3. Commit to a direction

Pick one and hold it. Mixing two is how a page ends up looking like nothing.

| Direction | Reads as | Watch out for |
|---|---|---|
| Swiss / editorial grid | Precise, confident, typographic | Becoming a plain Helvetica wall |
| Technical / instrumentation | Engineered, measured, data-forward | Monospace used as decoration |
| Print magazine | Considered, human, opinionated | Illegible pull-quote sizes |
| Brutalist / raw HTML | Deliberate, unpolished, memorable | Becoming genuinely unusable |
| Warm organic | Tactile, human, slower | Turning into a wellness template |
| Archival / documentary | Serious, credible, dense | Grey-on-grey with no focal point |
| Product-clean | Trustworthy, calm, functional | This is the closest to the default. Earn it |

**Three looks to avoid unless the brief explicitly asks:**
1. Cream background near `#F4F1EA`, high-contrast serif display, terracotta accent near `#D97757`. This is currently the most common LLM default and reads as a tell.
2. Near-black background with a single acid-green or vermilion accent.
3. Broadsheet layout with hairline rules, zero radius, and dense newspaper columns.

Each is legitimate for some briefs. None should be chosen by reflex.

---

## 4. Colour

- Cap the palette at three active hues: one dominant (about 60% of the surface), one neutral (about 30%), one sharp accent (about 10%). Extend with tints and shades of those, never new hues.
- Keep semantic colours (success, warning, error, info) separate from brand hues.
- Never pure `#ffffff` or `#000000` for large surfaces. Tint them warm or cool so the page has depth. `#FAF9F6` or `#0E0E10` rather than the extremes.
- Banned by default: purple-to-blue gradients, lavender `#8B5CF6` family accents, Tailwind `indigo-500`, default shadcn grey, gradient text on a big number, glassmorphism, neon glow borders.
- Gradients are allowed when they are subtle, single-hue, and serve depth rather than decoration.
- Derive the palette from the subject. A marine research group has chart blues and buoy orange available; it does not need indigo.
- Measure contrast, do not eyeball it. WCAG 2.1 AA minimum: 4.5:1 for body text, 3:1 for large text and non-text UI. If you can run APCA, target Lc 75 or above for body, 45 or above for large or bold.
- Text over an image or video needs a scrim or overlay that guarantees the ratio at every breakpoint.

---

## 5. Typography

- Two faces minimum: a display face used with restraint, and a body face. Add a utility or mono face only if data or captions need it. Three families is the ceiling.
- Banned as display faces: Inter, Roboto, Open Sans, Poppins, Montserrat, Lato, Geist, Space Grotesk, Manrope. Banned as a pairing: Space Grotesk with Instrument Serif; it has become its own tell.
- Free faces worth reaching for instead: Fraunces, Bricolage Grotesque, Newsreader, Source Serif 4, Literata, Libre Franklin, Archivo (including Expanded), Public Sans, IBM Plex family, Atkinson Hyperlegible, Karla, Syne, Redaction. Fontshare has General Sans, Switzer, Satoshi, Cabinet Grotesk, Zodiak, Erode, Boska, all free for commercial use.
- One mathematical type scale. Use 1.25 for app interfaces, 1.333 for editorial. No arbitrary sizes.
- Body text 16px minimum, 17px to 19px is better for reading. Line height 1.5 to 1.7 for body, 1.05 to 1.2 for large display.
- Measure (line length) between 60 and 80 characters. Set `max-width` in `ch`, not `px`.
- Build hierarchy with weight, size, and space, not with more families or more colours.
- Do not set an entire page in one weight of one face. Do not use all-caps section labels on every section. Do not italicise one serif word inside a sans headline; that pattern is now a tell.
- Tighten letter-spacing on large display text (roughly `-0.02em` and below); leave body alone.
- Load fonts properly: `font-display: swap`, preload the two faces used above the fold, subset to the character set you need.

---

## 6. Shape, radius, borders, and elevation

**Radius**
- Define a scale, not a single value. Something like: `--r-sm: 4px`, `--r-md: 8px`, `--r-lg: 16px`, `--r-full: 999px`. Assign each to a role (inputs and chips small, buttons medium, cards and images large, avatars and pills full).
- Applying one identical radius to every element on the page is itself an AI tell. Radius should scale with element size: a 40px button and a 600px card should not share a 16px corner.
- Nesting rule (concentric corners): `inner radius = outer radius - padding`. A card at 24px radius with 8px padding needs its inner image at 16px. Same value on both makes the gap look thicker at the corners than along the edges, and it reads as amateur work.

```css
.card {
  --radius: 24px;
  --pad: 8px;
  border-radius: var(--radius);
  padding: var(--pad);
}
.card > img {
  border-radius: calc(var(--radius) - var(--pad));
}
```

- If the formula returns zero or less, reduce the padding or increase the outer radius. Do not ship a sharp inner corner inside a rounded outer one.
- Full-bleed sections, table cells, and edge-anchored elements stay square. Rounding something that touches the viewport edge looks like a mistake.
- A zero-radius system is a valid deliberate choice for brutalist or editorial directions. What is not valid is mixing radii at random.

**Borders and separation**
- Default cards to borderless. Separate content in this order and stop as soon as it reads: whitespace, then a 3% to 5% background lightness shift, then soft elevation. A border is the last resort, and never a flat 1px grey line on everything.
- The coloured 3px to 4px left-border strip is the single most reliable signal of AI-generated UI. Use it only for genuine semantic state (an error callout), never as decoration.
- No cards inside cards inside cards. If a block is already inside a bounded surface, it does not need its own box.

**Elevation**
- One shadow scale, two or three steps. Shadows should be large, soft, and low opacity, tinted with the background hue rather than pure black.
- Elevation means interactive or floating. A static content block does not need a shadow.

---

## 7. Layout and structure

- Grid first. Set a column grid and a spacing scale on 8px steps (4px as a half step). No `13px`, no `37px`.
- Proximity carries meaning: space inside a component is smaller than space between components, which is smaller than space between sections.
- Vary section rhythm. If every section is a centred heading over a three-column grid with identical padding, the page is monotonous even though it is technically consistent. Alternate full-bleed, asymmetric, two-column, and edge-anchored treatments.
- Asymmetry is allowed and usually better than another centred stack.
- Banned by reflex: exactly three feature cards in a row; a "01 / 02 / 03" numbered step row when the content is not actually sequential; a horizontal stat banner with invented numbers; a bento grid used as the default; the canned skeleton of hero, three cards, logo strip, pricing, FAQ, footer shipped unchanged.
- Numbering, eyebrows, dividers, and labels must encode something true about the content. If the order does not matter, do not number it.
- The hero is a thesis, not a slot. Open with the most characteristic thing in the subject's world: a real photograph, a live demo, a diagram, a specimen, a menu, a schematic. A big number with a small label and a gradient accent is the template answer.
- Section padding should be generous but not identical everywhere. On a 27in monitor, uniform 120px vertical padding on every section reads as running out of content.
- Test at 320px, 768px, 1280px, and 1920px. No horizontal scroll at any width. No hamburger menu on desktop when there are five links.

---

## 8. Motion

- Motion is a budget, not a topping. One orchestrated moment lands harder than a fade-in on every element.
- Banned: the same generic scroll-triggered fade on every block, bouncing buttons, wiggling icons, animated gradient backgrounds, scroll-jacking, custom cursors, parallax used without reason.
- Every interactive element needs designed states: rest, hover, focus-visible, active, disabled, loading. A hover state that does nothing is worse than none.
- Transitions: 120ms to 200ms for small state changes, 250ms to 400ms for larger ones. Use an ease that is not `linear`. Buttons should ease, not snap.
- Wrap everything in `@media (prefers-reduced-motion: reduce)` and provide a static fallback. This is a floor, not an extra.

---

## 9. Imagery and icons

- No emoji as icons, ever. No emoji in nav items, list bullets, headings, buttons, or body copy.
- Pick one icon set and use it at one stroke weight and one size scale. Do not centre one oversized icon above every heading; when the decoration is bigger than the message, the priorities are backwards.
- Banned imagery: floating 3D abstract blobs, gradient mesh backgrounds, plastic-smooth AI illustration, stock photos of a diverse team laughing at a laptop, generic thin-line icons standing in for content.
- Use real photographs, real screenshots, real documents, real objects from the subject's world. One real image beats six illustrations.
- Every image needs `width`, `height`, and meaningful `alt`. Decorative images get `alt=""`.
- Lazy-load below the fold, eager-load the LCP image, serve modern formats, and do not ship a 3MB hero.

---

## 10. Writing

Copy makes a page feel templated just as fast as the visuals do.

**Mechanics**
- No emoji.
- No em dashes or en dashes. Restructure into two sentences, or use a colon, a comma, or brackets.
- Sentence case for headings and buttons. Not Title Case, not ALL CAPS.
- Active voice. A button says what happens: "Book a table", not "Submit". The action keeps its name through the whole flow, so a "Publish" button produces a "Published" toast.
- Vary sentence length. Uniform 18-word sentences read as machine output.
- Match spelling to the locale in the brief. For Australian audiences: colour, centre, organise, licence (noun), and AUD with a dollar sign.

**Banned words and phrases**
delve, tapestry, realm, harness, unlock, elevate, empower, seamless, seamlessly, robust, leverage (as a verb), cutting-edge, game-changer, revolutionise, transformative, unleash, navigate the landscape, in today's fast-paced world, at the end of the day, it is worth noting, furthermore, moreover, meticulous, pivotal, showcase (as a verb), underscore (as a verb), embark, journey (figurative), testament to, dive into, supercharge, next-level, world-class, best-in-class, holistic, synergy, curated (unless something was literally curated), bespoke (unless it literally is).

**Banned sentence structures**
- "It's not just X, it's Y." Also "This isn't about X, it's about Y." Remove the negation and state the point.
- Two-part headings joined by a colon on every single section.
- Rule of three everywhere: three adjectives, three clauses, three benefits, on repeat.
- Rhetorical question as a section opener ("So what does this mean for you?").
- "Whether you're a X or a Y, we've got you covered."

**Tests the copy must pass**
- *Competitor swap test*: replace your name with a direct competitor's. If it still reads perfectly, the copy is too generic to build trust. Rewrite until it breaks.
- *Specificity test*: the hero must name what this is, who it is for, and what changes. "We help businesses grow" fails. "Rostering software for cafés with under 30 staff" passes.
- *Read-aloud test*: if you would not say it out loud to a customer, do not put it on the page.
- Errors explain what went wrong and how to fix it. They do not apologise and they are never vague. Empty states are an invitation to act, not a mood.

---

## 11. Usability floor

Non-negotiable, regardless of aesthetic direction.

- Users judge a page in roughly 50ms and decide whether to stay within 10 to 20 seconds. The hero must answer "what is this and is it for me" without scrolling.
- One primary action per screen. Competing calls to action cancel each other out.
- Navigation labels name what the user recognises, not how the system is built. "Notifications", not "Webhook config".
- No entry pop-ups, no autoplay audio or video, no auto-rotating carousels, no interstitials on mobile.
- Touch targets 44x44px minimum with 8px between them.
- Forms: label every field visibly, do not rely on placeholder text, ask for the minimum, show inline validation after the field is left rather than on every keystroke, and never wipe the form on error.
- Visible `:focus-visible` outline on every interactive element. Never `outline: none` without a replacement.
- Links look like links. Buttons are `<button>`, links are `<a>`. Never a `<div>` with an `onClick`.
- Semantic HTML: one `<h1>`, headings in order, landmarks (`header`, `nav`, `main`, `footer`), lists as lists.
- Every link goes somewhere. Every button does something. No dead ends, and write a real 404 page.
- Include the boring trust signals: real contact details, real address, real hours, real ABN if it applies, a privacy policy that exists.
- Do not invent testimonials, client logos, or "10,000+ happy customers". Fabricated proof is worse than no proof.

---

## 12. Performance floor

- Largest Contentful Paint under 2.5s, Cumulative Layout Shift under 0.1, Interaction to Next Paint under 200ms, on a mid-range phone on 4G.
- Reserve space for images, embeds, and ads so nothing jumps.
- No web font loaded that is not used. No icon library imported whole for six icons. No animation library for one fade.
- Prefer CSS over JavaScript for anything CSS can do.
- The page must render something useful without JavaScript where the content is static.

---

## 13. Self-audit before calling it done

Run this every time. Any fail means fix and re-run the whole pass.

- [ ] Direction, palette, type pairing, and signature element were decided before code, and stated.
- [ ] Three active hues or fewer. No purple gradient. No pure black or white surfaces.
- [ ] Display face is not on the banned list. Body text is 16px or larger. Measure is 60 to 80ch.
- [ ] Radius scale defined and role-assigned. Nested radii use `outer - padding`. No stray sharp corners.
- [ ] Cards separated by space or background shift before any border is used. No coloured left strips. No nested cards.
- [ ] Spacing on the 8px grid. Section rhythm varies down the page.
- [ ] No emoji anywhere. No em dashes anywhere. No banned words or structures in the copy.
- [ ] Copy fails the competitor swap test (it should break when the name is swapped).
- [ ] Every interactive state designed: hover, focus-visible, active, disabled, loading, empty, error.
- [ ] Contrast measured, not guessed. Keyboard path complete. `prefers-reduced-motion` handled.
- [ ] Works at 320px with no horizontal scroll. Touch targets 44px.
- [ ] *Squint test*: shrink the page to a thumbnail. If every section reads as the same grey box, the hierarchy has failed.
- [ ] *Screenshot review*: review the rendered page, not the code. You ship what renders.
- [ ] *Sameness test*: would this design be a reasonable answer to a completely different brief? If yes, it is not designed for this one.

---

## 14. Prompting notes

- Adjectives do not fix this. "Make it look modern" returns the average. Constraints fix it: a named typeface, a named palette, a layout principle, a tone.
- Ask the model to produce the design plan first (palette as 4 to 6 named hex values, two or three typefaces with roles, a layout concept, one signature element), critique the plan against this file, then build.
- Ask for one real aesthetic risk per project, with a one-line justification. A page with no risk is usually a page with no memory.
- When you iterate, change one structural thing per section rather than restyling globally. Global restyles drift back towards the average.
- Keep a running `DESIGN-NOTES.md` of what has been tried across projects. Human designers avoid repeating themselves because they remember; the model needs the notes.
