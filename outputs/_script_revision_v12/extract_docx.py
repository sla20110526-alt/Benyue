from __future__ import annotations

import json
import sys
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.ns import qn


def iter_block_items(document: Document):
    body = document.element.body
    for child in body.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, document)
        elif child.tag == qn("w:tbl"):
            yield Table(child, document)


def main() -> None:
    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    document = Document(source)

    blocks: list[dict] = []
    for index, block in enumerate(iter_block_items(document), start=1):
        if isinstance(block, Paragraph):
            blocks.append(
                {
                    "index": index,
                    "type": "paragraph",
                    "style": block.style.name if block.style else "",
                    "text": block.text,
                }
            )
        else:
            rows = []
            for row in block.rows:
                rows.append([cell.text for cell in row.cells])
            blocks.append(
                {
                    "index": index,
                    "type": "table",
                    "style": block.style.name if block.style else "",
                    "rows": rows,
                }
            )

    sections = []
    for index, section in enumerate(document.sections, start=1):
        sections.append(
            {
                "index": index,
                "page_width_emu": section.page_width,
                "page_height_emu": section.page_height,
                "top_margin_emu": section.top_margin,
                "bottom_margin_emu": section.bottom_margin,
                "left_margin_emu": section.left_margin,
                "right_margin_emu": section.right_margin,
                "header_distance_emu": section.header_distance,
                "footer_distance_emu": section.footer_distance,
            }
        )

    payload = {
        "source": str(source.resolve()),
        "block_count": len(blocks),
        "section_count": len(sections),
        "sections": sections,
        "blocks": blocks,
    }
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
