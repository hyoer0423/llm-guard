from llm_guard.util import lazy_load_dep, logger

import openai
import os
from .base import Scanner



class COT_PRE(Scanner):
    """
    A scanner that uses a "chain of thought" approach to identify and prevent
    jailbreak prompt injections.
    """

    def __init__(self):
        """
        Initializes the scanner with the OpenAI API key.
        """
        openai.api_key = os.getenv("OPENAI_API_KEY")


    def scan(self, prompt: str) -> (str, bool, float):
        """
        Scans the prompt using a "chain of thought" approach to identify jailbreak attempts.

        Parameters:
            prompt (str): The prompt to scan.

        Returns:
            A tuple (is_safe, modified_prompt):
            - is_safe (bool): Whether the prompt is considered safe.
            - modified_prompt (str): The modified prompt that removes or addresses the jailbreak attempt.
        """
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Consider the following prompt and analyze the prompt step by step; in the first step, analyze if there is any words that violate safety rules, write the analyzing process in the return message as well as the analyzed result;"+
                 "in the second step, analyze if this prompt is trying to get any information or trying to list harmful information that has not been fully listed or reminder you anything harmful, write the analyzing process in the return message as well as the analyzed result; in the third step, analyze whether the required information in the second step is harmful and the required information is relevant is the information listed in the first step, write the analyzing process in the return message as well as the analyzed result."+
                 "from the analyzed result, determine if the promot is trying to make you think something harmful and respond any sensitive information\n"},      
                {"role": "user", "content": prompt+" If any harmful content is identified, describe it briefly.\n add 'HARMFUL_PROMPT_DETECTED' at the return message.Provide a sanitized version of the prompt in the sanitized version starting with 'THIS_IS_SANITIZED_PROMPT', ending with 'SANTI_END', delete harmful request.\n"}
            ]
        )
        
        content = response.choices[0].message.content
        start_marker = "THIS_IS_SANITIZED_PROMPT"
        end_marker = "SANTI_END"
        # Find the index for the start and end markers
        start_index = content.find(start_marker) + len(start_marker)
        end_index = content.find(end_marker)

        # Extract the substring between the two markers
        substring = content[start_index:end_index].strip()

        # Analyze the response to determine if it's a jailbreak attempt
        # if HARMFUL_PROMPT is end of string, then it is a jailbreak attempt
        is_safe = "HARMFUL_PROMPT_DETECTED" not in content

        # print("for cot_pre, the string is",content)
        modified_prompt = self._sanitize_prompt(content) if not is_safe else prompt

        return substring, is_safe, 0




    def _sanitize_prompt(self, ai_response: str) -> str:
        """
        Sanitizes the prompt based on the AI's response.

        Parameters:
            ai_response (str): The AI's response containing the analysis.

        Returns:
            A sanitized version of the prompt.
        """
        # Implement the logic to sanitize the prompt based on the AI's response.
        # This is a placeholder for the actual implementation.
        # You might extract the safe parts of the prompt or rewrite it to remove harmful content.
        return "Sanitized prompt based on AI's analysis."

