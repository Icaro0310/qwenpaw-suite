#!/usr/bin/env python3
"""
QwenPaw Bridge -- Conecta Ollama local a AgentScope Platform / RAW.hq
via ngrok / Cloudflare Tunnel.

Endpoints:
  - GET  /health                  -> Status do serviço
  - GET  /api/tags                -> Lista modelos Ollama
  - POST /api/generate            -> Gera resposta via Ollama (nativo)
  - POST /v1/chat/completions     -> OpenAI-compatible (para AgentScope)
  - GET  /v1/models               -> Lista modelos (OpenAI format)
"""
import requests
import json
import os
import time
import logging
from functools import wraps
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Config ---
OLLAMA_URL = os.environ.get('OLLAMA_URL', 'http://localhost:11434')
BRIDGE_API_KEY = os.environ.get('BRIDGE_API_KEY', '')  # Opcional
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s [%(levelname)s] %(message)s'
)
log = logging.getLogger('qwenpaw-bridge')

# --- Auth middleware ---
def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if BRIDGE_API_KEY:
            auth = request.headers.get('Authorization', '')
            if not auth.replace('Bearer ', '') == BRIDGE_API_KEY:
                return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

# --- Existing endpoints ---

@app.route('/health', methods=['GET'])
def health():
    ollama_ok = False
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        ollama_ok = r.status_code == 200
    except Exception:
        pass
    return jsonify({
        "status": "ok",
        "ollama": OLLAMA_URL,
        "ollama_connected": ollama_ok,
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    })

@app.route('/api/generate', methods=['POST'])
@require_auth
def generate():
    data = request.json
    model = data.get('model', 'qwen2.5-coder:1.5b')
    prompt = data.get('prompt', '')
    log.info(f"[generate] model={model} prompt_len={len(prompt)}")

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        return jsonify(r.json())
    except Exception as e:
        log.error(f"[generate] error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tags', methods=['GET'])
@require_auth
def list_models():
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        return jsonify(r.json())
    except Exception as e:
        log.error(f"[tags] error: {e}")
        return jsonify({"error": str(e)}), 500

# --- OpenAI-compatible endpoints ---

@app.route('/v1/models', methods=['GET'])
@require_auth
def openai_models():
    """List models in OpenAI format."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        data = r.json()
        models = []
        for m in data.get('models', []):
            models.append({
                "id": m.get('name', 'unknown'),
                "object": "model",
                "created": int(time.time()),
                "owned_by": "ollama-local"
            })
        return jsonify({"object": "list", "data": models})
    except Exception as e:
        log.error(f"[v1/models] error: {e}")
        return jsonify({"object": "list", "data": []})

@app.route('/v1/chat/completions', methods=['POST'])
@require_auth
def openai_chat():
    """OpenAI-compatible chat completions via Ollama."""
    data = request.json
    model = data.get('model', 'qwen2.5-coder:1.5b')
    messages = data.get('messages', [])
    temperature = data.get('temperature', 0.7)
    max_tokens = data.get('max_tokens', 2048)

    log.info(f"[chat] model={model} msgs={len(messages)}")

    # Convert OpenAI messages to Ollama prompt
    prompt_parts = []
    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if role == 'system':
            prompt_parts.append(f"System: {content}")
        elif role == 'assistant':
            prompt_parts.append(f"Assistant: {content}")
        else:
            prompt_parts.append(f"User: {content}")
    prompt_parts.append("Assistant:")
    prompt = "\n".join(prompt_parts)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens
        }
    }

    try:
        r = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        result = r.json()
        response_text = result.get('response', '')

        # Return in OpenAI format
        return jsonify({
            "id": f"chatcmpl-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [{
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": response_text
                },
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": result.get('prompt_eval_count', 0),
                "completion_tokens": result.get('eval_count', 0),
                "total_tokens": result.get('prompt_eval_count', 0) + result.get('eval_count', 0)
            }
        })
    except Exception as e:
        log.error(f"[chat] error: {e}")
        return jsonify({"error": {"message": str(e), "type": "server_error"}}), 500

if __name__ == '__main__':
    log.info(f"QwenPaw Bridge starting on 0.0.0.0:5000")
    log.info(f"Ollama URL: {OLLAMA_URL}")
    log.info(f"Auth: {'enabled' if BRIDGE_API_KEY else 'disabled'}")
    app.run(host='0.0.0.0', port=5000)
