# API de Extração de Vagas

API HTTP que recebe o texto de um anúncio de vaga e devolve um JSON
estruturado com os campos extraídos por um LLM rodando no Ollama.

Este é o esqueleto do projeto final da disciplina de Inteligência Artificial II.
A estrutura é funcional para o caso feliz — sua tarefa é iterar o prompt,
adicionar robustez e documentar suas decisões.

## Pré-requisitos

- Python 3.11+
- Ollama rodando (localmente ou no seu stack AWS Academy da Aula 14)
- Modelo `llama3.2:3b` disponível no Ollama

## Setup

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

## Configuração

Por padrão o cliente conecta em `http://localhost:11434` (Ollama local).
Para apontar para seu stack AWS, exporte a variável de ambiente antes de subir:

```bash
export OLLAMA_URL=http://SEU_EIP:11434
```

## Como rodar

```bash
uvicorn main:app --reload
```

A API sobe em `http://localhost:8000`.
Documentação interativa em `http://localhost:8000/docs`.

## Como testar

**Via Swagger (mais fácil):**

1. Abra `http://localhost:8000/docs`
2. Expanda o endpoint `POST /extrair`
3. Clique em "Try it out"
4. Cole um anúncio de `exemplos/anuncios.txt` no campo `texto`
5. Execute e inspecione o JSON retornado

**Via curl:**

```bash
curl -X POST http://localhost:8000/extrair \
  -H "Content-Type: application/json" \
  -d '{"texto": "Vaga de Desenvolvedor Junior na TechCorp..."}'
```

## Estrutura do projeto

```
api-extracao-vagas/
├── main.py             # rotas FastAPI
├── schemas.py          # modelos Pydantic (fonte da verdade do formato)
├── prompts.py          # templates de prompt (onde você mais itera)
├── ollama_client.py    # cliente do LLM
├── exemplos/
│   └── anuncios.txt    # anúncios de exemplo
├── requirements.txt
└── README.md
```

## O que você precisa completar

O esqueleto funciona, mas tem TODOs estratégicos. Procure por
`TODO (aluno)` nos arquivos:

- **`prompts.py`** — ponto principal de iteração. O prompt-base é razoável
  mas longe de ótimo. Adicione exemplos, refine instruções, teste com
  anúncios variados, considere variantes.
- **`ollama_client.py`** — tratamento de erros mais granular: distinguir
  timeout de erro de conexão, considerar retry em caso de JSON malformado.
- **`main.py`** — mapeamento mais fino de erros para status HTTP.

## Critérios de avaliação

| Critério | Peso |
|----------|------|
| Funcionamento ponta a ponta (API sobe, recebe, devolve) | 25% |
| Qualidade da extração (acerto em anúncios variados) | 30% |
| Robustez (tratamento de erros, entradas estranhas) | 15% |
| Qualidade do prompt (iteração visível, escolhas justificadas) | 15% |
| Organização do código (separação de módulos, legibilidade) | 10% |
| Documentação (README atualizado, exemplos) | 5% |

## Entrega

- Código completo no repositório do grupo
- README atualizado com as decisões de prompt tomadas
- Apresentação de 10 minutos na Aula 22 demonstrando o sistema funcionando

## Próximas aulas

- **Aula 17:** Avaliação de LLMs — como medir se a extração está boa
- **Aula 18:** Agents e tool use
- **Aula 19:** RAG (conceitual)
- **Aula 20:** Segurança em LLMs (prompt injection)
- **Aula 21:** Multimodalidade (conceitual) + apoio ao projeto
- **Aula 22:** Apresentações finais
