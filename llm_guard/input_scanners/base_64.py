from .base import Scanner
import base64

class BASE_64(Scanner):
    """
    A sentiment scanner based on the NLTK's SentimentIntensityAnalyzer. It is used to detect if a prompt
    has a sentiment score lower than the threshold, indicating a negative sentiment.
    """

    def __init__(self, threshold: float = -0.1):
        """
        Initializes Sentiment with a threshold and a chosen lexicon.

        Parameters:
           threshold (float): Threshold for the sentiment score (from -1 to 1). Default is -0.1.
           lexicon (str): Lexicon for the SentimentIntensityAnalyzer. Default is 'vader_lexicon'.

        Raises:
           None.
        """

        # nltk = lazy_load_dep("nltk")
        # nltk.download(lexicon)

        # sentiment = lazy_load_dep("nltk.sentiment", "nltk")
        # self._sentiment_analyzer = sentiment.SentimentIntensityAnalyzer()
        # self._threshold = threshold
        


    def scan(self, prompt: str) -> (str, bool, float):
        def isBase64():
            try:
                return base64.b64encode(base64.b64decode(prompt)) == prompt.encode('utf-8')
            except Exception:
                return False
        value=isBase64()
        score=0
        if value==True:
            prompt=base64.b64decode(prompt)
        
        
        return prompt.decode('utf-8'), value, score
