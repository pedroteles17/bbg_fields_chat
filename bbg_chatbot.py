#%%
import openai
import pickle
import pandas as pd

#%%
# Import data
metadata = pickle.load(open('data/field_metadata.pickle', 'rb'))

docs = pickle.load(open('data/field_documentation.pkl', 'rb'))

# %%
# Clean metadata 
all_fields = []
for field_group in metadata:
    for field in field_group['message']['element']['fieldResponse']:
        field_data = field['fieldData']
        field_info = field_data['fieldInfo']['fieldInfo']

        field_dict = {
            'id': field_data['id'],
            'mnemonic': field_info['mnemonic'],
            'description': field_info['description'],
            'data_type': field_info['datatype'],
            'category_name': field_info['categoryName'][0],
            'property': field_info['property'],
            #'overrides': field_info['overrides'],
            'ftype': field_info['ftype']
        }

        all_fields.append(field_dict)

all_fields_df = pd.DataFrame(all_fields)

# %%
# Clean documentation
all_docs = []
for field_group in docs:
    for field in field_group['message']['element']['fieldResponse']:
        field_data = field['fieldData']
        field_info = field_data['fieldInfo']['fieldInfo']

        field_dict = {
            'id': field_data['id'],
            'mnemonic': field_info['mnemonic'],
            'documentation': field_info['documentation']
        }

        all_docs.append(field_dict)

all_docs_df = pd.DataFrame(all_docs)

# %%
# Join documentation and metadata
all_data = all_fields_df\
    .merge(all_docs_df, on=['id', 'mnemonic'], how='left')\
    .drop(columns=['property'])

# %%
from langchain.llms import OpenAI
# %%
