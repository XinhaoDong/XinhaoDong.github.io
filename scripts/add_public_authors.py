"""Add a compact author block to the first page of an anonymous manuscript PDF.

The input remains untouched. All original pages and their text are retained.
"""

import argparse
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("output")
    parser.add_argument("--title", required=True)
    parser.add_argument("--authors", required=True)
    parser.add_argument("--affiliation", required=True)
    parser.add_argument("--author-top", required=True, type=float,
                        help="Author baseline measured from the top of page 1, in points")
    args = parser.parse_args()

    reader = PdfReader(args.source)
    writer = PdfWriter()
    # Preserve the document's bookmarks and named destinations as well as pages.
    writer.clone_document_from_reader(reader)
    first = writer.pages[0]
    width = float(first.mediabox.width)
    height = float(first.mediabox.height)
    overlay_bytes = BytesIO()
    layer = canvas.Canvas(overlay_bytes, pagesize=(width, height))
    layer.setFont("Times-Roman", 11)
    layer.drawCentredString(width / 2, height - args.author_top, args.authors)
    layer.setFillColorRGB(0.28, 0.28, 0.28)
    layer.setFont("Times-Italic", 9)
    layer.drawCentredString(width / 2, height - args.author_top - 15,
                            args.affiliation)
    layer.save()
    overlay_bytes.seek(0)
    first.merge_page(PdfReader(overlay_bytes).pages[0])

    writer.add_metadata({
        "/Title": args.title,
        "/Author": args.authors,
        "/Subject": "Public author version",
    })
    with open(args.output, "wb") as stream:
        writer.write(stream)


if __name__ == "__main__":
    main()
