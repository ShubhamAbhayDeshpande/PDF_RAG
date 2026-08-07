# Google API Trial

This repository is a small Python prototype for building a PDF-based retrieval workflow with Google Gemini. It currently focuses on three main ideas:

- Extracting text and images from PDF files
- Structuring the extracted content into JSON and document objects
- Experimenting with Gemini API integration and a simple chat-style interface

The project is still in an early stage and is best viewed as a learning/demo codebase for PDF parsing, chunking, and LLM integration.

## What this project does

The workflow is intended to look like this:

1. Read one or more PDF files from a folder
2. Extract text and embedded images from each page
3. Save the parsed output as JSON
4. Convert the JSON into document objects for chunking or later retrieval
5. Use Gemini for chat or question-answering over the extracted content

## Repository structure

- [APITestCode.py](APITestCode.py) — a simple Gemini API example that sends a prompt to the Google GenAI client.
- [app.py](app.py) — a basic Tkinter-based chat UI scaffold.
- [chunker.py](chunker.py) — converts parsed PDF JSON into LangChain-style document objects with metadata.
- [embedder.py](embedder.py) — intended for embedding generated chunks; currently empty.
- [llm_api.py](llm_api.py) — a small wrapper for Gemini client setup and API key loading.
- [pdf_extractor.py](pdf_extractor.py) — extracts text and images from PDFs and writes the results to JSON.
- [rag_chat.py](rag_chat.py) — intended for retrieval-augmented chat logic; currently empty.
- [retriever.py](retriever.py) — intended for similarity search/retrieval logic; currently empty.
- [vector_store.py](vector_store.py) — intended for vector database integration; currently empty.
- [requirements.txt](requirements.txt) — Python dependencies for the project.
- [pdfs/](pdfs) — place your source PDF files here.
- [jsondump/](jsondump) — stores the parsed output from the extractor.
- [extracted_images/](extracted_images) — stores images extracted from the PDFs.

## Setup

### 1. Prerequisites

Make sure you have Python 3.9+ installed.

### 2. Install dependencies

From the project root, run:

```bash
pip install -r requirements.txt
```

If you want to use the provided virtual environment in this workspace, activate it with:

```bash
PythonEnv\Scripts\activate
```

### 3. Configure your Gemini API key

Create a file named `.env` in the project root and add your key:

```env
GEMINI_API_KEY=your_api_key_here
```

## Usage

### Extract text and images from PDFs

Run:

```bash
python pdf_extractor.py
```

This will:

- scan all PDF files under the configured folder
- extract page text and images
- save a JSON structure to [jsondump/result.json](jsondump/result.json)
- export images to [extracted_images/](extracted_images)

### Create document objects from the parsed JSON

Run:

```bash
python chunker.py
```

This loads the generated JSON and builds a list of document objects with metadata such as:

- document name
- page number
- chunk ID
- image IDs and image paths

### Try the Gemini example

Run:

```bash
python APITestCode.py
```

This is a small test script to confirm that your Gemini connection works.

### Launch the simple UI

Run:

```bash
python app.py
```

This opens a basic Tkinter window for a chat-style interface.

## Current status

The repository is partially implemented. The core extraction logic is working, and the chunking logic is scaffolded. The following files are currently placeholders for the next stages of the project:

- [embedder.py](embedder.py)
- [retriever.py](retriever.py)
- [vector_store.py](vector_store.py)
- [rag_chat.py](rag_chat.py)

These files are intended to be completed for a full RAG pipeline that stores embeddings, retrieves relevant chunks, and answers questions over the PDF content.

## Dependencies

The project uses the following main packages:

- google-genai
- python-dotenv
- chromadb
- pymupdf
- pillow
- numpy
- tqdm

## Notes

- The parser currently expects PDF files to be available in the [pdfs/](pdfs) folder or in a path passed by the script logic.
- The output JSON and extracted images are written into the repository folders so they can be inspected easily.
- This repository is a good starting point for learning about PDF parsing, document chunking, and Gemini-based AI applications.

## Changelog (recent commits)

- 7d48b55: Made the final `chunker` file using `RecursiveCharacterTextSplitter.split_documents()` — the method now returns the chunks for the document objects created.
- 579e78e: Added `README.md` and made cosmetic corrections to `chunker.py`.
- 3ac1ca4: Started `chunk.py` implementation.
- 541845f: Initial commit.
