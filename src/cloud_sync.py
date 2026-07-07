import json
import os
from google.cloud import firestore
from google.cloud import bigquery

def log_to_firestore(transaction_id: str, payload: dict) -> dict:
    """Log the transaction state to Google Cloud Firestore.

    Args:
        transaction_id: The unique transaction ID to use as document ID.
        payload: The transaction data to store.

    Returns:
        A dictionary with the Firestore sync status.
    """
    print(f"[Firestore Sync] Logging transaction {transaction_id} to 'transactions' collection...")

    try:
        # Initialize Firestore client
        db = firestore.Client()

        # Get collection name from environment or use default
        collection_name = os.environ.get("FIRESTORE_COLLECTION", "transactions")

        # Write document to Firestore
        doc_ref = db.collection(collection_name).document(transaction_id)
        doc_ref.set(payload)

        print(f"[Firestore Sync] Successfully wrote document {transaction_id} to {collection_name}")

        return {
            "collection": collection_name,
            "document_id": transaction_id,
            "status": "SAVED"
        }

    except Exception as e:
        print(f"[Firestore Sync] ERROR: {str(e)}")
        return {
            "collection": "transactions",
            "document_id": transaction_id,
            "status": "FAILED",
            "error": str(e)
        }
    
def stream_to_bigquery(payload: dict) -> dict:
    """Stream the final ledger to Google BigQuery for analytics.

    Args:
        payload: The complete transaction ledger data to stream.

    Returns:
        A dictionary with the BigQuery streaming status.
    """
    print("[BigQuery Stream] Streaming ledger block to 'finance_audit.ledger_stream'...")

    try:
        # Initialize BigQuery client
        client = bigquery.Client()

        # Get dataset and table from environment or use defaults
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        dataset_id = os.environ.get("BIGQUERY_DATASET", "finance_audit")
        table_id = os.environ.get("BIGQUERY_TABLE", "ledger_stream")

        # Construct full table ID
        if project_id:
            table_full_id = f"{project_id}.{dataset_id}.{table_id}"
        else:
            table_full_id = f"{dataset_id}.{table_id}"

        print(f"[BigQuery Stream] Streaming to table: {table_full_id}")

        # Insert row into BigQuery
        # The payload should be a single dict, wrap it in a list for insert_rows_json
        rows_to_insert = [payload]
        errors = client.insert_rows_json(table_full_id, rows_to_insert)

        if errors:
            print(f"[BigQuery Stream] Encountered errors: {errors}")
            return {
                "dataset": dataset_id,
                "table": table_id,
                "status": "FAILED",
                "errors": errors
            }

        print(f"[BigQuery Stream] Successfully streamed 1 row to {table_full_id}")

        return {
            "dataset": dataset_id,
            "table": table_id,
            "status": "SUCCESS"
        }

    except Exception as e:
        print(f"[BigQuery Stream] ERROR: {str(e)}")
        return {
            "dataset": "finance_audit",
            "table": "ledger_stream",
            "status": "FAILED",
            "error": str(e)
        }
