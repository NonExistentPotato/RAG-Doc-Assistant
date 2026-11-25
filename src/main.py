from pypdf import PdfReader 

reader = PdfReader("./data/Software_Engineer_Switch_Resume_Template.pdf")

def extract_text_from_pdf(reader,pdf_content):
    for page_num,page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        extracted_page = {
            "page_num": page_num,
            "text": text if text is not None else "No extracteable text found !"
            #"text" : text
        }
        pdf_content.append(extracted_page)


def split_into_chunks(text, chunk_size):
    if text is None :
        return []
    if chunk_size < 1 :
        print("Non positive chunk size")
        raise ValueError("chunk_size must be positive")    

    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks


def main():
    print("MY FIRST RAG CAPSTONE!")
    print(len(reader.pages))
    pdf_content = []
    extract_text_from_pdf(reader, pdf_content)
    #print(pdf_content)

    chunk_size = 1000
    all_chunks = []

    # Split extracted content into chunks
    for record in pdf_content:
        chunks = split_into_chunks_word_boundary(record["text"], chunk_size)
        for chunk_index,chunk in enumerate(chunks):
            chunk_dict = {
                "page": record["page_num"],
                "chunk_index": chunk_index,
                "text": chunk
            }
            all_chunks.append(chunk_dict)
    
    print("Total chunks:", len(all_chunks))

    # Validate generated chunks
    for chunk in all_chunks:
        # Check each chunk is atmost chunk_size
        if len(chunk["text"]) > chunk_size:
            raise ValueError(f"text greater than chunk_size for chunk "f"{chunk['chunk_index']} page {chunk['page']}")

        print(len(chunk["text"]))

    # Verify chunks reproduce the original extracted content
    for record in pdf_content:
        page_num = record["page_num"]
        original_text = record["text"]

        page_chunks = []
        for chunk in all_chunks:
            if chunk["page"] == page_num:
                page_chunks.append(chunk["text"])

        reconstructed_text = "".join(page_chunks)

        if reconstructed_text != original_text:
            raise ValueError(f"Text mismatch on page {page_num}")

    print("All pages reconstructed successfully!")        

def split_into_chunks_word_boundary(text, chunk_size):
    print("split_into_chunks_word_boundary")

    if text is None :
        return []
    if chunk_size < 1 :
        print("Non positive chunk size")
        raise ValueError("chunk_size must be positive")
    
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end == len(text):
            chunks.append(text[start:end])
            break
        split_index = text.rfind(" ", start, end)
        if split_index <= start:
            split_index = end
        else:
            split_index += 1

        chunks.append(text[start:split_index])
        start = split_index
       
    return chunks


if __name__ == "__main__":
    main()
