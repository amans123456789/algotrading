import csv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
def write_to_csv(output_csv_file, statements, responses):
    with open(output_csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Input Text", "Generated Response"])

        for statement, response in zip(statements, responses):
            writer.writerow([statement.strip(), response])
            logger.info(f"Written to CSV: {statement.strip()}, {response}")

    logger.info(f"CSV file '{output_csv_file}' written successfully.")