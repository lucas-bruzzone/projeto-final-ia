"""Cliente para o servidor Ollama.

Isola toda a comunicação com o LLM. O resto da aplicação só chama
extrair_vaga() e recebe um objeto Vaga validado (ou um ErroExtracao).
"""
import os
import requests
from pydantic import ValidationError

from schemas import Vaga
from prompts import montar_prompt


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://32.199.236.244:11434")
MODELO = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
TIMEOUT_SEGUNDOS = 120


class ErroExtracao(Exception):
    """Erro genérico de extração. Será mapeado para HTTP 422/503 em main.py."""


def extrair_vaga(texto: str) -> Vaga:
    """Recebe o texto de um anúncio e devolve uma Vaga validada.

    Levanta ErroExtracao em caso de falha de comunicação, JSON inválido,
    ou validação Pydantic falhar.
    """
    prompt = montar_prompt(texto)
    payload = {
        "model": MODELO,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    # TODO (aluno): adicionar tratamento granular de timeout
    # (requests.Timeout) e de erro de conexão (requests.ConnectionError).
    # Hoje qualquer erro de rede vira ErroExtracao genérica.
    try:
        resposta = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=TIMEOUT_SEGUNDOS,
        )
        resposta.raise_for_status()
    except requests.RequestException as e:
        raise ErroExtracao(f"Falha ao chamar Ollama: {e}") from e

    json_cru = resposta.json().get("response", "")

    # TODO (aluno): em raras situações o modelo retorna JSON sintaticamente
    # inválido apesar do format="json", ou retorna JSON válido mas com
    # campos faltando. Considerar uma re-tentativa com prompt mais estrito
    # antes de falhar definitivamente.
    try:
        return Vaga.model_validate_json(json_cru)
    except ValidationError as e:
        raise ErroExtracao(
            f"Modelo retornou JSON que nao bate com o schema Vaga: {e}"
        ) from e
