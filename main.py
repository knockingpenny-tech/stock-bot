import os
import yfinance as yf
import requests
import pandas as pd

# 1. 환경변수에서 디스코드 주소 가져오기
try:
    discord_url = os.environ['DISCORD_URL']
except KeyError:
    print("에러: 디스코드 주소(Secret)가 설정되지 않았습니다.")
    exit(1)

# 2. 감시할 종목 리스트 (알테오젠, 한국금융지주)
stocks = {
    '알테오젠': '196170.KQ',
    '한국금융지주': '071050.KS'
}

def calculate_rsi(data, window=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

final_message = ""

# 3. 종목 분석 시작
for name, code in stocks.items():
    try:
        # 데이터 가져오기
        df = yf.Ticker(code).history(period="6mo")
        
        if len(df) < 15:
            print(f"{name}: 데이터가 부족합니다.")
            continue
            
        # RSI 계산
        df['RSI'] = calculate_rsi(df)
        today_rsi = df['RSI'].iloc[-1]
        price = df['Close'].iloc[-1]
        
        # 매수/매도 판단
        status = ""
        if today_rsi < 30:
            status = f"🚨 [매수 찬스] 과매도 상태! (RSI {today_rsi:.1f})"
        elif today_rsi > 70:
            status = f"💰 [매도 주의] 과열 상태! (RSI {today_rsi:.1f})"
        
        # 신호가 있을 때만 메시지 추가
        if status:
            final_message += f"\n👉 **{name} ({price:,.0f}원)**\n{status}\n"
        else:
            print(f"{name}: 특이사항 없음 (RSI {today_rsi:.1f})")

    except Exception as e:
        print(f"{name} 분석 중 에러 발생: {e}")

# 4. 결과 전송 (신호가 하나라도 있을 때만)
#if final_message:
#    payload = {"content": f"📢 **오늘의 주식 알림**\n{final_message}"}
#    requests.post(discord_url, json=payload)
#    print("디스코드 알림 전송 완료")
# if final_message:  <-- 이 줄 앞에 #을 붙여서 무시하게 만듦
if True:            # <-- 무조건(True) 실행해라!
    test_msg = "🚨 주인님! 연결 테스트 성공했습니다! (RSI 감시 중)"
    requests.post(discord_url, json={"content": test_msg})
    print("강제 알림 전송 완료")
else:
    print("오늘은 보낼 알림이 없습니다.")
