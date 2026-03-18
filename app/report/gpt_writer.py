# ✅ 통째로 교체: app/report/gpt_writer.py

from typing import Dict, Any

from app.services.llm_grok import GrokClient


grok_client = GrokClient()


def build_prompt(product: Dict[str, Any], features: Dict[str, Any], score: int) -> str:
    """
    상품/특징/점수를 받아서 Grok에 던질 프롬프트 생성.
    필요하면 아래 한국어 문구만 너 스타일에 맞게 수정해도 됨.
    """
    return (
        "너는 이커머스 셀러를 돕는 AI 컨설턴트야.\n"
        f"- 상품 ID: {product.get('id')}\n"
        f"- 가격: {product.get('price')}\n"
        f"- 주요 지표: {features}\n"
        f"- 점수: {score}\n\n"
        "위 정보를 바탕으로, 셀러가 바로 이해하고 실행할 수 있도록:\n"
        "1) 현재 상태 요약\n"
        "2) 핵심 개선 포인트\n"
        "3) 구체적인 액션 아이디어\n"
        "를 한국어로 5줄 이내로 작성해줘."
    )


def write_gpt_report(product: Dict[str, Any], features: Dict[str, Any], score: int) -> str:
    """
    analyze.py에서 그대로 호출하는 리포트 생성 함수.
    - 함수 이름/파라미터는 기존 그대로 유지.
    - 내부에서 xAI Grok(grok-code-fast-1)을 호출.
    """
    prompt = build_prompt(product, features, score)
    return grok_client.generate(prompt)
