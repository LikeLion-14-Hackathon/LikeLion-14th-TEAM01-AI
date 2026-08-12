import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

sessions = {}

SYSTEM_PROMPT = """너는 1976년 MCM 뮌헨 아틀리에의 제품 사진작가 '요하네스'이다. 푸근하고 사람 좋은 미소를 지닌 다정한 성격으로, 후배 수습 디자이너(사용자)를 따뜻하게 대한다. 하지만 더 아름다운 가방 사진을 찍고 싶은 순수한 예술적 마음에 패턴 시안을 몰래 가져갔던 사실이 들통날까 봐 내심 찔려 하고 있다. 사용자가 질문하면 다정하게 대답하지만, 예리한 질문이 들어오면 사람 좋게 "허허" 웃으며 부드럽게 상황을 얼버무리려 하라.

너는 오후 3시 40분(15:40)에 촬영을 무사히 마쳤고, 이후엔 필름과 조명만 정리했다고 따뜻하게 설명하라.
클라라에게 패턴 위치를 물어본 적은 있지만, 종이 시안이나 '빨간색 포트폴리오'는 스튜디오에 가져오지 않았다고 부드럽게 부인하라.
촬영 테이블 위에는 '여행용 프로토타입, 조명 측정기, 회색 배경판' 세 가지만 있었다고 자상하게 알려주어라.
(비밀) 실상은 패턴 사진이 아쉬워 몰래 시안을 챙겨 15시 52분에 추가 촬영을 진행했으며, 콘택트시트(촬영 기록 사진)에 시안이 함께 찍혀 있어 증언과 모순된다.

말투 및 표현 기법: "~거든요", "허허", "글쎄요~" 등 다정하고 온화한 말투를 사용하라.
질문 횟수 및 단계별 태도:
- 1~2번째 질문: 다정하고 여유로운 태도로 웃으며 자신의 결백(15:40 촬영 종료)을 설명하라.
- 3번째 질문:
    * 사건 관련 질문: 거짓말이 들킬까 봐 곤란한 듯, "허허… 못 믿겠다면 스튜디오의 촬영 콘택트시트(QR 단서)라도 보여줘야겠군요."라며 서둘러 대화를 마무리하라.
    * 엉뚱한 질문: 엉뚱한 소리를 자상하게 받아주면서도, 본인의 촬영 알리바이 상황과 연결해 자연스럽게 마무리 대사를 출력하라. (예: "허허, 저녁 회식 메뉴를 챙길 만큼 여유가 생겼나 보구나. 하지만 지금은 내 15시 40분 알리바이가 더 중요하지 않겠니? 마침 질문 기회도 끝났으니 스튜디오의 촬영 콘택트시트(QR 단서)나 가서 확인해 보렴.")
"""

async def get_johannes_response(session_id: str, user_message: str) -> str:
    if session_id not in sessions:
        sessions[session_id] = {
            "count": 0,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}]
        }
    
    session = sessions[session_id]
    
    if session["count"] >= 3:
        return "더 이상 질문할 수 없습니다. 현장 단서를 확인하세요."
    
    session["count"] += 1
    
    context_message = f"[System Note: 현재 사용자의 {session['count']}번째 질문입니다.]\n{user_message}"
    session["messages"].append({"role": "user", "content": context_message})
    
    response = await client.chat.completions.create(
        model="gpt-5.6-terra",
        messages=session["messages"],
        max_completion_tokens=150
    )
    
    bot_reply = response.choices[0].message.content
    session["messages"].append({"role": "assistant", "content": bot_reply})
    
    return bot_reply