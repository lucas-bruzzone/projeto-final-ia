"""API HTTP da extração de vagas.

Sobe com:
    uvicorn main:app --reload

Documentação interativa: http://localhost:8000/docs
"""
from fastapi import FastAPI, HTTPException

from schemas import RequestExtracao, Vaga
from ollama_client import extrair_vaga, ErroExtracao


app = FastAPI(
    title="API de Extração de Vagas",
    description="Extrai campos estruturados de anúncios de vagas usando LLM.",
    version="0.1.0",
)


@app.get("/")
def raiz():
    """Endpoint de saúde. Útil para verificar se o serviço está no ar."""
    return {"servico": "extracao-vagas", "status": "ok"}


@app.post("/extrair", response_model=Vaga)
def extrair(pedido: RequestExtracao) -> Vaga:
    """Recebe o texto de um anúncio e devolve a vaga estruturada.

    Retorna 422 se o modelo não conseguir estruturar a resposta.
    """
    try:
        return extrair_vaga(pedido.texto)
    except ErroExtracao as e:
        # TODO (aluno): refinar o status code. Erro de comunicação com
        # Ollama provavelmente deve ser 503 (Service Unavailable),
        # erro de validação do JSON deve ser 422 (Unprocessable Entity).
        # Hoje tudo vira 422.
        raise HTTPException(status_code=422, detail=str(e))
