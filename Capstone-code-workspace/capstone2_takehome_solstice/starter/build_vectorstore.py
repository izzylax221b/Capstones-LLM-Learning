"""
starter/build_vectorstore.py — Solstice Insurance (Claims Support)

============================ YOUR TASK ============================
This is a TAKE-HOME assignment. Fill in every TODO based on the
predictions you wrote in Part 1 of the worksheet, using your OWN
reasoning about Solstice's specific requirements — not by copying
Meridian's answers. The two scenarios have genuinely different
technical demands; a matching answer to Meridian's would likely be
WRONG here.
======================================================================
"""
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "toolkit"))

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

# TODO 1: Import the correct loader functions from toolkit/loaders.py.
# The CSV here has a claim_id column (not location_code like Meridian's);
# the JSON's top-level list is called "coverage_tiers" (not
# "open_positions"). Check both files directly before assuming.

from chunking import chunk_text
from pii import redact_pii

load_dotenv()

EMBED_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "solstice_documents"
PERSIST_DIR = "./chroma_store"

# TODO 2: Which chunking strategy fits the Claims Processing SOP?
# Open the PDF (or its source text) and look at its structure closely —
# does it use clean numbered headings like Meridian's Leave Policy, or
# is it written in flowing paragraphs? Your answer should follow from
# what you actually observe, not an assumption carried over from
# Capstone 1.
CHUNK_STRATEGY = "???"

# TODO 3: The denial log's "customer_note" column contains UNREVIEWED,
# free-text customer input. Does this change how you think about what
# happens to this data during ingestion, beyond just chunking? (Hint:
# re-read Section D of the client brief carefully.)


def build():
    print("=" * 64)
    print("Solstice Insurance — Building the Knowledge Base")
    print(f"Chunking strategy in use: {CHUNK_STRATEGY}")
    print("=" * 64)

    filepaths = sorted(glob.glob("../documents/*"))
    all_documents = []
    total_pii_redactions = {}

    for filepath in filepaths:
        filename = os.path.basename(filepath)
        print(f"\nProcessing {filename} ...")

        # TODO 4: Load, redact PII, chunk, and build Document objects
        # with metadata — same overall shape as every earlier lab, but
        # verify your loader arguments match THIS client's actual file
        # structure (see TODO 1).
        pass

    print(f"\nTotal chunks to embed: {len(all_documents)}")
    if total_pii_redactions:
        print(f"PII redacted at ingest: {total_pii_redactions}")

    # TODO 5: Embed and store in ChromaDB.

    print("Build complete. Next: fill in ../starter/app.py")


if __name__ == "__main__":
    build()
