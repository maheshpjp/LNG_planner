import os
import requests
from typing import Dict, Optional, Any

LLM_ENDPOINTS = {
    'qwen': {
        'url': 'https://samuh.indianoil.in:30565/gateway/qwen3.5-122B-a10B-q6_k_l/v1',
        'env_key': 'LLM_QWEN_API_KEY',
        'model_id': 'qwen3.5:122b-a10b',
        'api_type': 'chat-completions',
    },
    'deepseek': {
        'url': 'https://samuh.indianoil.in:30565/gateway/DeepSeek-V4-Flash/v1',
        'env_key': 'LLM_DEEPSEEK_API_KEY',
        'model_id': 'deepseek-ai/DeepSeek-V4-Flash',
        'api_type': 'messages',
    },
}

class LLMClientError(Exception):
    pass


def _get_api_key(vendor_key: str) -> str:
    api_key = os.environ.get(vendor_key)
    if not api_key:
        raise LLMClientError(f'Missing LLM API key for {vendor_key}')
    return api_key


def _build_headers(provider: str) -> Dict[str, str]:
    endpoint = LLM_ENDPOINTS[provider]
    return {
        'Content-Type': 'application/json',
        'X-Gravitee-Api-Key': _get_api_key(endpoint['env_key']),
    }


def _build_payload(provider: str, prompt: str, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    endpoint = LLM_ENDPOINTS[provider]
    if endpoint['api_type'] == 'chat-completions':
        payload = {
            'model': endpoint['model_id'],
            'messages': [
                {'role': 'system', 'content': 'You are a helpful LNG planning assistant.'},
                {'role': 'user', 'content': prompt},
            ],
            'max_tokens': 2000,
        }
    else:
        payload = {
            'model': endpoint['model_id'],
            'input': prompt,
            'max_output_tokens': 2000,
        }
    if extra:
        payload.update(extra)
    return payload


def invoke_llm(provider: str, prompt: str, extra: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if provider not in LLM_ENDPOINTS:
        raise LLMClientError(f'Unknown LLM provider: {provider}')

    endpoint = LLM_ENDPOINTS[provider]
    headers = _build_headers(provider)
    payload = _build_payload(provider, prompt, extra)

    try:
        response = requests.post(endpoint['url'], headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        raise LLMClientError(f'LLM request failed: {exc}') from exc


def summarize_simulation(simulation_data: str, provider: str = 'qwen') -> str:
    prompt = (
        'Summarize the following LNG simulation data and return a short summary of the schedule and potential issues:\n\n'
        f'{simulation_data}'
    )
    result = invoke_llm(provider, prompt)

    if provider == 'qwen':
        choices = result.get('choices', [])
        if choices and isinstance(choices, list):
            return choices[0].get('message', {}).get('content', '').strip()
        return result.get('response', '')

    return str(result.get('output', result))
