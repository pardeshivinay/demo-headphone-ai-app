from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent

from rag.ingest import load as load_vectorstore
from tools.mcp_tools import get_tools


SYSTEM_PROMPT = """You are a helpful headphone shopping assistant for an Indian e-commerce store.

You help users find the best headphones within their budget, compare products, add items to cart, check stock, and apply discounts.

You have access to a product catalogue via search, and tools to:
- Add products to cart
- Apply discount codes
- Check stock availability

When recommending products:
- Always mention price in ₹
- Mention key specs: battery, noise cancellation, connectivity, rating
- Be conversational and helpful
- If the user says "the first one" or "the second one", refer back to what you previously listed

Available discount codes (share only when asked): SAVE10, BUDGET20, FIRST15

Keep responses concise and friendly."""


def build_agent(api_key: str):
    llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key, temperature=0.3)
    vectorstore = load_vectorstore(api_key)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    @tool
    def search_headphones(query: str) -> str:
        """Search the headphone catalogue for products matching a query. Use this for any product recommendations or lookups."""
        docs = retriever.invoke(query)
        if not docs:
            return "No products found matching your query."
        results = []
        for i, doc in enumerate(docs, 1):
            results.append(f"{i}. {doc.page_content}")
        return "\n\n".join(results)

    all_tools = [search_headphones] + get_tools()

    agent = create_react_agent(
        model=llm,
        tools=all_tools,
        prompt=SYSTEM_PROMPT,
    )
    return agent


def run_agent(agent, user_message: str, chat_history: list) -> tuple[str, list]:
    """Run the agent and return response + updated history."""
    # Build LangChain message history
    lc_messages = []
    for msg in chat_history:
        if msg["role"] == "user":
            lc_messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            lc_messages.append(AIMessage(content=msg["content"]))

    lc_messages.append(HumanMessage(content=user_message))

    result = agent.invoke({"messages": lc_messages})

    # Extract last AI message from the response
    response = ""
    for msg in reversed(result["messages"]):
        if isinstance(msg, AIMessage) and msg.content:
            response = msg.content
            break

    chat_history.append({"role": "user", "content": user_message})
    chat_history.append({"role": "assistant", "content": response})
    return response, chat_history
