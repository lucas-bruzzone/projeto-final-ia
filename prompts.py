"""Templates de prompt para extração.

Este é o arquivo onde você mais vai iterar. O prompt abaixo é um ponto de
partida razoável, mas longe de ótimo. Você vai precisar:

  - Adicionar mais exemplos no few-shot, cobrindo casos variados
  - Refinar a descrição dos campos
  - Tratar casos limite (vaga sem salário, sem localidade, etc.)
  - Testar com anúncios reais e ajustar

Cada iteração relevante deve ser justificada na entrega final.
"""


PROMPT_BASE = """Você é um analista de RH especializado em estruturar informações de vagas. Sua tarefa é extrair os campos abaixo a partir do texto do anúncio e retornar APENAS um JSON válido.

Campos esperados:
- cargo (string): título da vaga
- empresa (string ou null): nome da empresa contratante
- localidade (string ou null): cidade ou estado
- modalidade (string): "remoto", "hibrido" ou "presencial"
- nivel (string ou null): "estagio", "junior", "pleno" ou "senior"
- salario (objeto ou null): com campos "min" e "max" (números ou null)
- requisitos (lista de strings): habilidades exigidas
- beneficios (lista de strings): benefícios oferecidos

Regras:
- Use null para campos não declarados no anúncio
- NÃO invente informações que não estão escritas
- Salário "a combinar" ou não mencionado: null

Exemplo:
Anúncio: "Desenvolvedor Python Pleno na DataCorp, São Paulo - híbrido. Salário R$ 8000 a R$ 12000. Requisitos: Python, SQL, Docker. Benefícios: VR, plano de saúde."
JSON: {{"cargo": "Desenvolvedor Python", "empresa": "DataCorp", "localidade": "São Paulo", "modalidade": "hibrido", "nivel": "pleno", "salario": {{"min": 8000, "max": 12000}}, "requisitos": ["Python", "SQL", "Docker"], "beneficios": ["VR", "plano de saúde"]}}

Anúncio: "{texto}"
JSON:"""


def montar_prompt(texto: str) -> str:
    """Monta o prompt final substituindo o texto do anúncio.

    TODO (aluno): considere expandir esta função se quiser variantes
    (ex.: prompts diferentes para vagas técnicas vs não-técnicas, ou
    versões com mais/menos exemplos para comparar qualidade).
    """
    return PROMPT_BASE.format(texto=texto)
