"""
starter/app.py — Meridian Freight & Logistics

============================ YOUR TASK ============================
This is the FastAPI backend. Every TODO below corresponds to a
prediction you made in Part 1 of the worksheet. Implement each one to
match your reasoning — if a TODO's implementation contradicts what you
predicted, that's worth noticing and discussing, not silently ignoring.
======================================================================

Run with: uvicorn app:app --reload --port 8000
(from inside the starter/ folder, AFTER build_vectorstore.py has run)
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "toolkit"))

from dotenv import load_dotenv
from fastapi import FastAPI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from openai import OpenAI

from context import assemble_context
from pii import redact_pii
from confidence import confidence_level, should_refuse, best_score_from_results
from observability import Tracer

# TODO A: Does this scenario need hybrid retrieval (BM25 + vector)?
# Think about the pay-band CSV data specifically — location codes like
# "MFL-PUN-01" and role bands like "Band B" are exact strings a manager
# might type verbatim. If you predicted hybrid retrieval is needed,
# import and use HybridIndex from toolkit/hybrid_retrieval.py here.
# If you predicted plain vector search is enough, explain why in a
# comment and skip the import.

# TODO B: Does this scenario need cross-encoder reranking? Consider:
# most Meridian questions are fairly narrow ("what's my leave
# entitlement") rather than broad multi-topic questions. Would
# reranking change much here, or add latency without much benefit?
# Make a decision and import toolkit/reranking.py only if you use it.

# TODO C: Does this scenario need prompt-injection defence? These are
# INTERNAL HR documents Meridian controls and reviews before
# publishing — is the injection risk here the same as it would be for,
# say, a document ingesting live customer complaint text? Decide, and
# justify it in your README.

import audit_log

load_dotenv()

CHAT_MODEL = "gpt-5.4-mini"
EMBED_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "meridian_documents"
PERSIST_DIR = "./chroma_store"
TOP_K = 3

# TODO D: Compliance mentioned a near-miss where a manager acted on an
# OUTDATED policy version. Given that, should this system's confidence
# threshold for refusing to answer be STRICTER or LOOSER than the
# toolkit's defaults (confidence.py: HIGH_THRESHOLD=0.5, MEDIUM=0.3)?
# Set your own values here if you're overriding the defaults, and
# explain why in your README.

SYSTEM_PROMPT = """
You are the Meridian Freight & Logistics HR Assistant.

Tone: TODO E — decide this. Meridian's workforce is depot-based, not
office-based. What tone fits a Depot Manager checking a policy on their
phone between shifts?

Grounding rule: Only answer using the excerpts provided. Every factual
claim MUST be followed by a citation in the form (Source: <filename>).
If the excerpts don't cover the question, say so plainly and do not guess.

TODO F: Compliance specifically asked that answers show which DOCUMENT
VERSION they came from, not just the filename — does your citation
instruction above actually require that, or only the filename? Revise
if needed.
"""

client = OpenAI()
embeddings = OpenAIEmbeddings(model=EMBED_MODEL)
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR,
)

app = FastAPI(title="Meridian Freight & Logistics HR Assistant")


@app.get("/")
def root():
    return {"message": "Meridian HR Assistant is running. Try /ask?q=your+question"}


@app.get("/ask")
def ask(q: str, top_k: int = TOP_K):
    tracer = Tracer()

    # TODO G: PII redaction on the way IN. A depot manager might paste
    # their own phone number into a question without thinking about it
    # ("my number is ..., can you check my leave balance?"). Redact the
    # incoming question before it's used or logged.
    with tracer.stage("pii_redact_input"):
        redacted_question = q  # TODO: actually call redact_pii() here

    # TODO H: Retrieval. Implement EITHER plain vector search OR hybrid
    # search, based on your TODO A decision. Store results as a list of
    # (doc, score) tuples in `raw_results`.
    with tracer.stage("retrieval"):
        raw_results = []  # TODO: implement

    best_score = best_score_from_results(raw_results)
    level = confidence_level(best_score)

    # TODO I: Refusal guardrail. If should_refuse(best_score) is True,
    # log the refusal (see Pramaan's app.py from Module 7 for the exact
    # pattern) and return an "I don't know" response WITHOUT calling
    # the LLM at all.

    # TODO J: If you decided reranking is needed (TODO B), apply it here
    # to `raw_results` before context assembly. If not, just use
    # raw_results directly.

    # TODO K: Context assembly — reuse assemble_context() from
    # toolkit/context.py, same as every earlier lab.
    context_text, used_results = "", []  # TODO: implement

    # TODO L: Build the user_prompt and call the LLM, same pattern as
    # every earlier lab. If you decided injection defence IS needed
    # (TODO C), wrap each chunk as untrusted data here instead of using
    # the raw chunk text directly.

    # TODO M: Audit logging. Log this request using audit_log.log_request(),
    # capturing at minimum: the redacted question, retrieved sources and
    # scores, confidence level, the answer, cited sources, and latency.

    return {
        "question": redacted_question,
        "confidence": level,
        # TODO N: fill in the rest of the response shape — retrieved_chunks,
        # answer, sources, trace — following the pattern from earlier labs.
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
