"""Vertex AI RAG Retrieval tool for querying Google Drive documents."""

import logging

from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

from app.config.settings import settings

logger = logging.getLogger(__name__)

vertex_ai_rag_retrieval_tool = VertexAiRagRetrieval(
    name="retrieve_drive_documents",
    description=(
        "Use this tool to retrieve information from Google Drive documents. "
        "Searches across vectorized documents in the RAG corpus."
    ),
    rag_resources=[
        rag.RagResource(
            rag_corpus=settings.RAG_CORPUS_ID,
        )
    ],
    similarity_top_k=10,
    vector_distance_threshold=0.6,
)
