from transformers import AutoTokenizer
import transformers
import torch
import logging
from response_generator import generate_responses
from csv_writer import write_to_csv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_prompt(prompt_file):
    with open(prompt_file, 'r', encoding='utf-8') as file:
        return file.read().strip()
def main():
    statements_file = "statement_txt/output_headings_and_text.txt"  # Replace with the path to your text file
    prompt_file = "prompt/llama_prompt.txt"
    output_csv_file = "output_responses.csv"

    prompt = read_prompt(prompt_file)
    logger.info(f"Using prompt: {prompt}")

    logger.info("Reading statements from file...")

    statements = []

    with open(statements_file, 'r', encoding='utf-8') as file:
        statements = [line.strip() for line in file.readlines()]

    logger.info(f"Total statements to process: {len(statements)}")

    responses = generate_responses(statements, prompt)


    logger.info("Writing input statements and generated responses to CSV file...")
    # Write input statements and generated responses to a CSV file
    write_to_csv(output_csv_file, statements, responses)

    logger.info("Process completed successfully.")

if __name__ == "__main__":
    main()

# model = "meta-llama/Llama-2-7b-chat-hf"
#
# tokenizer = AutoTokenizer.from_pretrained(model)
#
#
#
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     pipeline = transformers.pipeline(
#         "text-generation",
#         model=model,
#         # torch_dtype=torch.float16,
#         torch_dtype=torch.float32,
#         device_map="auto",
#     )
#     sequences = pipeline(
#         'I liked "Breaking Bad" and "Band of Brothers". Do you have any recommendations of other shows I might like?\n',
#         do_sample=True,
#         top_k=10,
#         num_return_sequences=1,
#         eos_token_id=tokenizer.eos_token_id,
#         max_length=200,
#     )
#     for seq in sequences:
#         print(f"Result: {seq['generated_text']}")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
