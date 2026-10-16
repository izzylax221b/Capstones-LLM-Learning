"""
starter/app.py — Solstice Insurance (Claims Support)

============================ YOUR TASK ============================
Implement every TODO based on YOUR predictions from Part 1. This
client's risk profile is different from Meridian's — regulatory
sensitivity, unreviewed free-text input, and broader multi-reason
questions all point toward different technical choices in places.
======================================================================

Run with: uvicorn app:app --reload --port 8000
(from inside starter/, AFTER build_vectorstore.py has run)
"""
import os
import sys

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

# TODO A: Retrieval pattern. Do location/claim-style exact codes matter
# here the way they did for Meridian? (Look at claim_id values like
# "CLM-88309" — would an agent ever type one verbatim?) Decide hybrid
# vs. plain vector search and justify it — don't just copy Meridian's
# choice without re-checking whether the same reasoning actually applies.

# TODO B: Reranking. The client brief specifically says agents want a
# broad question to surface ALL distinct relevant reasons, not just the
# single closest match. Does that change your Part 1 prediction on
# reranking compared to Meridian's narrower, single-fact questions?

# TODO C: Prompt-injection defence. The denial log's customer_note field
# is UNREVIEWED free text — you already proved (in your loader testing)
# that at least one row contains injection-style phrasing. Is this
# optional here the way it was for Meridian's internally-authored
# documents? Implement wrap_untrusted() and check_retrieved_chunks()
# from toolkit/injection_defense.py accordingly.

import audit_log

load_dotenv()

CHAT_MODEL = "gpt-5.4-mini"
EMBED_MODEL = "text-embedding-3-small"
COLLECTION_NAME = "solstice_documents"
PERSIST_DIR = "./chroma_store"
TOP_K = 3

# TODO D: Confidence threshold. Compliance called an unsupported claims
# answer "a regulatory incident, not just a bad customer experience."
# Given that — and given Meridian's threshold was already raised from
# defaults for a LESS severe concern — where should Solstice's
# threshold land? Set your own values and justify them.

SYSTEM_PROMPT = """
You are the Solstice Insurance Claims Support Assistant.

Tone: TODO E — this is an INTERNAL tool for claims agents, not directly
customer-facing (yet). Does that change the tone compared to Meridian's
depot-manager-facing assistant?

Grounding rule: Only answer using the excerpts provided. Every factual
claim MUST be followed by a citation in the form (Source: <filename>).
If the excerpts don't cover the question, say so plainly and do not guess.

TODO F: Should this system prompt also explicitly instruct the model on
how to handle text that looks like an instruction embedded inside a
customer note? (See TODO C.) If you implemented injection defence,
make sure the system prompt actually reflects it — an unused import
doesn't count as a real defence.
"""

client = OpenAI()
embeddings = OpenAIEmbeddings(model=EMBED_MODEL)
vectorstore = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=PERSIST_DIR,
)

app = FastAPI(title="Solstice Insurance Claims Support Assistant")


@app.get("/")
def root():
    return {"message": "Solstice Claims Assistant is running. Try /ask?q=your+question"}


@app.get("/ask")
def ask(q: str, top_k: int = TOP_K):
    tracer = Tracer()

    # TODO G: PII redaction, incoming question. Same pattern as Meridian —
    # but ALSO think about whether this needs to run on the OUTGOING
    # answer too, given the sensitivity Compliance flagged. (Toolkit
    # hint: output_validation.py's no_leaked_pii check already does
    # this — are you actually calling validate_answer() before returning?)
    with tracer.stage("pii_redact_input"):
        redacted_question = q  # TODO: call redact_pii()

    # TODO H: Retrieval — implement per your TODO A decision.
    with tracer.stage("retrieval"):
        raw_results = []  # TODO: implement

    best_score = best_score_from_results(raw_results)
    level = confidence_level(best_score)

    # TODO I: Refusal guardrail — same pattern as every earlier lab.

    # TODO J: Reranking — implement per your TODO B decision.

    # TODO K: Injection scan + untrusted-data wrapping — implement per
    # your TODO C decision. This is the one place a shortcut here would
    # be a genuine, demonstrable gap against the client brief, not just
    # a style choice.

    # TODO L: Context assembly, LLM call, and OUTPUT VALIDATION
    # (toolkit/output_validation.py's validate_answer()) before
    # returning anything to the caller.

    # TODO M: Audit logging — capture everything, including whether
    # injection was flagged and whether output validation passed.

    return {
        "question": redacted_question,
        "confidence": level,
        # TODO N: complete the response shape.
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
