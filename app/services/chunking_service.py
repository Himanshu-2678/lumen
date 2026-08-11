from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ". ", " ", ""]
)

def chunk_pages(pages: list[dict]) -> list[dict]:

    chunks = []
    global_index = 0

    for page in pages:
        page_chunks = text_splitter.split_text(page["text"])

        for chunk in page_chunks:
            chunks.append({
                "page_number": page["page_number"],
                "chunk_index": global_index,
                "text": chunk
            })

            global_index += 1

    return chunks