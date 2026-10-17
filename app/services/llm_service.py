from langchain.chat_models import ChatOpenAI
# ChatOpenAI is a LangChain integration that allows you to communicate with OpenAI chat models.
from langchain.chains import ConversationalRetrievalChain
## | Word           | Meaning                                              |
## | -------------- | ---------------------------------------------------- |
## | Conversational | Supports questions and answers across a conversation |
## | Retrieval      | Retrieves relevant information from your documents   |
## | Chain          | Connects multiple processing steps into a workflow   |
## ConversationalRetrievalChain connects document retrieval with conversational question answering.

from langchain.memory import ConversationBufferMemory
from app.config import Config

class LLMService:
    def __init__(self, vector_store):
        self.llm = ChatOpenAI(
            temperature = 0.7,
            model_name = "gpt-3.5-turbo",
            openai_api_key = Config.OPENAPI_API_KEY
        )
        self.memory = ConversationBufferMemory(
            memory_key = "chat_history",
            return_messages = True
        )
## Conversation memory - Stores previous conversation exchanges, helps interpret follow up questions
## Vector database - Stores document chunks and their embeddings, helps find relevant document info
        self.chain = ConversationalRetrievalChain.from_llm(
            llm = self.llm,
            retriever = vector_store.vectorstore.as_retriever(),
            memory=self.memory
        )
    def get_response(self, query):
        try:
            response = self.chain({"question":query})
            return response['answer']
        except Exception as e:
            print(f"Error getting LLM response : {e}")
            return "I encountered an error processing your request"
