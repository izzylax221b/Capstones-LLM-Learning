"""
starter/build_vectorstore.py — Meridian Freight & Logistics

============================ YOUR TASK ============================
Fill in the TODOs below based on the predictions you wrote in Part 1
of the worksheet. Don't just make it run — make your choices match
your reasoning about THIS client's specific needs.
======================================================================

Read documents/, redact PII, chunk, embed, and store in ChromaDB.
"""
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "toolkit"))

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# TODO 1: Import the correct loader functions for EACH format Meridian
# gave you (PDF, HTML, CSV, JSON) from toolkit/loaders.py. The CSV and
# JSON loaders need extra arguments (id_column / list_key) — check
# loaders.py's docstrings for what those documents actually need.
#
#     from loaders import load_pdf, load_html, load_csv, load_json

from chunking import chunk_text
from pii import redact_pii

load_dotenv()

EMBED_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "meridian_documents"
PERSIST_DIR = "./chroma_store"

# TODO 2: Which chunking strategy did you predict for the LEAVE POLICY
# PDF, and why? Set it here:
CHUNK_STRATEGY = "???"  # fixed | overlap | sentence | heading_aware | semantic

# TODO 3: Does the CSV pay-band data need chunking at all, or should
# each row simply become its own single chunk (no further splitting)?
# Write your reasoning as a comment, then implement accordingly below.


def build():
    print("=" * 64)
    print(f"Meridian Freight & Logistics — Building the Knowledge Base")
    print(f"Chunking strategy in use: {CHUNK_STRATEGY}")
    print("=" * 64)

    filepaths = sorted(glob.glob("../documents/*"))
    all_documents = []
    total_pii_redactions = {}

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        print(f"\nProcessing {filename} ...")

        # TODO 4: Call the correct loader for this file's extension.
        # raw_units = ...

        # TODO 5: For each unit, redact PII BEFORE chunking (ingest-time
        # PII handling — why does that ordering matter?).

        # TODO 6: Chunk appropriately — remember TODO 3's decision for
        # the CSV file specifically; it may not need the same treatment
        # as the PDF and HTML documents.

        # TODO 7: Attach metadata to every chunk: at minimum source and
        # chunk_index. Given Compliance's concern about citing the exact
        # DOCUMENT VERSION, what else should you extract and attach here?
        pass

    print(f"\nTotal chunks to embed: {len(all_documents)}")
    if total_pii_redactions:
        print(f"PII redacted at ingest: {total_pii_redactions}")

    # TODO 8: Embed and store in ChromaDB (same pattern as every earlier lab).

    print("Build complete. Next: fill in ../starter/app.py")


if __name__ == "__main__":
    build()
