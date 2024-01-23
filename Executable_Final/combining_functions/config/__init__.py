import os
import yaml

config_path = os.environ.get("CONFIG_PATH", "config/eval.yaml")

with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)