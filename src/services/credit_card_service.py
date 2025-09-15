from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from src.utils.Config import Config

def analyze_credit_card(file_url):

    credential = AzureKeyCredential(Config.SUBSCRIPTION_KEY)

    document_Client = DocumentIntelligenceClient(endpoint=Config.ENDPOINT, credential=credential)

    poller = document_Client.begin_analyze_document(
    "prebuilt-id-card",
    AnalyzeDocumentRequest(url_source=file_url)
)
    card_info = poller.result()


    result = card_info.result()

    for document in result.documents:
        fields = document.fields if hasattr(document, "fields") else {}

        return {
            "card_number": fields.get("CardNumber").value if fields.get("CardNumber") else None,
            "card_holder_name": fields.get("CardHolderName").value if fields.get("CardHolderName") else None,
            "expiry_date": fields.get("ExpiryDate").value if fields.get("ExpiryDate") else None,
            "brand": fields.get("Brand").value if fields.get("Brand") else None
        }
        
    return result