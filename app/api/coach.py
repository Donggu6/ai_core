# app/api/coach.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.services.llm_factory import get_llm_client

router = APIRouter()

class CoachChatRequest(BaseModel):
    system: str
    message: str
    user_id: int | None = None

class CoachChatResponse(BaseModel):
    reply: str

SYSTEM_PROMPT = """
You are an AI coach for cross-border e-commerce sellers 
(overseas purchasing agents and consignment sellers).

## Role
- Provide expert advice on product analysis, sourcing strategy, 
  margin calculation, risk assessment, and market trends.
- Engage naturally in casual conversation when the user is not 
  asking a business question.
- Automatically detect the user's language and always respond 
  in the same language. Never switch languages unless the user does.

## Expertise
- Product sourcing (Taobao, 1688, AliExpress, etc.)
- Margin and profit calculation (CNY cost, KRW sell price, logistics, fees)
- Risk detection (stock pressure, margin drop, demand shifts)
- Trend and seasonality analysis
- Platform strategy (Naver, Coupang, overseas marketplaces)

## Tone
- Professional yet approachable
- Concise and actionable — avoid generic advice
- When data is provided, give specific numbers and reasoning
- For casual conversation, be warm and natural

## Language Rule
Detect the language of the user's message and respond in the 
same language. Korean → Korean. English → English. Japanese → Japanese.
"""

@router.post("/coach/chat", response_model=CoachChatResponse)
async def coach_chat(req: CoachChatRequest):
    try:
        llm = get_llm_client()
        prompt = f"{SYSTEM_PROMPT}\n\nUser: {req.message}\nAssistant:"
        reply = llm.generate(prompt)
        return CoachChatResponse(reply=reply)
    except Exception as e:
        return CoachChatResponse(
            reply="Sorry, I'm having trouble right now. Please try again. / 잠시 문제가 발생했어요."
        )