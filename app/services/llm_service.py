
## | Word           | Meaning                                              |
## | -------------- | ---------------------------------------------------- |
## | Conversational | Supports questions and answers across a conversation |
## | Retrieval      | Retrieves relevant information from your documents   |
## | Chain          | Connects multiple processing steps into a workflow   |
## ConversationalRetrievalChain connects document retrieval with conversational question answering.

# from langchain_classic.chains import ConversationalRetrievalChain
# from langchain_classic.memory import ConversationBufferMemory

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver

from config import Config

class LLMService:
    def __init__(self, vector_store):
        # Assumes vector_store.vector_store is your Chroma vector store.
        chroma = vector_store.vector_store

        @tool
        def search_documents(query: str) -> str:
            """Search the uploaded documents for information relevant to the question."""
            docs = chroma.similarity_search(query, k=4)
            if not docs:
                return "No relevant information was found in the documents."

            return "\n\n".join(doc.page_content for doc in docs)

        self.agent = create_agent(
            model=ChatOpenAI(
                model="gpt-4o-mini",
                temperature=0.7,
                api_key=Config.OPENAI_API_KEY,
            ),
            tools=[search_documents],
            system_prompt=(
                "Answer the user's questions using the uploaded documents. "
                "Use the search_documents tool when document information is needed. "
                "If the documents do not contain the answer, say so."
            ),
            checkpointer=InMemorySaver(),
        )

    def get_response(self, query, session_id="default"):
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": query}]},
            config={"configurable": {"thread_id": session_id}},
        )

        return result["messages"][-1].content