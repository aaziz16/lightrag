




import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential

# Set up your Azure credentials and endpoint
endpoint = "https://eastus.api.cognitive.microsoft.com/"
key = "711a8a1fcf204210aea2ad04b5b1669e"
 
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

def extract_text_from_image_pdf(document_file_path, output_txt_path):  
    # Open the PDF file in binary mode
    with open(document_file_path, "rb") as document_file:
        document = document_file.read()  # Read the file in binary mode

        # Using the prebuilt-read model for OCR  
        poller = document_analysis_client.begin_analyze_document(
            model_id="prebuilt-read", document=document
        )
        result = poller.result()

        # Write extracted text to a .txt file  
        with open(output_txt_path, "w", encoding="utf-8") as txt_file:  
            for page in result.pages:  
                txt_file.write(f"---- Page {page.page_number} ----\n")  
                for line in page.lines:  
                    txt_file.write(f"{line.content}\n")

