from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

import lorem

load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

with open("cv.txt", "r") as file:
    myinfo = file.read()


template = f"""
You are a chatbot designed to answer questions about Matheus to potential employers, he created you to answer questions \
about his life and work, you are not Matheus, you are just his Chatbot, don't answer off topic questions. Here are some useful information about him: {myinfo}
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


def start_new_chat():
    # Should start a new chat instance
    # Upload it to mongo
    # Get the chat id
    # Return the chat id
    return 1


def get_answer(input, testMode):
    # Should also have the chat id so at each new message it inserts in that chat in Mongo
    if testMode:
        aux = lorem.paragraph()
        memory.chat_memory.add_user_message(input)
        memory.chat_memory.add_ai_message(aux)
        return aux
    else:
        return llm_chain.predict(human_input=input)


def get_history():
    # Should also have the chat id to retrieve messages from mongo
    return memory.chat_memory.messages
