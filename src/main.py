import os

from langchain_community.llms import ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

ollama_base_url = os.getenv("OLLAMA_BASE_URL")

llm = ollama.Ollama(
    base_url=ollama_base_url,
    model='tinyllama:chat',
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

llm.invoke("Can you please japanese. Write a message in japanese")

print('\n')

# docker exec --workdir /src -it python-demo /bin/bash
# docker exec --workdir /src -it python-demo python3 main.py
# docker exec --workdir /python-demo -it python-demo python3 main.py