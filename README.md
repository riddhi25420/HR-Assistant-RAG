# HR Knowledge Assistant- Local RAG System using Oracle AI Vector Search

## Project Overview

- The HR_KNOWLEDGE_ASSISTANT is an application designed to help organizations manage HR policy documents and enable employees to quickly find answers to HR related queries using Retrieval Augmented Generation(RAG).

- To ensure complete privacy of confidential company documents,all processing is performed locally on the user's computer. No third-party cloud services or APIs are used.

- Application enables employees to add/delete or view HR policy documents and perform AI searches on them.

## Project Statement

Organizations maintain a large number of HR policy documents covering areas such as leave,attendance,payroll,medical insurance,travel,information security,data privacy,work-from-home policies and employee conduct.

Finding an answer to a specific employee question manually requires searching through multiple documents and pages.

The HR Knowledge Assistant addresses this problem by creating a local Retrieval-Augmented Generation (RAG) system that retrieves relevant information from HR policy documents and uses a locally running Large Language Model to generate grounded answers.

The system was designed with data privacy as a core requirement. HR documents,embeddings,database records,retrieval operations and LLM inference remain on the local machine without requiring external AI APIs.

## Key Features

- AI-powered HR chatbot
- Oracle APEX web interface
- FastAPI backend
- Oracle AI Database 26ai
- Oracle VECTOR datatype
- Automatic PDF upload
- PDF text extraction
- Intelligent document chunking
- SentenceTransformer embeddings
- Oracle AI Vector Search
- Hybrid Search(Vector + Keyword Search)
- Local Large Language Model using Ollama
- Chat session history
- Source document citations
- Environment-based credential configuration
- Modular backend architecture

# Technologies Used

| Technology | Purpose |
|------------|---------|
| Oracle APEX | Frontend |
| FastAPI | Backend REST API |
| Oracle AI Database 26ai | Database |
| Oracle VECTOR | Embedding storage |
| Oracle AI Vector Search | Semantic retrieval |
| Sentence Transformers (all-MiniLM-L6-v2) | Embedding generation |
| Ollama | Local LLM runtime |
| Qwen 2.5:3b | Large Language Model |
| Python | Backend development |
| PyPDF | PDF text extraction |
| SHA-256 | Duplicate document detection |

## Project Architecture

```
                           Oracle APEX
                                │
                                │ REST API
                                ▼
                        FastAPI Backend
                                │
        ┌──────────────┬───────────────┬──────────────┐
        │              │               │              │
        ▼              ▼               ▼              ▼
 Upload Service   Search Service   RAG Service   Ollama Service
        │              │               │              │
        ▼              ▼               ▼              ▼
 Document DB   Oracle AI Vector   Prompt Builder   Qwen LLM
        │
        ▼
Oracle Database 26ai
        │
        ├── HR Documents
        ├── Document Chunks
        └── VECTOR Embeddings
```

## Project Structure

```text
HR_KNOWLEDGE_ASSISTANT/
│
├── backend/
│   ├── api/                              # FastAPI API endpoints
│   │   ├── chat.py
│   │   ├── chunk.py
│   │   ├── documents.py
│   │   ├── embedding.py
│   │   ├── health.py
│   │   ├── history.py
│   │   ├── index.py
│   │   ├── pdf.py
│   │   ├── rag.py
│   │   ├── routes.py
│   │   ├── search.py
│   │   ├── session.py
│   │   └── upload.py
│   │
│   ├── database/                         # Oracle database connection and schema documentation
│   │   ├── oracle.py
│   │   └── describe_tables.md
│   │
│   ├── models/                           # Pydantic request and response models
│   │   ├── api_response.py
│   │   ├── chat_models.py
│   │   ├── request_models.py
│   │   └── response_models.py
│   │
│   ├── services/                         # Core application and RAG services
│   │   ├── chat_memory.py
│   │   ├── chat_service.py
│   │   ├── chunk_service.py
│   │   ├── document_service.py
│   │   ├── embedding_service.py
│   │   ├── hybrid_search.py
│   │   ├── index_service.py
│   │   ├── ingestion_service.py
│   │   ├── keyword_search.py
│   │   ├── ollama_service.py
│   │   ├── pdf_service.py
│   │   ├── prompt_service.py
│   │   ├── rag_service.py
│   │   ├── search_service.py
│   │   ├── session_service.py
│   │   └── upload_service.py
│   │
│   ├── utils/                            # Logging and file utilities
│   │   ├── logger.py
│   │   └── file_utils.py
│   │
│   ├── app.py                            # FastAPI application entry point
│   ├── config.py                         # Application configuration
│   └── .env.example                      # Example environment configuration
│
├── apex/
│   └── HR_Assistant_APEX.sql             # Oracle APEX application export
│
├── hr_documents/                         # HR policy PDF documents
│
├── screenshots/                          # Screenshots of the Oracle APEX frontend
│   ├── User sign in page.png
│   ├── Home page.png
│   ├── Documents page.png
│   ├── Upload document page.png
│   ├── Chatbot assistant page with new chat.png
│   ├── Asking question from chatbot in new chat.png
│   └── Displaying a previous chat.png
│
├── README.md                             # Project documentation
├── .gitignore                            # Files excluded from Git
└── requirements.txt                      # Python dependencies 

```
## Project Workflow

### Upload PDF

```
Receive PDF

        │
        ▼
        
Generate SHA256 hash

        │
        ▼
        
Duplicate Detection

        │
        ▼
        
Store metadata

        │
        ▼
        
Extract text

        │
        ▼
        
Chunk document

        │
        ▼
        
Generate embeddings

        │
        ▼
        
Store vectors
```

### CHAT 

```
Employee question

        │
        ▼
        
Generate query embedding

        │
        ▼
        
Oracle AI Vector Search

        │
        ▼
        
Keyword search

        │
        ▼
        
Hybrid ranking

        │
        ▼
        
Top relevant chunks

        │
        ▼
        
Prompt construction

        │
        ▼
        
Qwen 2.5:3b (Ollama)

        │
        ▼
        
Generated answer

        │
        ▼
        
Store chat history
```

## RAG Pipeline

### Document Upload

- Upload PDF
- Extract text using PyPDF
- Calculate SHA256 hash
- Detect duplicate documents
- Store metadata

### Chunking

- Recursive character text splitter
- Chunk Size:500 characters
- Chunk Overlap:100 characters

### Embedding Generation

- SentenceTransformer
- Model:`all-MiniLM-L6-v2`
- Embedding Dimension:384

### Retrieval

- Oracle AI Vector Search
- Keyword Search
- Hybrid Ranking

### Response Generation

Relevant chunks are passed to the locally running Qwen 2.5:3b model through Ollama to generate grounded answers.

## Backend Architecture

The backend follows a modular architecture.
```
Client(Oracle APEX)

         │
         ▼
         
API Layer
(Receives HTTP requests)

         │
         ▼

Service Layer
(Contains business logic)

         │
         ▼

Database Layer
(Communicates with Oracle Database)

         │
         ▼

AI Layer
(Retrieves HR documents and generates answers using a local language model)
```

## Database Design

The application uses Oracle Database 26ai to store:
- HR document metadata
- Original HR documents
- Extracted document chunks
- Vector embeddings
- Chat sessions
- Chat messages
- Chat history

The application uses the following Oracle tables:
- HR_DOCUMENTS
- DOCUMENT_CHUNKS
- CHAT_SESSIONS
- CHAT_MESSAGES
- CHAT_HISTORY

For more information about tables see backend/database/describe_tables.md

Document embeddings are stored using Oracle VECTOR datatype.

The database is designed to support Retrieval-Augmented Generation (RAG) and Oracle AI Vector Search.

## REST API

| Method | Endpoint | Purpose |
|---------|----------|---------|
| GET | /health | check health |
| POST | /chat | ask AI assistant |
| GET | /documents | list documents |
| DELETE | /documents/{document_id} | delete document |
| POST | /upload | upload HR policy PDF |
| POST | /upload-apex | upload document from apex |
| GET | /extract | extract |
| GET | /chunk-test | test |
| GET | /embedding-test | embedding test |
| POST | /index | build index |
| POST | /search | search |
| GET | /history/{session_id} | retrieve chat history |
| GET | /session | session |
| POST | /session | create session |
| DELETE | /session/{session_id} | delete session |
| POST | /rename | rename chat |

## Oracle AI Features Used

- Oracle AI Database 26ai
- Oracle VECTOR datatype
- VECTOR(384, FLOAT32)
- VECTOR_DISTANCE()
- Native Vector Search
- Oracle SQL joins with vector retrieval

## Frontend – Oracle APEX

The user interface of the HR Knowledge Assistant is developed using Oracle APEX.

Oracle APEX provides the web interface through which employees interact with the RAG backend.

### Home Page

The Home page acts as the application's central navigation dashboard.

It provides cards for accessing:

- Chatbot Assistant
- HR Documents
- Upload Documents

### HR Documents

The HR Documents page allows users to browse the HR policy documents currently available in the knowledge base.

### Upload Documents

The Upload Documents page allows new HR policy PDFs to be added to the knowledge base.

Uploaded documents are sent to the FastAPI backend where the ingestion pipeline performs:

PDF Upload  
→ SHA256 Hashing  
→ Duplicate Detection  
→ Text Extraction  
→ Chunking  
→ Embedding Generation  
→ Oracle Vector Storage

### Chatbot Assistant

The Chatbot Assistant provides a conversational interface for asking questions about HR policies.

Questions are sent to the FastAPI backend, processed through the RAG pipeline, and answered using the locally running Qwen model.

The interface also supports chat session history and conversation management.

## Development Progress

The project was developed incrementally, with each stage building a component of the final RAG pipeline.

### Phase 1 – Environment Setup

The initial development environment was prepared with:

- Python development environment
- Oracle AI Database
- Oracle APEX
- Oracle REST Data Services (ORDS)
- FastAPI
- Ollama
- Sentence Transformers

A Python virtual environment was created to isolate project dependencies.

### Phase 2 – Oracle Database Design

The Oracle database schema was created for storing HR documents,extracted document chunks,vector embeddings,chat sessions,chat messages and chat history.

The major database tables are:

- `HR_DOCUMENTS`
- `DOCUMENT_CHUNKS`
- `CHAT_SESSIONS`
- `CHAT_MESSAGES`
- `CHAT_HISTORY`

Oracle's native `VECTOR(384, FLOAT32)` datatype is used to store document embeddings.

### Phase 3 – Document Management

A document management pipeline was implemented to support:

- PDF upload
- Document metadata storage
- File path management
- Page count extraction
- Document status management

### Phase 4 – Duplicate Document Detection

SHA256 hashing was introduced to identify duplicate files.

When a document is uploaded,its SHA-256 hash is calculated and compared against hashes of existing documents before ingestion.

This prevents duplicate documents from unnecessarily entering the knowledge base.

### Phase 5 – PDF Text Extraction

PDF text extraction was implemented using PyPDF.

Text is extracted page by page so that retrieved information can retain its relationship with the original document and page.

### Phase 6 – Intelligent Document Chunking

Extracted text is divided into smaller chunks before embedding.

The implemented configuration uses:

- Chunk size:500 characters
- Chunk overlap:100 characters

Chunk overlap helps preserve context when information spans chunk boundaries.

### Phase 7 – Embedding Generation

Semantic embeddings are generated using:

`all-MiniLM-L6-v2`

Each document chunk is converted into a 384-dimensional embedding vector.

These embeddings are stored directly inside Oracle Database using the native VECTOR datatype.

### Phase 8 – Oracle AI Vector Search

Semantic retrieval was implemented using Oracle AI Vector Search.

When an employee submits a question:

1. The question is converted into an embedding.
2. Oracle compares the question vector with stored document vectors.
3. Cosine vector distance is calculated.
4. The most semantically relevant chunks are retrieved.

### Phase 9 – Hybrid Search

Vector similarity alone was not used as the final retrieval mechanism.

A hybrid retrieval strategy was implemented by combining:

- Semantic vector similarity
- Keyword matching
- Document title matching
- Important phrase matching

The ranking score is calculated using:

`Final Score = 0.65 × Vector Similarity + 0.35 × Keyword Score`

This improves retrieval quality by combining semantic similarity with exact keyword matching.

The highest-ranked chunks are selected as context for answer generation.

### Phase 10 – Local LLM Integration

Ollama was integrated as the local LLM runtime.

The final application uses:

`Qwen 2.5:3b`

The retrieved HR policy chunks are supplied to the model as context so that responses are generated using information from the organization's HR documents.

### Phase 11 – RAG Pipeline Integration

The individual components were integrated into the complete Retrieval-Augmented Generation pipeline:

Employee Question  
→ Query Embedding  
→ Vector Search  
→ Keyword Search  
→ Hybrid Ranking  
→ Relevant Document Chunks  
→ Prompt Construction  
→ Qwen 2.5:3b
→ Grounded Answer

### Phase 12 – Chat Session Management

Chat session functionality was implemented to support:

- Creating conversations
- Maintaining chat history
- Retrieving previous messages
- Renaming conversations
- Deleting conversations

### Phase 13 – FastAPI REST API

REST endpoints were developed using FastAPI to expose backend functionality to the frontend.

The API provides operations for:

- Check health
- Chat
- Document upload
- Document listing
- Document deletion
- Search
- Indexing
- Chat history
- Session management
- Rename chat

### Phase 14 – Oracle APEX Frontend

The frontend was developed using Oracle APEX.

The application includes:

- Home page
- HR Documents page
- Upload Documents page
- Chatbot Assistant page

Oracle APEX communicates with the FastAPI backend through REST API requests.

### Phase 15 – Retrieval Testing and Evaluation

The retrieval pipeline was evaluated using a test set of 100 HR-policy questions with expected source documents.

The observed result for that evaluation was:

| Metric | Result |
|---|---|
| Test Questions | 100 |
| Top-1 Document Retrieval Accuracy | 95% |
| Top-3 Document Retrieval Accuracy | 99% |


### Evaluation Meaning

Top-1 accuracy measures whether the expected HR document was ranked as the first retrieval result.

Top-3 accuracy measures whether the expected document appeared among the first three retrieved results.

The results demonstrate that the hybrid retrieval strategy was highly effective on the project's evaluation dataset.

> Note: These results measure document retrieval performance on the project's test dataset. They do not represent universal LLM answer accuracy.

## Privacy and Security

The application was designed for environments containing confidential HR information.

The architecture therefore prioritises local processing.

### Privacy Measures

- HR documents remain on the local system.
- Embeddings are generated locally.
- Embeddings are stored in Oracle Database.
- Vector similarity search is performed inside Oracle.
- LLM inference is performed locally through Ollama.
- No external AI API is required for answer generation.
- Database credentials are stored using environment variables.
- `.env` is excluded from version control.

### Credential Management

Sensitive credentials should never be committed to the repository.

The repository should contain:

`.env.example`

instead of:

`.env`

Users configure their own credentials locally after cloning the project.

## Installation and Setup

### Prerequisites

The following software must be installed locally:

- Python
- Oracle AI Database 26ai
- Oracle APEX 26.1
- Oracle REST Data Services (ORDS)
- Ollama
- Git

The application uses the following local AI models:

- Embedding model: `all-MiniLM-L6-v2`
- LLM: `qwen2.5:3b`

### Clone Repository

```bash
git clone <repository-url>
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Environment

Windows

```bash
.venv\Scripts\activate
```

Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

See requirements.txt

```bash
pip install -r requirements.txt
```

### Configure Environment

Create `.env`

```
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=1521
DB_SERVICE=FREEPDB1
OLLAMA_MODEL=qwen2.5:3b
```

### Start Backend

```bash
uvicorn backend.app:app --reload
```

### Oracle APEX

Import

```
apex/HR_Assistant_APEX.sql
```

into Oracle APEX

## Future Enhancements

- User authentication
- Role based access control
- OCR support for scanned PDFs
- Response streaming
- Citation highlighting
- Analytics dashboard
- Multi-document comparison

## Author

**Riddhi Aggarwal**

B.Tech Computer Science and Engineering
Indraprastha Institute of Information Technology Delhi (IIIT Delhi)

NTPC Limited
