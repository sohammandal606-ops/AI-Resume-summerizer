import os
import time

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda


def get_llm():
    return ChatMistralAI(
        model=os.getenv("MISTRAL_MODEL", "mistral-large-latest"),
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.2,
        max_retries=5,
    )


def build_chain(system_prompt: str):
    llm = get_llm()
    return (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{text}"),
        ])
        | llm
        | StrOutputParser()
    )

def extract_all(transcript: str) -> tuple[str, str, str]:
    """Extracts Action Items, Key Decisions, and Open Questions in a single LLM call to save quota and prevent rate-limiting."""
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert meeting analyst. From the meeting transcript, extract three sections:\n\n"
            "1. ACTION ITEMS: Numbered list with Task description, Owner (who is responsible), Deadline (if mentioned, else 'Not specified'). If none, write 'No action items found.'\n"
            "2. KEY DECISIONS: Numbered list of all key decisions made. If none, write 'No key decisions found.'\n"
            "3. OPEN QUESTIONS: Numbered list of all unresolved questions or topics needing follow-up. If none, write 'No open questions found.'\n\n"
            "You MUST format your output with EXACTLY these three headers:\n"
            "### ACTION ITEMS\n"
            "<action items here>\n\n"
            "### KEY DECISIONS\n"
            "<key decisions here>\n\n"
            "### OPEN QUESTIONS\n"
            "<open questions here>",
        ),
        ("human", "{text}"),
    ])
    chain = prompt | get_llm() | StrOutputParser()
    raw = chain.invoke({"text": transcript})

    action_items = "No action items found."
    decisions = "No key decisions found."
    questions = "No open questions found."

    parts = raw.split("### ")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        lines = part.split("\n", 1)
        header = lines[0].strip().upper()
        content = lines[1].strip() if len(lines) > 1 else ""

        if "ACTION ITEM" in header:
            action_items = content
        elif "DECISION" in header:
            decisions = content
        elif "QUESTION" in header:
            questions = content

    return action_items, decisions, questions


def extract_action_items(transcript: str) -> str:
    items, _, _ = extract_all(transcript)
    return items


def extract_key_decisions(transcript: str) -> str:
    _, dec, _ = extract_all(transcript)
    return dec


def extract_questions(transcript: str) -> str:
    _, _, q = extract_all(transcript)
    return q