from qdrant_client import QdrantClient
from docling.chunking import HybridChunker
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter

qdrant_client = QdrantClient(
    url="https://59004e01-863e-4d09-802b-24ddbcefe01b.eu-west-2-0.aws.cloud.qdrant.io:6333", 
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.kEwGurfbzPq0Na9D1shINCrnqTjd5Q2DpT3EiKBzWeA",
)

collectionName = "recipe"
converter = DocumentConverter(
    allowed_formats=[InputFormat.PDF,
                    InputFormat.DOCX, 
                    InputFormat.XLSX,

                    InputFormat.PPTX,
                      ],
)
qdrant_client.set_model("sentence-transformers/all-MiniLM-L6-v2")
qdrant_client.set_sparse_model("Qdrant/bm25")


def upload_file(COLLECTION_NAME ,file_path):
    
    result = converter.convert(file_path)
    documents, metadatas = [], []

    for chunk in HybridChunker().chunk(result.document):
            documents.append(chunk.text)
            metadatas.append(chunk.meta.export_json_dict())

    qdrant_client.add(
        collection_name=COLLECTION_NAME,
        documents=documents,
        metadata=metadatas,
        batch_size=80,
    )  

upload_file(collectionName,"F:/fastapi_recipe/sample.pdf")
print("Uploaded to Qdrant")