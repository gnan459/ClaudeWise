from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

authenticator = IAMAuthenticator("_Tx2WKK4GC8B2VMd_CsP0cmQBY3593KPYn-7MM2KxPPd")
nlu = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)
nlu.set_service_url("https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/766276be-3941-48ac-819c-2a986230c244")

def extract_entities(text: str) -> dict:
    """
    Extracts legal entities (keywords) from the given text using IBM Watson NLU.
    Returns a dictionary with 'keywords' as a list of keyword strings.
    """
    response = nlu.analyze(
        text=text,
        features=Features(keywords=KeywordsOptions())
    ).get_result()
    keywords = response.get("keywords", [])
    keyword_texts = [kw["text"] for kw in keywords]
    return {"keywords": keyword_texts}