import json
import os
import re
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI

from .prompts import ACTOR_SYSTEM, EVALUATOR_SYSTEM, REFLECTOR_SYSTEM
from .schemas import JudgeResult, QAExample, ReflectionEntry

load_dotenv()

llm_link = os.getenv("LLM_LINK", "").strip()
llm_model = os.getenv("LLM_MODEL", "").strip()

client: Optional[OpenAI] = OpenAI(base_url=llm_link, api_key="ollama") if llm_link else None

def _check_env() -> None:
    if not llm_link:
        raise ValueError("Missing LLM_LINK environment variable.")
    if not llm_model:
        raise ValueError("Missing LLM_MODEL environment variable.")


def _call_llm(system_prompt: str, user_prompt: str, label: str = "LLM") -> tuple[str, int]:
    """Gọi LLM và trả về (content, total_tokens)."""
    _check_env()
    active_client = client or OpenAI(base_url=llm_link, api_key="ollama")
    try:
        response = active_client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            timeout=60,
        )
    except Exception as exc:
        raise RuntimeError(f"{label} failed to call LLM: {exc}") from exc

    content = (response.choices[0].message.content if response.choices else None) or ""
    tokens = (response.usage.total_tokens if response.usage else 0)
    return content.strip(), tokens


def actor_answer_real(example: QAExample, attempt_id: int, agent_type: str, reflection_memory: list[str]) -> tuple[str, int]:
    context_block = "\n".join(f"- {chunk.title}: {chunk.text}" for chunk in example.context) or "- (no context provided)"
    reflection_block = "\n".join(f"- {item}" for item in reflection_memory) or "- (none)"
    user_prompt = (
        f"Question:\n{example.question}\n\n"
        f"Context:\n{context_block}\n\n"
        f"Reflection Memory:\n{reflection_block}\n\n"
        f"Attempt: {attempt_id}\n"
        f"Agent Type: {agent_type}\n\n"
        "Provide only the final answer."
    )
    return _call_llm(ACTOR_SYSTEM, user_prompt, label="actor_answer_real")


def _parse_json(text: str) -> dict:
    """Extract JSON từ response LLM, xử lý cả trường hợp có markdown code fence."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]+?)\s*```", text)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def evaluator_real(example: QAExample, answer: str) -> tuple[JudgeResult, int]:
    user_prompt = (
        f"Question:\n{example.question}\n\n"
        f"Gold Answer:\n{example.gold_answer}\n\n"
        f"Predicted Answer:\n{answer}\n\n"
        "Judge whether the predicted answer is correct."
    )
    raw, tokens = _call_llm(EVALUATOR_SYSTEM, user_prompt, label="evaluator_real")
    try:
        data = _parse_json(raw)
        result = JudgeResult(
            score=int(data.get("score", 0)),
            reason=str(data.get("reason", "")),
            missing_evidence=list(data.get("missing_evidence", [])),
            spurious_claims=list(data.get("spurious_claims", [])),
        )
    except Exception as exc:
        result = JudgeResult(score=0, reason=f"[parse error] {exc} | raw={raw[:200]}")
    return result, tokens


def reflector_real(example: QAExample, attempt_id: int, judge: JudgeResult) -> tuple[ReflectionEntry, int]:
    user_prompt = (
        f"Question:\n{example.question}\n\n"
        f"Attempt ID: {attempt_id}\n"
        f"Evaluator Feedback:\n"
        f"  score: {judge.score}\n"
        f"  reason: {judge.reason}\n"
        f"  missing_evidence: {judge.missing_evidence}\n"
        f"  spurious_claims: {judge.spurious_claims}\n\n"
        "Produce a reflection to guide the next attempt."
    )
    raw, tokens = _call_llm(REFLECTOR_SYSTEM, user_prompt, label="reflector_real")
    try:
        data = _parse_json(raw)
        result = ReflectionEntry(
            attempt_id=int(data.get("attempt_id", attempt_id)),
            failure_reason=str(data.get("failure_reason", judge.reason)),
            lesson=str(data.get("lesson", "")),
            next_strategy=str(data.get("next_strategy", "")),
        )
    except Exception as exc:
        result = ReflectionEntry(
            attempt_id=attempt_id,
            failure_reason=judge.reason,
            lesson=f"[parse error] {exc}",
            next_strategy="Re-read the context carefully and verify each hop before answering.",
        )
    return result, tokens

