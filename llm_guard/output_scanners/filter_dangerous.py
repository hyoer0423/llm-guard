
from .base import Scanner
import openai

class Filter(Scanner):
    """
    A class for scanning if the model output includes code in specific programming languages.

    This class uses the transformers library to detect code snippets in the output of the language model.
    It can be configured to allow or deny specific programming languages.
    """

    def __init__(
        self,
        threshold: float = 0.5,
        
    ):
        """
        Initializes an instance of the Code class.

        Parameters:
            threshold (float): The threshold for the model output to be considered valid. Default is 0.5.
        
        """
        openai.api_key = ''
        

        

    def scan(self, prompt: str, output: str) -> (str, bool, float):
        score=0
        completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a answer checker that return the same answer if it is safe and proper or rewrite a better answer. You will be given the original injected prompt and answer. You need to check whether the answer does not contain the harmful part and can follow the prompt."},
        {"role": "user", "content": "Here is the answer:<"+output+">"+"\n"+"Here is the prompt:"+"<"+prompt+">"}
        ])
        new_answer=completion.choices[0].message.content
        return new_answer,True,0