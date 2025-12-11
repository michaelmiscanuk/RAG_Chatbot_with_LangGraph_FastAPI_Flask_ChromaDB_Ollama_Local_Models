"""
Helper utilities for the workflow

This module provides utility functions for formatting output,
validating input, and other common tasks.
"""

import os
import uuid
import requests
import asyncio
from dotenv import load_dotenv


async def translate_text(text, target_language="en"):
    """Helper function that translates text to a target language using Azure Translator API.

    This function provides language translation for PDF chunk retrieval, where queries may be in
    Czech but PDF documentation is in English. It uses Azure Cognitive Services Translator API
    with asynchronous execution to avoid blocking the event loop.

    The function runs the synchronous HTTP request in a thread pool executor to maintain async
    compatibility while using the requests library. It generates a unique trace ID for each
    request to support debugging and monitoring.

    Args:
        text (str): Text to translate (any language supported by Azure Translator).
        target_language (str): Target language code (e.g., 'en', 'cs', 'de', 'fr'). Defaults to 'en'.

    Returns:
        str: Translated text in the target language.

    Key Steps:
        1. Load Azure Translator credentials from environment
        2. Construct translation endpoint URL with API version and target language
        3. Build HTTP headers with subscription key, region, and trace ID
        4. Create request body with input text
        5. Execute POST request in thread pool (async-safe)
        6. Parse JSON response and extract translated text
        7. Return translated text in target language

    Environment Variables Required:
        - TRANSLATOR_TEXT_SUBSCRIPTION_KEY: Azure Translator API key
        - TRANSLATOR_TEXT_REGION: Azure region (e.g., 'westeurope')
        - TRANSLATOR_TEXT_ENDPOINT: API endpoint URL

    API Details:
        - Endpoint: /translate?api-version=3.0&to={target_language}
        - Method: POST
        - Content-Type: application/json
        - Headers: Ocp-Apim-Subscription-Key, Ocp-Apim-Subscription-Region, X-ClientTraceId
    """
    load_dotenv()
    subscription_key = os.environ["TRANSLATOR_TEXT_SUBSCRIPTION_KEY"]
    region = os.environ["TRANSLATOR_TEXT_REGION"]
    endpoint = os.environ["TRANSLATOR_TEXT_ENDPOINT"]

    path = "/translate?api-version=3.0"
    params = f"&to={target_language}"
    constructed_url = endpoint + path + params

    headers = {
        "Ocp-Apim-Subscription-Key": subscription_key,
        "Ocp-Apim-Subscription-Region": region,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    body = [{"text": text}]

    # Run the synchronous request in a thread
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(
        None, lambda: requests.post(constructed_url, headers=headers, json=body)
    )
    result = response.json()
    return result[0]["translations"][0]["text"]

