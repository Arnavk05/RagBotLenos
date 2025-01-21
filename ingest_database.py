from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_chroma import Chroma
from uuid import uuid4
from langchain_openai.embeddings import OpenAIEmbeddings


# import the .env file
from dotenv import load_dotenv
load_dotenv()
import os
print(os.path.exists("lenosdata.pdf"))
# configuration
DATA_PATH = r"data"
CHROMA_PATH = r"chroma_db"

# initiate the embeddings model
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-large")

# initiate the vector store
vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings_model,
    persist_directory=CHROMA_PATH,
)

# loading the PDF document
loader = PyPDFDirectoryLoader(DATA_PATH)

raw_documents = loader.load()
if not raw_documents:
    raise ValueError("Failed to load PDF documents. Ensure the file path is correct and accessible.")

# splitting the document
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False,
)

# creating the chunks
chunks = text_splitter.split_documents(raw_documents)
# Filter out empty chunks
chunks = [chunk for chunk in chunks if chunk.page_content.strip()]
# Validate chunks
max_tokens = 8191
chunks = [chunk for chunk in chunks if len(chunk.page_content) <= max_tokens]

# Generate embeddings
embeddings_model = OpenAIEmbeddings(model="text-embedding-ada-002")

# creating unique ID's
uuids = [str(uuid4()) for _ in range(len(chunks))]

# adding chunks to vector store
vector_store.add_documents(documents=chunks, ids=uuids)

