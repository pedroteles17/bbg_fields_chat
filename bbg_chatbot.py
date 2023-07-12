#%%
import pandas as pd

from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# %%
# Join documentation and metadata
all_fields_data = pd.read_excel('data/clean_fields_data.xlsx')

#%%
# Load data using LangChain
loader = DataFrameLoader(all_fields_data, page_content_column="documentation")

documents = loader.load()

del all_fields_data

# %%
# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1000,
    chunk_overlap  = 200,
    length_function = len,
    add_start_index = False,
)

docs = text_splitter.split_documents(documents)

# %%
# Create embeddings using OpenAI and FAISS
embeddings = OpenAIEmbeddings()

#db = FAISS.from_documents(docs, embeddings)

db.save_local("faiss_index")

#%%
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma

# create the open-source embedding function
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# load it into Chroma
chroma_db = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")
chroma_db.persist()
# %%
