from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 각 캐릭터의 응답 로직을 불러옵니다.
from felix import get_felix_response
from emil import get_emil_response
from johannes import get_johannes_response
from klara import get_klara_response  # ← 추가

app = FastAPI(title="MCM 1976 해커톤 AI 챗봇 서버")

# CORS 설정: 프론트엔드 도메인에서 통신이 가능하도록 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 배포 시 프론트엔드 URL만 넣는 것을 권장합니다 (예: ["https://my-frontend.com"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 프론트엔드에서 보내올 JSON 데이터 형식 정의
class ChatRequest(BaseModel):
    session_id: str  # 사용자 구분을 위한 고유 ID (프론트엔드에서 생성하여 전송)
    message: str     # 사용자가 입력한 질문

@app.post("/chat/felix")
async def chat_felix(request: ChatRequest):
    reply = await get_felix_response(request.session_id, request.message)
    return {"reply": reply}

@app.post("/chat/emil")
async def chat_emil(request: ChatRequest):
    reply = await get_emil_response(request.session_id, request.message)
    return {"reply": reply}

@app.post("/chat/johannes")
async def chat_johannes(request: ChatRequest):
    reply = await get_johannes_response(request.session_id, request.message)
    return {"reply": reply}

@app.post("/chat/klara")  # ← 추가
async def chat_klara(request: ChatRequest):
    reply = await get_klara_response(request.session_id, request.message)
    return {"reply": reply}