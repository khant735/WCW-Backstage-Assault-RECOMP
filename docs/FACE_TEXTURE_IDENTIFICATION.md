# Wrestler face texture identification

User-supplied rough guide, 2026-11-26. Order is transcription order, not texture numbering. Names normalized for spelling. Sarge's suggested association with WWF War Zone / Attitude is unverified.

![Extracted face reference sheet](../download%20%2817%29.png)

| Character | Sheet ID | Identification status | VRAM / CLUT / hash / replacement PNG |
|---|---|---|---|
| CAW (Create-a-Wrestler) | Unknown | Name supplied; ID unresolved | Pending |
| David Flair | Unknown | Name supplied; ID unresolved | Pending |
| Bam Bam Bigelow | Unknown | Name supplied; ID unresolved | Pending |
| Diamond Dallas Page | Unknown | Name supplied; ID unresolved | Pending |
| Disco Inferno | Unknown | Name supplied; ID unresolved | Pending |
| Eric Bischoff | Unknown | Name supplied; ID unresolved | Pending |
| Goldberg | Unknown | Name supplied; ID unresolved | Pending |
| Hulk Hogan | Unknown | Name supplied; ID unresolved | Pending |
| Jeff Jarrett | Unknown | Name supplied; ID unresolved | Pending |
| Jimmy Hart | Unknown | Name supplied; ID unresolved | Pending |
| Kevin Nash | Unknown | Name supplied; ID unresolved | Pending |
| Billy Kidman | Unknown | Name supplied; ID unresolved | Pending |
| La Parka | Unknown | Name supplied; ID unresolved | Pending |
| Rey Mysterio Jr. | Unknown | Name supplied; ID unresolved | Pending |
| Ric Flair | Unknown | Name supplied; ID unresolved | Pending |
| Scott Hall / Razor Ramon | Unknown | Name supplied; ID unresolved | Pending |
| Scott Steiner | Unknown | Name supplied; ID unresolved | Pending |
| Sarge (trainer) | Unknown | Name supplied; ID unresolved | Pending |
| Sid Vicious | Unknown | Name supplied; ID unresolved | Pending |
| Stevie Ray | 33? | Tentative | Pending |
| Sting | Unknown | Name supplied; ID unresolved | Pending |
| Tank Abbott | Unknown | Name supplied; ID unresolved | Pending |
| Bret Hart | Unknown | Name supplied; ID unresolved | Pending |
| Torrie Wilson | Unknown | Name supplied; ID unresolved | Pending |
| Vampiro | Unknown | Name supplied; ID unresolved | Pending |
| Buff Bagwell | Unknown | Name supplied; ID unresolved | Pending |
| Lance Storm | 42 or 50? | Tentative | Pending |
| Booker T | 47 | User identified; runtime unverified | Pending |

## Replacement mapping requirements

- Treat sheet IDs as reference labels, not verified runtime texture IDs.
- Capture texture page, VRAM rectangle, pixel format, CLUT coordinates and palette, and source texture hash during controlled character selection and gameplay.
- Confirm the same texture identity across frames and palette variants before enabling replacement.
- Record replacement PNG paths only after matching the existing mod loader's naming convention.
- Keep original textures as fallback; do not enable replacements for unresolved identities.

No runtime mapping or replacement is implemented by this document.
