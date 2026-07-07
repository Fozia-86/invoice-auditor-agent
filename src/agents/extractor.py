import json
import os
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def extract_invoice_data(gcs_uri: str) -> str:
    """Extract structured invoice data from a GCS file using Gemini multimodal API.

    Args:
        gcs_uri: The Google Cloud Storage URI to the raw invoice image/PDF (gs://bucket/path/file).

    Returns:
        A JSON string containing the structured invoice data.
    """
    print(f"[Extractor Agent] Processing file from {gcs_uri}...")

    try:
        # Parse GCS URI
        if not gcs_uri.startswith("gs://"):
            raise ValueError(f"Invalid GCS URI format: {gcs_uri}. Must start with gs://")

        uri_parts = gcs_uri[5:].split("/", 1)
        bucket_name = uri_parts[0]
        blob_path = uri_parts[1] if len(uri_parts) > 1 else ""

        if not blob_path:
            raise ValueError(f"Invalid GCS URI: missing file path in {gcs_uri}")

        print(f"[Extractor Agent] Fetching {blob_path} from bucket {bucket_name}...")

        # Fetch file from GCS
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)

        # Download file content to memory
        file_bytes = blob.download_as_bytes()
        content_type = blob.content_type or "image/jpeg"

        print(f"[Extractor Agent] Downloaded {len(file_bytes)} bytes, type: {content_type}")
        print(f"[Extractor Agent] Invoking Gemini multimodal API...")

        # Initialize Vertex AI with project and location
        project = os.environ.get("GOOGLE_CLOUD_PROJECT")
        location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

        if not project:
            raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set")

        vertexai.init(project=project, location=location)

        # Create Gemini model for multimodal processing
        model = GenerativeModel('gemini-2.5-flash')

        # Construct extraction prompt
        extraction_prompt = """Analyze this invoice image and extract the following information in strict JSON format:

{
    "invoice_id": "the invoice or receipt number",
    "vendor": "the vendor or company name",
    "category": "hardware OR software OR travel OR general (choose the most appropriate)",
    "line_items": [
        {"description": "item description", "amount": numeric_amount_in_dollars}
    ],
    "total_amount_usd": total_numeric_amount_in_dollars
}

IMPORTANT: Return ONLY the raw JSON object with no markdown formatting, no code blocks, and no explanations. Just pure JSON."""

        # Generate content with multimodal input
        response = model.generate_content([
            extraction_prompt,
            Part.from_data(data=file_bytes, mime_type=content_type)
        ])

        # Extract text from response
        extracted_text = response.text.strip()

        # Remove markdown code blocks if Gemini added them
        if extracted_text.startswith("```"):
            lines = extracted_text.split("\n")
            # Remove first and last lines (```json and ```)
            extracted_text = "\n".join(lines[1:-1]).strip()

        print(f"[Extractor Agent] Gemini response: {extracted_text[:200]}...")

        # Parse and validate JSON
        extracted_data = json.loads(extracted_text)

        # Add source tracking
        extracted_data["gcs_source"] = gcs_uri

        print(f"[Extractor Agent] Successfully extracted invoice {extracted_data.get('invoice_id')} from {extracted_data.get('vendor')}")

        return json.dumps(extracted_data)

    except Exception as e:
        print(f"[Extractor Agent] ERROR: {str(e)}")
        # Return error response that won't break downstream processing
        error_response = {
            "invoice_id": "ERROR",
            "vendor": "EXTRACTION_FAILED",
            "category": "general",
            "line_items": [],
            "total_amount_usd": 0.0,
            "gcs_source": gcs_uri,
            "error": str(e)
        }
        return json.dumps(error_response)

extractor_agent = Agent(
    name="extractor_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction="""You are the Data Extractor Agent. Your job is to extract structured data 
    from raw invoices in GCS. When given an invoice URI, call the extract_invoice_data tool 
    and return the exact JSON.""",
    tools=[extract_invoice_data]
)
