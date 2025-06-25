from dotenv import load_dotenv
from typing import Optional
import warnings
import requests
import json
from langflow.load import run_flow_from_json
import streamlit as st
import logging


load_dotenv()


def check_langflow_connection():
    """Check if Langflow API is accessible"""
    try:
        response = requests.get("http://127.0.0.1:7860/api/v1/health", timeout=5)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def dict_to_string(obj, level=0):
    strings = []
    indent = "  " * level  # Indentation for nested levels

    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (dict, list)):
                nested_string = dict_to_string(value, level + 1)
                strings.append(f"{indent}{key}: {nested_string}")
            else:
                strings.append(f"{indent}{key}: {value}")
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested_string = dict_to_string(item, level + 1)
            strings.append(f"{indent}Item {idx + 1}: {nested_string}")
    else:
        strings.append(f"{indent}{obj}")

    return ", ".join(strings)


def ask_ai(profile: str, question: str):
    try:
        TWEAKS = {
            "TextInput-jeogt": {"input_value": question},
            "TextInput-NgtNe": {"input_value": dict_to_string(profile)},
        }

        result = run_flow_from_json(
            flow="AskAI.json",
            input_value="message",
            fallback_to_env_vars=False,
            tweaks=TWEAKS,
        )

        return result[0].outputs[0].results["text"].data["text"]
    except Exception as e:
        logging.error(f"AI ask_ai failed: {str(e)}")
        return f"Sorry, I'm having trouble connecting to the AI service. Please try again later. Error: {str(e)}"


def get_macros(profile, goals):
    try:
        TWEAKS = {
            "TextInput-2IzQH": {"input_value": ", ".join(goals)},
            "TextInput-nXmQI": {"input_value": dict_to_string(profile)},
        }
        return run_flow("", tweaks=TWEAKS)
    except Exception as e:
        logging.error(f"AI get_macros failed: {str(e)}")
        st.error(f"Failed to generate macros. Please check if Langflow is running on localhost:7860. Error: {str(e)}")
        return {"calories": 2000, "protein": 140, "fat": 20, "carbs": 100}  # Default fallback


def run_flow(
    message: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    application_token: Optional[str] = None,
) -> dict:
    api_url = f"http://127.0.0.1:7860/api/v1/run/macros"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {
            "Authorization": "Bearer " + application_token,
            "Content-Type": "application/json",
        }
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        
        return json.loads(
            response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"]
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"Langflow API request failed: {str(e)}")
        raise Exception(f"Failed to connect to Langflow API: {str(e)}")
    except (KeyError, json.JSONDecodeError) as e:
        logging.error(f"Invalid Langflow API response: {str(e)}")
        raise Exception(f"Invalid response from Langflow API: {str(e)}")
