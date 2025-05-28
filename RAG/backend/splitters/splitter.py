from langchain.text_splitter import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain.schema import Document

def split_chunks(documents, chunk_size=1000, chunk_overlap=200):
    headers_to_split_on = [
        ("#", "Heading1"),
        ("##", "Heading2"),
        ("###", "Heading3"),
    ]
    md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    char_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n## ", "\n### ", "\n#### ", "\n", " ", ""],
        add_start_index=True,
    )

    all_chunks = []
    for doc in documents:
        # Split by Markdown headers
        md_chunks = md_splitter.split_text(doc.page_content)
        for md_chunk in md_chunks:
            # Then split by size
            char_chunks = char_splitter.split_text(md_chunk.page_content)
            for i, chunk_text in enumerate(char_chunks):
                metadata = dict(md_chunk.metadata)
                metadata["chunk_index_in_doc"] = i
                all_chunks.append(Document(page_content=chunk_text, metadata=metadata))
    print(f"Split {len(documents)} documents into {len(all_chunks)} chunks.")
    return all_chunks

if __name__ == "__main__":
    from ingestion import load_markdown_chunks
    docs = load_markdown_chunks()
    chunks = split_chunks(docs)
    print(f"Number of loaded chunks: {len(chunks)}")
    if chunks:
        print("Example chunk metadata:", chunks[0].metadata)
