import requests
import os
import json

from config import (
    USE_LLM,
    LLM_PROVIDER,
    LOG_DIR,
    # ollama
    OLLAMA_URL,
    OLLAMA_MODEL,
    # openai
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL
)

from logger import setup_logger

logger = setup_logger(LOG_DIR)


def build_prompt(name, candidates):
    return f"""
你是一个文件分类助手。

任务：
从候选目录中选择最匹配的一个。

要求：
- 只能返回候选中的一个
- 不要解释
- 如果没有合适的返回 NONE

torrent:
{name}

候选目录：
{json.dumps(candidates, ensure_ascii=False)}

输出：
"""


# ========================
# Ollama 调用
# ========================
def call_ollama(prompt):
    try:
        r = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=20
        )
        return r.json().get("response", "").strip()
    except Exception as e:
        logger.error(f"Ollama调用失败: {e}")
        return None


# ========================
# OpenAI 调用（兼容）
# ========================
def call_openai(prompt):
    try:
        r = requests.post(
            f"{OPENAI_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            },
            json={
                "model": OPENAI_MODEL,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0
            },
            timeout=20
        )

        data = r.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        logger.error(f"OpenAI调用失败: {e}")
        return None


# ========================
# 主逻辑
# ========================
def llm_match(name, base_path):
    if not USE_LLM:
        return None

    if not os.path.exists(base_path):
        return None

    candidates = [
        d for d in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, d))
    ]

    if not candidates:
        return None

    logger.info(f"[LLM] 候选目录: {candidates}")
    logger.info(f"[LLM] 输入: {name}")

    prompt = build_prompt(name, candidates)

    # 👉 根据配置选择模型
    if LLM_PROVIDER == "ollama":
        result = call_ollama(prompt)
    elif LLM_PROVIDER == "openai":
        result = call_openai(prompt)
    else:
        logger.error(f"未知LLM_PROVIDER: {LLM_PROVIDER}")
        return None

    if not result:
        return None

    # 清洗输出
    result = result.strip().replace('"', '').replace("'", "")

    if result == "NONE":
        return None

    if result in candidates:
        logger.info(f"[LLM匹配成功] {result}")
        return result

    logger.warning(f"[LLM输出非法] {result}")
    return None