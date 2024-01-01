# response_generator.py
import os
import transformers
import logging

from transformers import AutoTokenizer, pipeline
import torch


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# model_name = "meta-llama/Llama-2-7b-chat-hf"
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# pipeline = transformers.pipeline(
#         "text-generation",
#         model=model_name,
#         # torch_dtype=torch.float16,
#         torch_dtype=torch.float32,
#         device_map="auto",
#     )
# logger.info("Model loaded successfully.")
# Load the model if it hasn't been loaded already
# if 'pipeline' not in globals():
#     # tokenizer = AutoTokenizer.from_pretrained(model_name)
#     pipeline = transformers.pipeline(
#         "text-generation",
#         model=model_name,
#         torch_dtype=torch.float32,
#         device_map="auto",
#     )
#     logger.info("Model loaded successfully.")


def generate_responses(statements, prompt, model_name="meta-llama/Llama-2-7b-chat-hf"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    pipeline_model = transformers.pipeline(
        "text-generation",
        model=model_name,
        torch_dtype=torch.float32,
        device_map="auto",
    )

    responses = []
    for statement in statements:
        full_input = f"{prompt} {statement}"
        logger.info(f"Generating response for input: {full_input}")
        sequences = pipeline_model(
            full_input,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=tokenizer.eos_token_id,
            max_length=200,
        )
        for seq in sequences:
            response = seq['generated_text'].strip()
            responses.append(response)
            logger.info(f"Generated response: {response}")

    return responses




    # with open(statements_file, 'r', encoding='utf-8') as file:
    #     statements = file.readlines()
    #
    # responses = []
    # for statement in statements:
    #     logger.info(f"Generating response for input: {statement.strip()}")
    #     sequences = pipeline(
    #         statement,
    #         do_sample=True,
    #         top_k=10,
    #         num_return_sequences=1,
    #         eos_token_id=tokenizer.eos_token_id,
    #         max_length=200,
    #     )
    #     for seq in sequences:
    #         response = seq['generated_text'].strip()
    #         responses.append(response)
    #         # responses.append(seq['generated_text'].strip())
    #         logger.info(f"Generated response: {response}")
    # return statements, responses
