#%%
import pickle
import pandas as pd
import re

#%%
# Import data
fields_metadata = pickle.load(open('field_metadata.pickle', 'rb'))

fields_documentation = pickle.load(open('field_documentation.pkl', 'rb'))

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

        # Replace newlines with spaces and remove extra spaces
        field_documentation = field_info['documentation'].replace('\n', ' ')
        field_documentation = re.sub(r'\s+', ' ', field_documentation)

        field_dict = {
            'source': field_data['id'],
            'mnemonic': field_info['mnemonic'],
            'documentation': field_documentation
        }

        all_fields_documentation.append(field_dict)

all_fields_documentation_df = pd.DataFrame(all_fields_documentation)

# %%
# Join documentation and metadata
all_fields_data = all_fields_metadata_df\
    .merge(all_fields_documentation_df, on=['source', 'mnemonic'], how='left')\
    .drop(columns=['property'])\
    .dropna(subset=['documentation'])

all_fields_data.to_parquet('clean_fields_docs.parquet', index=False)

#%%