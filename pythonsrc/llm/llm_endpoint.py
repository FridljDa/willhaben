import openai
from openai import UnprocessableEntityError

import config

openai.base_url = config.llm_base_url
openai.api_key = config.llm_token  # what is the api_key?
openai.default_headers = {"x-user-agent": config.llm_x_user_agent}


def ask_llm(message: str) -> (bool, str):
  print("asking llm single question\n=======")
  print(f"user:{message}")
  success, answer = get_llm_answer_for_messages(
      [{"role": "user", "content": message}])
  print(f"assistant:{answer}")
  return success, answer


def get_llm_answer_for_messages(messages: [dict]) -> (bool, str):
  try:
    response_raw = openai.chat.completions.create(
        model=config.llm_model,
        messages=messages,
    )
  except UnprocessableEntityError as e:
    print(e)
    return False, ""

  return True, response_raw.choices[0].message.content


class Dialog:
  messages = []

  def write_to_llm(self, message: str) -> (bool, str):
    if len(self.messages) == 0:
      print("starting new dialog\n===========")

    self.messages.append({
      "role": "user",
      "content": message
    })
    print(f"user:\n{message}")

    success, answer = get_llm_answer_for_messages(self.messages)

    if success:
      self.messages.append({
        "role": "assistant",
        "content": answer})
      print(f"assistant:\n{answer}")
    else:
      print("Failed to answer")

    return success, answer
