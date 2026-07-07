#!/usr/bin/env python3
"""
Direct deployment script for the Invoice Auditor Agent to Vertex AI Reasoning Engine.
This bypasses the Agents CLI and uses the Vertex AI Python SDK directly.
"""

import os
import sys

# Set environment variables from .env file manually
env_file = ".env"
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key, value)

import vertexai
from vertexai.preview import reasoning_engines

def deploy_agent():
    """Deploy the agent to Vertex AI Reasoning Engine."""

    # Get configuration from environment
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

    if not project_id:
        print("ERROR: GOOGLE_CLOUD_PROJECT environment variable not set")
        sys.exit(1)

    print(f"🚀 Deploying Invoice Auditor Agent to Vertex AI")
    print(f"   Project: {project_id}")
    print(f"   Location: {location}")
    print()

    # Initialize Vertex AI
    vertexai.init(project=project_id, location=location)

    try:
        # Import the agent runtime app
        print("📦 Loading agent application...")
        from src.agent_runtime_app import agent_runtime

        # Deploy the agent as a Reasoning Engine
        print("🔧 Creating Reasoning Engine deployment...")

        reasoning_engine = reasoning_engines.ReasoningEngine.create(
            agent_runtime,
            requirements=[
                "google-adk[gcp]>=2.0.0",
                "opentelemetry-instrumentation-google-genai>=0.1.0",
                "gcsfs>=2024.11.0",
                "google-cloud-logging>=3.12.0",
                "google-cloud-aiplatform[evaluation,agent-engines]>=1.156.0",
                "google-cloud-storage",
                "google-cloud-firestore",
                "google-cloud-bigquery",
                "python-dotenv",
                "google-generativeai",
            ],
            display_name="invoice-auditor-agent",
            description="Smart Invoice Auditor & Autonomous Settlement Agent - Production Deployment",
            extra_packages=[],
        )

        print()
        print("✅ Deployment successful!")
        print(f"   Resource Name: {reasoning_engine.resource_name}")
        print(f"   Display Name: {reasoning_engine.display_name}")
        print()
        print("🎯 Next steps:")
        print("   1. Test the deployed agent using the returned resource name")
        print("   2. Verify Firestore and BigQuery logging")
        print("   3. Upload test invoices to GCS and process them")

        # Update deployment metadata
        import json
        metadata = {
            "remote_agent_runtime_id": reasoning_engine.resource_name,
            "deployment_timestamp": reasoning_engine.create_time.isoformat() if hasattr(reasoning_engine, 'create_time') else "unknown"
        }

        with open("deployment_metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        print()
        print(f"📝 Deployment metadata saved to deployment_metadata.json")

        return reasoning_engine

    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    deploy_agent()
