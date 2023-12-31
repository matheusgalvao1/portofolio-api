from langchain.llms import OpenAI
from langchain import LLMChain
from langchain.prompts.prompt import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
import os
import lorem
import asyncio

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_myinfo():
    with open("cv.txt", "r") as file:
        return file.read()


def get_template(myinfo):
    return f"""
    You are a chatbot designed to answer questions about Matheus to potential employers, you never say you are Matheus galvao yourself, he created you to answer questions \
    about his life and work, you are not Matheus, you are just his Chatbot, don't answer off topic questions. Here are some useful information about him: {myinfo}
    Chat History:
    {{chat_history}}
    Human: {{human_input}}
    Chatbot:"""


# Create a dictionary to store chat instances
chat_instances = {}


def start_new_chat(chat_id):
    if chat_id in chat_instances:
        raise KeyError(f"Chat ID aready exists.")

    myinfo = get_myinfo()
    template = get_template(myinfo)
    prompt = PromptTemplate(
        input_variables=["chat_history", "human_input"], template=template
    )

    # Create a new instance of memory
    new_memory = ConversationBufferMemory(memory_key="chat_history")

    # Create a new instance of LLMChain
    new_llm_chain = LLMChain(
        llm=ChatOpenAI(openai_api_key=OPENAI_API_KEY, model_name="gpt-3.5-turbo"),
        prompt=prompt,
        verbose=True,
        memory=new_memory,
    )

    # Store the new instances in the dictionary
    chat_instances[chat_id] = {"memory": new_memory, "llm_chain": new_llm_chain}

    # Schedule the destruction in 3 hours to free resources
    asyncio.create_task(finish_chat_timer(chat_id))


def finish_chat(chat_id):
    # Remove the instance from the dictionary to release resources
    if chat_id in chat_instances:
        del chat_instances[chat_id]
        return True
    else:
        return False


# Async function to destroy an instance
async def finish_chat_timer(chat_id):
    await asyncio.sleep(10800)  # wait for 3 hours
    if chat_id in chat_instances:
        del chat_instances[chat_id]
        print(f"Destroyed instance with chat_id {chat_id}")
    else:
        print(f"Instance with chat_id {chat_id} does not exist.")


# Can only get answer from a chat if it is in the instances dictionary, therefore started and not finished
def get_answer(input, chat_id, testMode=False):
    # Retrieve the specific memory and llm_chain for the given chat_id
    if chat_id not in chat_instances:
        raise KeyError(f"Chat ID {chat_id} not found. Please start a new chat.")

    # Get memory and llm_chain based on chat_id
    memory = chat_instances[chat_id]["memory"]
    llm_chain = chat_instances[chat_id]["llm_chain"]

    if testMode:
        # Generate a dummy response using lorem module
        aux = lorem.paragraph()

        # Add the messages to the memory
        memory.chat_memory.add_user_message(input)
        memory.chat_memory.add_ai_message(aux)

        return aux
    else:
        # Get the response from the llm_chain
        return llm_chain.predict(human_input=input)


def exist_instance(chat_id):
    return chat_id in chat_instances


"""
def get_history(chat_id):
    messages = chat_instances[chat_id]["memory"].chat_memory.messages
    return messages
"""
