import requests
from config import LLM_API_URL

def match_by_llm(target, candidates):
    prompt = f"""
从候选中选出最匹配目标的动漫名称。
只返回一个字符串或 null。

目标:
{target}

候选:
{candidates}
"""

    try:
        resp = requests.post(LLM_API_URL, json={"prompt": prompt})
        text = resp.json().get("response", "").strip()

        if text in candidates:
            return text
    except:
        pass

    return None