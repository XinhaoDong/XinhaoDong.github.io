# Xinhao Dong — personal website

This repository contains the static site published at
[`xinhaodong.github.io`](https://xinhaodong.github.io/).

## Structure

- `index.html` — academic homepage and research
- `photography/index.html` — photography collection and lightbox
- `assets/css/site.css` — shared visual system and responsive layout
- `assets/js/site.js` — mobile navigation and gallery interaction
- `assets/photos/` — responsive WebP and JPEG derivatives
- `assets/cv/` — current public CV
- `assets/papers/` — public versions of research PDFs
- `assets/slides/` — presentation PDFs linked from the research page
- `scripts/build_cv.py` — editable CV source; rebuilds the public PDF
- `scripts/add_public_authors.py` — adds author details to a public copy of an anonymous manuscript

Paper and CV links use relative paths, so GitHub Pages serves the files from
this repository without Dropbox uploads. The anonymous submission PDFs in the
research directories are preserved; the public versions here add author details
to their first pages. The pension and migration paper retains its collaborator
link. To update the CV, rebuild `assets/cv/CV_XinhaoDong.pdf` and also replace
the local administrative copy.

Camera originals are intentionally not committed. Keep originals outside the
repository, remove private EXIF/GPS metadata, and generate responsive web
derivatives before publishing. The current collection uses 640, 1280, and up
to 2400-pixel widths so browsers can choose an appropriate file.
