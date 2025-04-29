import os.path
import re
from enum import Enum
from string import Template
from typing import Any

import config
from config import positive_list, negative_list
from llm_endpoint import ask_llm


class LLmDecision(Enum):
    Negative = 0,
    Positive = 1,
    Undecided = -1,
    Error = -2,

def decide_if_is_sublet(listing_content: dict[str, int]) -> LLmDecision:
    return decide_on_file_content(listing_content, config.decide_if_is_sublet_prompt_filename)

def substitute_prompt_template(prompt_template_string: str, listing_content: dict[str, int]) -> str:
    prompt_template = Template(prompt_template_string)
    prompt = prompt_template.substitute(filecontent = listing_content)
    return prompt

def call_llm_from_prompt_template(listing_content: dict[str, int], prompt_filename: str) -> (bool, str):
    prompt_file_path = os.path.join(config.prompt_directory, prompt_filename)

    with open(prompt_file_path) as file:
        prompt_template_string = file.read()

        prompt = substitute_prompt_template(prompt_template_string, listing_content)
        (success, answer) = ask_llm(prompt)

    print(f"DEBUG: llm answer decide_on_file_content for promptfile {prompt_filename}:\n{answer}")
    return success, answer

def decide_on_file_content(class_file_content: str, prompt_filename: str) -> LLmDecision:
    success, answer = call_llm_from_prompt_template(class_file_content, prompt_filename)
    return get_decision_from_llm_answer(answer) if success else LLmDecision.Error

def get_decision_from_llm_answer(answer:str) -> LLmDecision:
    is_positive_answer = any([positive_string in answer for positive_string in positive_list])
    is_negative_answer = any([negative_string in answer for negative_string in negative_list])

    if is_positive_answer and (not is_negative_answer):
        return LLmDecision.Positive

    if is_negative_answer and (not is_positive_answer):
        return LLmDecision.Negative

    return LLmDecision.Undecided
