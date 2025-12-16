# import cv2
# import pytesseract
# from PIL import Image

# # -------------------------------------------------
# # CONFIG
# # -------------------------------------------------
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# # -------------------------------------------------
# # TEXT EXTRACTION
# # -------------------------------------------------
# def extract_full_text(image_path):
#     image = Image.open(image_path)
#     text = pytesseract.image_to_string(image, config="--psm 6")
#     return text.strip()


# # -------------------------------------------------
# # TABLE EXTRACTION (OpenCV + Tesseract)
# # -------------------------------------------------
# def extract_table(image_path):
#     img = cv2.imread(image_path)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Binary image
#     _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

#     # Detect horizontal lines
#     horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
#     horizontal = cv2.morphologyEx(binary, cv2.MORPH_OPEN, horizontal_kernel)

#     # Detect vertical lines
#     vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 40))
#     vertical = cv2.morphologyEx(binary, cv2.MORPH_OPEN, vertical_kernel)

#     # Combine lines
#     table_mask = cv2.add(horizontal, vertical)

#     # Find contours
#     contours, _ = cv2.findContours(
#         table_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
#     )

#     # Extract table cells
#     cells = []
#     for cnt in contours:
#         x, y, w, h = cv2.boundingRect(cnt)
#         if w > 80 and h > 25:  # remove noise
#             cells.append((x, y, w, h))

#     # Sort cells
#     cells = sorted(cells, key=lambda b: (b[1], b[0]))

#     rows = []
#     current_row = []
#     last_y = None

#     for x, y, w, h in cells:
#         cell_img = gray[y:y+h, x:x+w]

#         text = pytesseract.image_to_string(
#             cell_img,
#             config="--psm 6"
#         ).strip()

#         if not text:
#             text = "-"

#         if last_y is None or abs(y - last_y) < 15:
#             current_row.append(text)
#         else:
#             rows.append(current_row)
#             current_row = [text]

#         last_y = y

#     if current_row:
#         rows.append(current_row)

#     return rows


# # -------------------------------------------------
# # MAIN
# # -------------------------------------------------
# if __name__ == "__main__":
#     image_path = input("Enter image path: ")

#     print("\n" + "=" * 70)
#     print("📄 FULL TEXT EXTRACTED")
#     print("=" * 70)
#     print(extract_full_text(image_path))

#     print("\n" + "=" * 70)
#     print("📊 TABLE DATA EXTRACTED")
#     print("=" * 70)

#     table = extract_table(image_path)

#     if not table:
#         print("❌ No table detected")
#     else:
#         for row in table:
#             print(" | ".join(row))

#     print("\n✅ Done (nothing saved)")


# import pdfplumber
# import camelot

# PDF_PATH = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\test_invoices\sampleinvoice.pdf"


# def extract_text_from_pdf(pdf_path):
#     print("\n" + "=" * 70)
#     print("📄 FULL TEXT EXTRACTED (FROM PDF)")
#     print("=" * 70)

#     with pdfplumber.open(pdf_path) as pdf:
#         for i, page in enumerate(pdf.pages, start=1):
#             text = page.extract_text()
#             if text:
#                 print(f"\n--- Page {i} ---\n")
#                 print(text)


# def extract_tables_from_pdf(pdf_path):
#     print("\n" + "=" * 70)
#     print("📊 TABLE DATA EXTRACTED (FROM PDF)")
#     print("=" * 70)

#     tables = camelot.read_pdf(
#         pdf_path,
#         pages="all",
#         flavor="lattice"   # PERFECT for bordered invoice tables
#     )

#     if tables.n == 0:
#         print("❌ No tables detected")
#         return

#     for i, table in enumerate(tables, start=1):
#         print(f"\n--- Table {i} ---\n")
#         print(table.df.to_string(index=False))


# if __name__ == "__main__":
#     extract_text_from_pdf(PDF_PATH)
#     extract_tables_from_pdf(PDF_PATH)

#     print("\n✅ Done (nothing saved)")


import pdfplumber
import camelot
import pandas as pd
from textwrap import fill

PDF_PATH = r"C:\My Programs\Machine Learning Project\InvoiceXtract-AI\backend\test_invoices\sampleinvoice.pdf"


# -------------------------------------------------
# UTILS
# -------------------------------------------------
def print_title(title):
    print("\n" + "=" * 80)
    print(f"{title.center(80)}")
    print("=" * 80)


def print_subtitle(title):
    print("\n" + "-" * 80)
    print(f"{title}")
    print("-" * 80)


def print_wrapped(text, width=80):
    for line in text.split("\n"):
        print(fill(line, width))


def print_table(df: pd.DataFrame):
    print(df.to_string(index=False))


# -------------------------------------------------
# TEXT EXTRACTION (FORMATTED)
# -------------------------------------------------
def print_text_from_pdf(pdf_path):
    print_title("FULL TEXT EXTRACTED (PDF)")

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue

            print_subtitle(f"PAGE {i}")
            print_wrapped(text)


# -------------------------------------------------
# TABLE EXTRACTION (FORMATTED)
# -------------------------------------------------
def print_tables_from_pdf(pdf_path):
    print_title("TABLE DATA EXTRACTED (PDF)")

    tables = camelot.read_pdf(
        pdf_path,
        pages="all",
        flavor="lattice"
    )

    if tables.n == 0:
        print("❌ No tables detected")
        return

    for idx, table in enumerate(tables, start=1):
        df = table.df

        # Clean headers if present
        if len(df) > 1:
            df.columns = [c.replace("\n", " ").strip() for c in df.iloc[0]]
            df = df.iloc[1:].reset_index(drop=True)

        print_subtitle(f"TABLE {idx}")
        print_table(df)


# -------------------------------------------------
# MAIN
# -------------------------------------------------
if __name__ == "__main__":
    print_text_from_pdf(PDF_PATH)
    print_tables_from_pdf(PDF_PATH)

    print("\n" + "=" * 80)
    print("✅ DONE – CLEAN, READABLE OUTPUT (NOTHING SAVED)")
    print("=" * 80)
