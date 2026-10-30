"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Prompt inválido:")
        for error in errors:
            print(f"   - {error}")
        return False

    prompt = ChatPromptTemplate.from_messages([
        ("system", prompt_data["system_prompt"]),
        ("human", prompt_data.get("user_prompt", "{bug_report}")),
    ])

    techniques = ", ".join(prompt_data.get("techniques_applied", []))
    tags = ", ".join(prompt_data.get("tags", []))
    description = prompt_data.get("description", "Prompt otimizado para converter bugs em User Stories")
    description = f"{description}. Técnicas: {techniques}. Tags: {tags}."

    try:
        hub.push(
            prompt_name,
            prompt,
            new_repo_is_public=True,
            new_repo_description=description,
            tags=prompt_data.get("tags", []),
        )
        print(f"✓ Prompt publicado como público: {prompt_name}")
        return True
    except Exception as exc:
        print(f"❌ Erro ao publicar prompt: {exc}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    errors = []
    required_fields = ["description", "system_prompt", "version", "techniques_applied"]

    for field in required_fields:
        if field not in prompt_data:
            errors.append(f"Campo obrigatório ausente: {field}")

    if not isinstance(prompt_data.get("system_prompt"), str) or not prompt_data["system_prompt"].strip():
        errors.append("system_prompt está vazio")

    if not isinstance(prompt_data.get("user_prompt", "{bug_report}"), str):
        errors.append("user_prompt deve ser texto")

    techniques = prompt_data.get("techniques_applied", [])
    if not isinstance(techniques, list) or len(techniques) < 2:
        errors.append("Informe pelo menos duas técnicas em techniques_applied")

    prompt_text = f"{prompt_data.get('system_prompt', '')}\n{prompt_data.get('user_prompt', '')}"
    if "[TODO]" in prompt_text or "TODO" in prompt_text:
        errors.append("O prompt ainda contém TODOs")

    return (len(errors) == 0, errors)


def main():
    """Função principal"""
    print_section_header("PUSH DE PROMPTS PARA O LANGSMITH")

    provider_vars = ["LANGSMITH_API_KEY", "USERNAME_LANGSMITH_HUB"]
    if not check_env_vars(provider_vars):
        return 1

    prompt_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "prompts",
        "bug_to_user_story_v2.yml",
    )
    prompt_document = load_yaml(prompt_path)
    if not prompt_document or "bug_to_user_story_v2" not in prompt_document:
        print(f"❌ Prompt v2 não encontrado ou inválido: {prompt_path}")
        return 1

    prompt_data = prompt_document["bug_to_user_story_v2"]
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_name = f"{username}/bug_to_user_story_v2"

    return 0 if push_prompt_to_langsmith(prompt_name, prompt_data) else 1


if __name__ == "__main__":
    sys.exit(main())
