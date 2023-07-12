#%%
#import os

#os.environ["OPENAI_API_KEY"] = "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"

#from dotenv import load_dotenv
#load_dotenv()

#%%
import pickle
import pandas as pd

from langchain.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

#%%
# Import data
fields_metadata = pickle.load(open('data/field_metadata.pickle', 'rb'))

fields_documentation = pickle.load(open('data/field_documentation.pkl', 'rb'))

# %%
# Clean metadata 
all_fields_metadata = []
for field_group in fields_metadata:
    for field in field_group['message']['element']['fieldResponse']:
        field_data = field['fieldData']
        field_info = field_data['fieldInfo']['fieldInfo']

        field_dict = {
            'source': field_data['id'],
            'mnemonic': field_info['mnemonic'],
            'description': field_info['description'],
            'data_type': field_info['datatype'],
            'category_name': field_info['categoryName'][0],
            'property': field_info['property'],
            #'overrides': field_info['overrides'],
            'ftype': field_info['ftype']
        }

        all_fields_metadata.append(field_dict)

all_fields_metadata_df = pd.DataFrame(all_fields_metadata)

# %%
# Clean documentation
all_fields_documentation = []
for field_group in fields_documentation:
    for field in field_group['message']['element']['fieldResponse']:
        field_data = field['fieldData']
        field_info = field_data['fieldInfo']['fieldInfo']

        field_dict = {
            'source': field_data['id'],
            'mnemonic': field_info['mnemonic'],
            'documentation': field_info['documentation']
        }

        all_fields_documentation.append(field_dict)

all_fields_documentation_df = pd.DataFrame(all_fields_documentation)

# %%
# Join documentation and metadata
all_fields_data = all_fields_metadata_df\
    .merge(all_fields_documentation_df, on=['source', 'mnemonic'], how='left')\
    .drop(columns=['property'])

#%%
# Load data using LangChain
loader = DataFrameLoader(all_fields_data, page_content_column="documentation")

documents = loader.load()

# %%
# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size = 100,
    chunk_overlap  = 2,
    length_function = len,
    add_start_index = True,
)

docs = text_splitter.split_documents(documents)

# %%
# Create embeddings using OpenAI and FAISS
embeddings = OpenAIEmbeddings()

db = FAISS.from_documents(docs, embeddings)

#%%
