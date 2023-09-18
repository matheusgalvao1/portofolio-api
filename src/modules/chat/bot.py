from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

load_dotenv('.env')
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

with open('cv.txt', 'r') as file:
    content = file.read()


template = f"""
You are a chatbot designed to answer questions about Matheus to potential employers, he created you to answer questions \
about his life and work. Here are some useful information about him: {content}
Chat History:
{{chat_history}}
Human: {{human_input}}
Chatbot:"""

prompt = PromptTemplate(
    input_variables=["chat_history", "human_input"], template=template
)
memory = ConversationBufferMemory(memory_key="chat_history")

llm_chain = LLMChain(
    llm=OpenAI(openai_api_key=OPENAI_API_KEY),
    prompt=prompt,
    verbose=True,
    memory=memory,
)

def answer(input):
    return llm_chain.predict(human_input=input)
