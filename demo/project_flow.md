| Component            | Company analogy         | Responsibility                                                  |
| -------------------- | ----------------------- | --------------------------------------------------------------- |
| `main.py`            | Receptionist            | Receives requests and directs them to the appropriate component |
| `config.py`          | Company policy document | Stores configuration and settings                               |
| `llm_service.py`     | Subject-matter expert   | Communicates with the LLM and generates answers                 |
| `vector_store.py`    | Knowledge librarian     | Stores document chunks and finds relevant information           |
| `storage_service.py` | Records department      | Manages uploaded documents and their storage                    |
| `index.html`         | Customer-facing counter | Displays the user interface                                     |
| `style.css`          | Interior designer       | Controls the visual appearance                                  |
| `requirements.txt`   | Equipment inventory     | Lists the Python packages the application needs                 |

## A. requirements.txt — Dependencies

This file contains the Python libraries required by your application.

For example:
```bash
flask==2.3.3
langchain==0.0.267
openai==0.28.0
chromadb==0.4.0
pypdf==3.9.0
```
These libraries provide capabilities such as:

Building the web application.
Communicating with an LLM.
Extracting text from PDFs.
Storing and retrieving document embeddings.

Important: Listing a package in this file doesn't automatically make your application use it. You must import and call its functionality in your Python code.

## B. app/__init__.py — Package initialization
This file identifies app as a Python package.

It can also initialize shared application components.

For example, you could leave it empty initially:
```bash
app/__init__.py
```
Python can then import modules using paths such as:
```bash
from app.services import llm_service
```
You don't need to put your entire application inside this file.

For your project, keep the main application logic in main.py and the relevant service logic in the services folder.

## C. app/config.py — Configuration management

This file stores settings that multiple parts of your application may need.

For example:
```bash
# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

UPLOAD_FOLDER = "uploads"

CHROMA_DB_PATH = "chroma_db"
```
Let's understand these variables.

OPENAI_API_KEY

Allows your application to access the configured OpenAI API credential.
```bash
UPLOAD_FOLDER
``````
Specifies where uploaded documents will be stored if you choose local file storage.
```bash
CHROMA_DB_PATH
```
Specifies where persistent ChromaDB data can be stored.

These are examples, not mandatory values. You should configure the paths according to your actual application.

### Why separate configuration from the main code?

Suppose you want to change your vector database's storage location.

Without a configuration file, you might have hardcoded the location in several Python files.

With config.py, you can centralize the setting and import it wherever necessary.

This makes the project easier to maintain.

### Security tip: 
Store secrets in environment variables or a protected .env file, not directly in source code. Add .env to .gitignore.

## 3. The models folder — Your knowledge storage layer

Your structure contains:

models/
├── __init__.py
└── vector_store.py

In this architecture, vector_store.py is responsible for interacting with your vector database.

Let's understand why you need it.

Imagine a user uploads a 100-page employee handbook.

You don't want to send all 100 pages to the LLM every time the user asks a question.

Instead, you can:

1. Extract the text.
2. Split it into smaller chunks.
3Convert the chunks into embeddings.
S tore the embeddings in a vector database.
4. Retrieve only the chunks relevant to a question.

This is a central part of a Retrieval-Augmented Generation (RAG) system.

What is an embedding?

An embedding is a numerical representation of text that captures aspects of its meaning.

For example:

Document chunk:
"Employees can work remotely two days per week."

An embedding model might convert this into a vector resembling:

[0.21, -0.42, 0.76, 0.13, ...]

These numbers are illustrative.

When the user asks:

How many days can employees work from home?

The system converts the question into an embedding and searches for semantically relevant document chunks.

What does vector_store.py do?

Its responsibilities may include:

1. Initializing the ChromaDB client.
2. Creating or accessing a collection.
3. Storing document chunks and their embeddings.
4. Searching for relevant chunks.
5. Returning the retrieved text to the LLM service.

Conceptually, it might expose functions like:
```bash
def add_documents(chunks):
    """Store document chunks in the vector database."""
    pass


def search_documents(question, k=3):
    """Retrieve the most relevant chunks."""
    pass
```
These are illustrative function signatures. They don't perform the operations until you implement them.

Why put this code in a separate file?

Because you don't want main.py to contain all the database implementation.

Instead, main.py can simply request:
```bash
relevant_chunks = search_documents(question)
```
The vector-store module handles the details of the search.

One architectural note: models is being used here for the vector-storage layer. In other projects, a models folder may contain data models or database entities instead. Your naming convention is acceptable as long as you use it consistently.

### 4. The services folder — The business logic

Your structure contains:

services/
├── __init__.py
├── llm_service.py
└── storage_service.py

These two service files have different responsibilities.

A. llm_service.py — Communicating with the LLM

This module handles the language-model part of the application.

Suppose the user asks:

What is the company's work-from-home policy?

Your system retrieves relevant text from the vector database.

For example:
```bash
Retrieved context:
"Employees are permitted to work remotely two days per week,
subject to manager approval."
```

The LLM receives both the question and the retrieved context.

A prompt might look like this:
```bash
You are a document assistant.

Answer the question using only the provided context.

Context:
Employees are permitted to work remotely two days per week,
subject to manager approval.

Question:
What is the company's work-from-home policy?

Answer:
```
The model might generate:
```bash
Employees can work remotely two days per week,
subject to manager approval.
```
What should llm_service.py handle?

Typically:

1. Accept the user's question.
2. Receive the relevant document chunks.
3. Construct the prompt.
4. Call the configured LLM.
5. Return the generated answer.

Its interface might look like:
```bash
def generate_answer(question, context):
    """Generate an answer using the question and retrieved context."""
    pass
```
The implementation will depend on whether you use OpenAI, Amazon Bedrock, or another model provider.

Important distinction: The LLM does not automatically know the contents of the user's uploaded documents. Your RAG pipeline supplies relevant document context to the model.

### B. storage_service.py — Managing uploaded documents

This service manages the document files themselves.

For example, the user uploads:
```bash
employee_handbook.pdf
```
The storage service could save the file to:
```bash
uploads/employee_handbook.pdf
```
Its responsibilities might include:

1. Saving uploaded files.
2. Validating file types.
3. Managing filenames.
4. Returning the stored file path.
5. Providing access to documents when they need processing.

You might define a function such as:
```bash
def save_document(uploaded_file):
    """Validate and save an uploaded document."""
    pass
```
The exact implementation depends on how you want to store documents.

For an initial local project, you could use a directory on your computer.

For a cloud-based application, you might use Amazon S3, in which case Boto3 could be useful.

Why separate document storage from vector storage?

This is an important architectural distinction.

| Storage component | What it stores                                       |
| ----------------- | ---------------------------------------------------- |
| Document storage  | Original PDF, DOCX, or other uploaded file           |
| Vector storage    | Document chunks, embeddings, and associated metadata |


For example:
```bash
Original document:
uploads/employee_handbook.pdf

Vector database:
Chunk 1 → embedding + text
Chunk 2 → embedding + text
Chunk 3 → embedding + text
```
The original document and the vector database serve different purposes.

### 5. The templates folder — What the user sees

Your structure contains:

templates/
└── index.html

Flask uses the templates directory by convention to locate HTML templates.

The index.html file defines the structure of your webpage.

For example, your interface might contain:

A heading: Document Intelligence System.
A file-upload control.
A question input box.
A Submit button.
An answer display area.

A simplified example:
```bash
<!DOCTYPE html>
<html>
<head>
    <title>Document Intelligence System</title>
    <link
        rel="stylesheet"
        href="{{ url_for('static', filename='style.css') }}"
    >
</head>

<body>
    <h1>Document Intelligence System</h1>

    <form method="POST" enctype="multipart/form-data">
        <label>Upload your document:</label>
        <input type="file" name="document">

        <br><br>

        <label>Ask a question:</label>
        <input type="text" name="question">

        <button type="submit">Submit</button>
    </form>
</body>
</html>
```
This is only a basic interface example. It doesn't yet implement document upload or question answering.

Notice this line:
```bash
{{ url_for('static', filename='style.css') }}
```
Flask generates the URL for the CSS file in your static directory.

Also, this form uses multipart/form-data, which is needed when submitting uploaded files through a standard HTML form.

### 6. The static folder — Styling your webpage

Your structure contains:

static/
└── style.css

This file controls the appearance of the webpage.

For example:
```bash
body {
    font-family: Arial, sans-serif;
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
}

h1 {
    text-align: center;
}

input,
button {
    padding: 10px;
    margin-top: 10px;
}
```
This CSS:

1. Sets the font.
2. Controls the page width and spacing.
3. Centers the heading.
4. Adds spacing around inputs and buttons.

The HTML defines the structure; the CSS defines its appearance.

Flask can serve the file from the static directory automatically.

### There are two related workflows:

Document ingestion: The user uploads a document, and the application prepares it for retrieval.
Question answering: The user asks a question, and the application retrieves relevant information and generates an answer.

These workflows are connected, but they don't necessarily happen at the same time.

### Workflow A: Uploading and processing a document

Imagine the user uploads employee_handbook.pdf.

### Step 1: User uploads the PDF

The user selects the file in index.html and clicks Upload.

### Step 2: Flask receives the request

main.py receives the submitted file through a Flask route.

### Step 3: Save the original document

main.py calls storage_service.py.

### Step 4: Extract the text

The application uses PyPDF or Unstructured to extract the document contents.

### Step 5: Split the text into chunks

LangChain can split the extracted text into smaller sections.

### Step 6: Generate embeddings

An embedding model converts each chunk into a vector.

### Step 7: Store the chunks and embeddings

The application calls vector_store.py, which stores the data in ChromaDB.

At this point, the document is ready for retrieval.

### Workflow B: Asking a question

Now imagine the user asks:

What is the company's annual leave policy?

The flow changes slightly.

### Step 1: The user submits a question

The user enters the question into index.html.

### Step 2: Flask receives the question

main.py receives the submitted form data.

### Step 3: Retrieve relevant document chunks

main.py calls vector_store.py.

The vector store searches the document embeddings and retrieves relevant content.

### Step 4: Send the context and question to the LLM

main.py calls llm_service.py, passing the question and retrieved text.

### Step 5: Return the answer to the user

Flask renders the answer in the HTML template.

### Important components to understand:

1. storage_service.py: Where and how is the original document saved?
2. vector_store.py: How is the document converted into searchable information?
3. llm_service.py: How are retrieved chunks used to generate the final answer?

### Development order

| Order | File                        | What you should implement                                       |
| ----- | --------------------------- | --------------------------------------------------------------- |
| 1     | `config.py`                 | Load environment variables and configure storage paths          |
| 2     | `storage_service.py`        | Save and validate uploaded documents                            |
| 3     | Document-processing service | Extract text and split it into chunks                           |
| 4     | `vector_store.py`           | Generate/store embeddings and retrieve relevant chunks          |
| 5     | `llm_service.py`            | Construct prompts and generate answers                          |
| 6     | `index.html`                | Create the upload and question-answering interface              |
| 7     | `style.css`                 | Style the interface                                             |
| 8     | `main.py`                   | Connect the components through Flask routes                     |
| 9     | `requirements.txt`          | Confirm that the required dependencies are installed            |
| 10    | Testing                     | Test document uploads, retrieval quality, and answer generation |

document_service.py would handle:

1. PDF or other document parsing.
2. Text extraction.
3. Chunking.
4. 
Preparing documents for embedding and storage.

That keeps document ingestion separate from LLM generation and file storage.