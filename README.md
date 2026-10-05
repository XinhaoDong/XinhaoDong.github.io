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

## Updating the CHIP paper

The homepage title, Paper button, and CV share the stable public URL
[`assets/papers/who-gets-protection.pdf`](https://xinhaodong.github.io/assets/papers/who-gets-protection.pdf).
The current file is the 51-page v9 manuscript dated 4 October 2026, with the
author's name and affiliation added to the first page. It remains listed as a
working paper; submission status is not displayed.

The research repository is private. Its source changes and Actions artifacts do
not automatically update this public copy. Keep that repository private and publish
only the intended public manuscript here. GitHub Pages serves a replacement at the
same URL once the website's `main` branch deploys; existing links need no changes.

To refresh this copy from a local checkout, first build the research PDFs with
`bash scripts/build_pdfs.sh` from the CHIP repository. Then, from this website
checkout (Python requires `pypdf` and `reportlab`):

```bash
python3 scripts/add_public_authors.py \
  /path/to/CHIP_Project/.build/pdf/manuscript-v9.pdf \
  assets/papers/who-gets-protection.pdf \
  --title 'Who Gets Protection? Interprovincial Inequality in Social Protection after Land Expropriation in China' \
  --authors 'Xinhao Dong' \
  --affiliation 'Department of Economics, Simon Fraser University' \
  --author-top 184
python3 scripts/build_cv.py assets/cv/CV_XinhaoDong.pdf
```

Check the first-page author placement if the manuscript layout changes, verify
that all original pages are retained, and update the title and summary in
`index.html` and `scripts/build_cv.py` when needed. Publish the resulting
files to the website's `main` branch and verify the live PDFs after deployment.

Camera originals are intentionally not committed. Keep originals outside the
repository, remove private EXIF/GPS metadata, and generate responsive web
derivatives before publishing. The current collection uses 640, 1280, and up
to 2400-pixel widths so browsers can choose an appropriate file.
