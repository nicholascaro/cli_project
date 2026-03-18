from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base

mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

@mcp.tool("read_doc")
def read_doc(doc_id: str) -> str:
    """Read the contents of a document."""
    return docs.get(doc_id, "Document not found.")

@mcp.tool("edit_doc")
def edit_doc(doc_id: str, new_content: str) -> str:
    """Edit the contents of a document."""
    if doc_id in docs:
        docs[doc_id] = new_content
        return "Document updated successfully."
    else:
        return "Document not found."

@mcp.resource("docs://documents", mime_type="application/json")
def list_docs() -> list[str]:
    """Return a list of all document IDs."""
    return list(docs.keys())

@mcp.resource("docs://documents/{doc_id}", mime_type="text/plain")
def get_doc(doc_id: str) -> str:
    """Return the contents of a specific document."""
    return docs.get(doc_id, "Document not found.")

@mcp.prompt("format")
def rewrite_doc(doc_id: str) -> list[base.Message]:
    prompt = f"""
    Rewrite the following document in markdown format:

    Document ID: {doc_id}
    Content: {docs.get(doc_id, "Document not found.")}

    As markdown, you can use headings, bullet points, and other formatting to make the document easier to read.
    """
    return [base.UserMessage(content=prompt)]


# TODO: Write a prompt to summarize a doc
@mcp.prompt("summarize_doc")
def summarize_doc(doc_id: str) -> list[base.Message]:
    prompt = f"""
    Summarize the following document in 2-3 sentences:

    Document ID: {doc_id}
    """
    return [base.UserMessage(content=prompt)]


if __name__ == "__main__":
    mcp.run(transport="stdio")
