"""PDF processing pipeline: extract page images and text from uploaded exam PDFs."""

import os
import shutil
import fitz  # pymupdf


def process_pdf(pdf_path: str, output_dir: str, dpi: int = 200) -> dict:
    """Extract page images and text from a PDF.

    Args:
        pdf_path: Path to the PDF file.
        output_dir: Directory to save extracted images.
        dpi: Resolution for page images.

    Returns:
        dict with page_count, pages (list of {page_num, image_path, text}).
    """
    os.makedirs(output_dir, exist_ok=True)

    doc = fitz.open(pdf_path)
    pages = []

    for i in range(doc.page_count):
        page = doc[i]
        # Extract image
        pix = page.get_pixmap(dpi=dpi)
        image_filename = f"page_{i + 1:02d}.png"
        image_path = os.path.join(output_dir, image_filename)
        pix.save(image_path)

        # Extract text
        text = page.get_text()

        pages.append({
            "page_num": i + 1,
            "image_path": image_filename,
            "text": text.strip(),
        })

    doc.close()

    return {
        "page_count": len(pages),
        "pages": pages,
    }


def copy_existing_images(source_dir: str, dest_dir: str):
    """Copy already-extracted page images to the uploads directory."""
    os.makedirs(dest_dir, exist_ok=True)
    for f in sorted(os.listdir(source_dir)):
        if f.endswith(".png"):
            shutil.copy2(os.path.join(source_dir, f), os.path.join(dest_dir, f))


def crop_question_image(
    pdf_path: str,
    page_0indexed: int,
    top_frac: float,
    bottom_frac: float,
    output_path: str,
    dpi: int = 200,
    margin_frac: float = 0.02,
):
    """Crop a region from a PDF page and save as PNG.

    Args:
        pdf_path: Path to the PDF.
        page_0indexed: 0-indexed page number.
        top_frac: Top of crop region as fraction of page height (0.0 = top).
        bottom_frac: Bottom of crop region as fraction of page height (1.0 = bottom).
        output_path: Where to save the cropped PNG.
        dpi: Resolution.
        margin_frac: Extra margin above/below as fraction of page height.
    """
    doc = fitz.open(pdf_path)
    page = doc[page_0indexed]
    rect = page.rect
    h = rect.height
    w = rect.width

    y0 = max(0, h * top_frac - h * margin_frac)
    y1 = min(h, h * bottom_frac + h * margin_frac)

    clip = fitz.Rect(0, y0, w, y1)
    pix = page.get_pixmap(dpi=dpi, clip=clip)
    pix.save(output_path)
    doc.close()
