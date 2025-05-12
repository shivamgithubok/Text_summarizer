import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def scrape_and_summarize(url):
    try:
        # Fetch webpage content
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse the webpage
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract text from paragraph tags
        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])
        
        # Summarize text using Sumy
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, 5)  # Extract 5 sentences
        
        return " ".join(str(sentence) for sentence in summary)
    
    except Exception as e:
        return str(e)

