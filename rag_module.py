import chromadb
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from llama_index import VectorStoreIndex
from llama_index.llms import ChatMessage, MessageRole
from llama_index.prompts import ChatPromptTemplate

class VectorDB:
    def __init__(self, path, collection_name):
        self.path = path
        self.collection_name = collection_name

    def initialize_index(self):
        vector_store = self.get_vector_store()

        storage_context = StorageContext.from_defaults(vector_store=vector_store)

        index = VectorStoreIndex.from_vector_store(
            vector_store, storage_context=storage_context
        )

        return index
    
    def get_vector_store(self):
        db = chromadb.PersistentClient(path=self.path)

        chroma_collection = db.get_or_create_collection(self.collection_name)

        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        return vector_store
    
class QueryEngine:
    SYSTEM_TEMPLATE = (
        "As an exceptional and invaluable question-and-answer system for Bloomberg data fields,"
        "your role is to provide accurate and relevant responses to inquiries based on the given" 
        "context. It is important to rely solely on the provided information and refrain from" 
        "offering answers based on external knowledge. If the context is insufficient, just say so."
        "Do not create new fields or answer with external knowledge. Your task is to suggest up to"
        "three valid bloomberg fields for each question based on the bloomberg fields presented"
        "in the context. You should include the mnemonic and the source of the fields." 
    )
    
    USER_TEMPLATE = (
        "Context information is below.\n"
        "---------------------\n"
        "{context_str}\n"
        "---------------------\n"
        "Given the context information and not prior knowledge, "
        "please answer the query. Do not create new fields"
        "or use information outside the context.\n"
        "Query: {query_str}\n"
        "Answer: "
    )

    def __init__(self, index, similarity_top_k):
        self.index = index
        self.similarity_top_k = similarity_top_k
    
    def initialize_query_engine(self):
        text_qa_template = self._get_question_answer_template()

        query_engine = self.index.as_query_engine(
            text_qa_template=text_qa_template, 
            similarity_top_k=self.similarity_top_k
        )

        return query_engine
    
    def _get_question_answer_template(self):
        chat_text_qa_msgs = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=self.SYSTEM_TEMPLATE,
            ),
            ChatMessage(
                role=MessageRole.USER,
                content=self.USER_TEMPLATE,
            ),
        ]
        return ChatPromptTemplate(chat_text_qa_msgs)