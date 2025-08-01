#Extract legal entities such as parties, dates, obligations, monetary values, etc.
#pip install ibm-watson
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, KeywordsOptions

authenticator = IAMAuthenticator("_Tx2WKK4GC8B2VMd_CsP0cmQBY3593KPYn-7MM2KxPPd")
nlu = NaturalLanguageUnderstandingV1(
    version='2022-04-07',
    authenticator=authenticator
)
nlu.set_service_url("https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/766276be-3941-48ac-819c-2a986230c244")

response = nlu.analyze(
    text="IBM is a global technology company.",
    features=Features(keywords=KeywordsOptions())
).get_result()

print(response)
