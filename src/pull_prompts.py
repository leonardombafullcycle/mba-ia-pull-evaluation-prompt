"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def pull_prompts_from_langsmith():
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_path = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v1.yml"

    if not check_env_vars(["LANGSMITH_API_KEY"]):
        raise RuntimeError("Configure LANGSMITH_API_KEY no arquivo .env antes de continuar.")

    print(f"Puxando prompt do LangSmith Hub: {prompt_name}")
    prompt = hub.pull(prompt_name)

    messages = getattr(prompt, "messages", [])
    system_prompt = ""
    user_prompt = ""

    for message in messages:
        template = getattr(getattr(message, "prompt", None), "template", None)
        if template is None:
            template = getattr(message, "template", None)
        if not template:
            continue

        message_type = getattr(message, "type", "")
        message_class = type(message).__name__.lower()
        if (
            (message_type == "system" or "systemmessageprompttemplate" in message_class)
            and not system_prompt
        ):
            system_prompt = template
        elif (
            message_type in {"human", "user"}
            or "humanmessageprompttemplate" in message_class
            or "usermessageprompttemplate" in message_class
        ) and not user_prompt:
            user_prompt = template

    if not system_prompt:
        raise ValueError("O prompt retornado não contém uma mensagem system válida.")

    data = {
        "bug_to_user_story_v1": {
            "description": "Prompt importado do LangSmith Prompt Hub",
            "system_prompt": system_prompt,
            "user_prompt": user_prompt or "{bug_report}",
            "version": "v1",
            "tags": ["bug-analysis", "user-story", "product-management"],
        }
    }

    if not save_yaml(data, str(output_path)):
        raise OSError(f"Não foi possível salvar o prompt em {output_path}.")

    print(f"✓ Prompt salvo em: {output_path}")
    return str(output_path)


def main():
    """Função principal"""
    print_section_header("PULL DE PROMPTS DO LANGSMITH")
    try:
        pull_prompts_from_langsmith()
        return 0
    except Exception as exc:
        print(f"❌ Falha ao fazer pull do prompt: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
