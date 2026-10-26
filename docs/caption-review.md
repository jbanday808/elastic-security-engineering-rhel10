
# Caption verification and publication review

## Changes

- Added 26 lossless PNGs in `assets/screenshots/captioned/`, retaining the original filenames.
- Appended white panels with 24 px DejaVu Sans text, bold figure labels, 32 px margins, and 36 px line spacing. Text wraps to each screenshot's original width.
- Used the exact descriptions in `figure-captions.md`, which match the supplied figure descriptions.
- Updated the gallery to use captioned images in the four requested categories, removing repeated visible headings/descriptions for Figures 1–26. Image alternative text retains descriptions for accessibility.
- Updated the README with category links, a captioned preview, and regeneration instructions.
- Added `scripts/caption-screenshots.py` and `assets/screenshots/captioned/original-sha256.json` for reproducibility and original-file verification.

## Verification

All 26 numbered screenshots were present, with one source file per prefix. Each output has the same width as its source and additional height only below the original. Every pixel in the original screenshot area was compared against the source and matched exactly. Embedded PNG caption metadata was checked against the figure index for all 26 images. SHA-256 hashes confirmed that all original screenshots and Figure 00 were unchanged during generation. Figure 00's gallery entry and architecture image were left intact.

All image paths in the README and gallery were checked locally, including all 26 captioned gallery images. The original inventory check also passed. GitHub rendering was not tested on a remote repository; the links use standard relative GitHub Markdown paths. A representative long caption (Figure 22) was visually inspected for wrapping, bold label, alignment, and panel spacing; all images use the same measured text layout.

## Screenshot security review

Visual review covered all 26 original screenshots. No visible plaintext password, enrollment token, API key, or cloud client secret was identified. This is a visual review of visible content, not proof that hidden or truncated values contain no secrets. No OCR tool was available.

Potential information exposure retained in both originals and captioned copies:

| Figures | Visible information |
|---|---|
| 1–26 | Elastic Cloud deployment hostname in browser address bars, dashboard paths/identifiers, browser profile initials, and capture times |
| 1, 4 | Agent/host identifiers and endpoint metadata |
| 1–6, 9, 12, 17, 23–24 | Lab hostnames, service details, logs, or command activity |
| 16, 22–24 | Usernames including `jbanday`, `root`, and service accounts |
| 23, 25 | Private source IP `172.25.250.11` |

Figure 22 and Figure 25 descriptions intentionally include the username and private IP specified in the task. No redactions were applied because the original screenshot content must remain intact. Review whether these identifiers are acceptable for public release. The existing security publication checklist separately reports credentials in original deployment notes; those notes were outside this screenshot review.

## Commit status

No files were committed, staged, or pushed. The supplied workspace's `.git` directory contains no usable Git repository metadata, so `git status` and Git diff verification were unavailable.
