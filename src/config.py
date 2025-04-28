# Create a ConfigParser object
import configparser
import json
import os
from pathlib import Path


def parse_escaped(escaped_str: str):
    if (escaped_str.startswith("'") and escaped_str.endswith("'")):
        return escaped_str[1:-1]
    return escaped_str

def parse_path(raw_path: str):
    return raw_path.replace("\\\\", "\\")

config = configparser.ConfigParser()

# Read the configuration file
config.read(os.path.join(Path(__file__).parent, 'config.ini'))

### LLM configuration
llm_section_head = "Large Language Model"
# token for llm
llm_token = config.get(llm_section_head, "llm_token")
# the name of the llm model, must be available at the given base url
llm_model = config.get(llm_section_head, "llm_model")
llm_base_url = config.get(llm_section_head, "llm_base_url")
# some reasonable name for the application visible to llm (no further criteria for it)
llm_x_user_agent = config.get(llm_section_head, "llm_x_user_agent")

### Prompt parser config
prompt_parser_section_head = "Prompt Parser"
# absolute path of the directory containing all prompts
prompt_directory = config.get(prompt_parser_section_head, "prompt_directory")
# list that contains answers of the llm that will be considered positive
positive_list = json.loads(config.get(prompt_parser_section_head, "positive_list"))
# list that contains answers of the llm that will be considered negative
negative_list = json.loads(config.get(prompt_parser_section_head, "negative_list"))
