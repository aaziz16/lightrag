
'''

# Developed by Abdul Aziz
#Contains main functions for LightRAG
# Date: 10/25/2024



'''



import os
import asyncio
import shutil
import logging
import numpy as np
import aiohttp
from lightrag import LightRAG, QueryParam
from lightrag.utils import EmbeddingFunc
from prompts import st1_to_st3_prompt, stp4_prompt, submittal_prompt,submittal_prompt2,submittal_prompt3
from prompts import stp4_prompt  # Ensure this is correctly imported
import time
from prompts import submittal_st1_to_st3_prompt,submittal_stp4_prompt,comparison
# Configure logging
logging.basicConfig(level=logging.INFO)


# Function to set up working directory
# def setup_working_directory(directory):
#     if os.path.exists(directory):
#         shutil.rmtree(directory)
#     os.mkdir(directory)

import shutil
import os
import time
import logging

def setup_working_directory(directory):
    # Check if the directory exists
    if os.path.exists(directory):
        log_file = os.path.join(directory, "lightrag.log")

        # Attempt to close and remove any file handlers associated with the log file
        logging.shutdown()  # Gracefully shut down all logging handlers

        # If the file is still being accessed, retry deletion with delay
        retries = 3
        for attempt in range(retries):
            try:
                shutil.rmtree(directory)
                break
            except PermissionError as e:
                if attempt < retries - 1:
                    time.sleep(1)  # Wait for 1 second before retrying
                else:
                    print(f"Could not delete the directory {directory}. The file may be locked: {e}")
                    raise e  # Raise the error if the final attempt fails

    # Recreate the directory
    os.makedirs(directory, exist_ok=True)



# LLM model function (dynamically taking config)
async def llm_model_func(prompt, model_config, system_prompt=None, history_messages=[], **kwargs) -> str:
    headers = {
        "Content-Type": "application/json",
        "api-key": model_config['api_key'],
    }
    endpoint = f"{model_config['endpoint']}openai/deployments/{model_config['deployment']}/chat/completions?api-version={model_config['api_version']}"

    messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
    messages += history_messages + [{"role": "user", "content": prompt}]

    payload = {
        "messages": messages,
        "temperature": kwargs.get("temperature", 0),
        "top_p": kwargs.get("top_p", 1),
        "n": kwargs.get("n", 1),
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, json=payload) as response:
            if response.status != 200:
                raise ValueError(f"Request failed with status {response.status}: {await response.text()}")
            result = await response.json()
            return result["choices"][0]["message"]["content"]

# Embedding function (dynamically taking config)
async def embedding_func(texts: list[str], model_config) -> np.ndarray:
    headers = {
        "Content-Type": "application/json",
        "api-key": model_config['api_key'],
    }
    endpoint = f"{model_config['endpoint']}openai/deployments/{model_config['embedding_deployment']}/embeddings?api-version={model_config['embedding_api_version']}"

    payload = {"input": texts}

    async with aiohttp.ClientSession() as session:
        async with session.post(endpoint, headers=headers, json=payload) as response:
            if response.status != 200:
                raise ValueError(f"Request failed with status {response.status}: {await response.text()}")
            result = await response.json()
            embeddings = [item["embedding"] for item in result["data"]]
            return np.array(embeddings)

# Test the functions (optional testing method)
async def test_funcs(model_config):
    llm_result = await llm_model_func("How are you?", model_config)
    print("LLM Model Result: ", llm_result)

    embedding_result = await embedding_func(["How are you?"], model_config)
    print("Embedding Result Shape: ", embedding_result.shape)

# Query setup and execution
async def execute_query(rag_instance, query_text, mode="hybrid"):
    # Use the asynchronous 'aquery' method instead of 'query' to avoid loop issues
    result = await rag_instance.aquery(query_text, param=QueryParam(mode=mode))
    print(f"Query Result ({mode.capitalize()}):\n", result)
    return result

# Initialize the RAG pipeline



def initialize_rag(working_dir, embedding_dimension, llm_func, embedding_func, model_config, chunk_token_size=750):
    return LightRAG(
        working_dir=working_dir,
        chunk_token_size=chunk_token_size,  
        llm_model_func=lambda *args, **kwargs: llm_func(*args, model_config, **kwargs),
        embedding_func=EmbeddingFunc(
            embedding_dim=embedding_dimension,
            max_token_size=8192,
            func=lambda *args, **kwargs: embedding_func(*args, model_config, **kwargs)
        ),
    )

