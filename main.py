import os
import yfinance as yf
import requests
import pandas as pd

# 1. 환경변수에서 디스코드 주소 가져오기 (보안)
discord_url = os.environ['DISCORD_URL']

# 2. 감시할 종목 리스트 (이름: 코드)
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

# 3. 종목별 분석 및 메시지 작성
final_message = ""

for name, code in stocks.items():
    try:
        df = yf.Ticker(code).history(period="6mo")
        if len(df) < 15: continue # 데이터 부족하면 패스
        
        df['RSI'] = calculate_rsi(df)
        today_rsi = df['RSI'].iloc[-1]
        price = df['Close'].iloc[-1]
        
        # 매수/매도 로직
        status = ""
        if today_rsi <import os
import yfinance as yf
import requests
import pandas as pd

# 1. 환경변수에서 디스코드 주소 가져오기 (보안)
discord_url = os.environ['DISCORD_URL']

# 2. 감시할 종목 리스트 (이름: 코드)
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

# 3. 종목별 분석 및 메시지 작성
final_message = ""

for name, code in stocks.items():
    try:
        df = yf.Ticker(code).history(period="6mo")
        if len(df) < 15: continue # 데이터 부족하면 패스
        
        df['RSI'] = calculate_rsi(df)
        today_rsi = df['RSI'].iloc[-1]
        price = df['Close'].iloc[-1]
        
        # 매수/매도 로직
        status = ""
        if today_rsi < 30:
            status = f"🚨 [매수 찬스] 과매도 (RSI {today_rsi:.1f})"
        elif today_rsi > 70:
            status = f"💰 [매도 주의] 과열 (RSI {today_rsi:.1f})"
        
        # 특이사항 있을 때만 메시지에 추가
        if status:
            final_message += f"\n**{name} ({price:,.0f}원)**\n{status}\n"
        else:
            print(f"{name}: 특이사항 없음 (RSI {today_rsi:.1f})")

    except Exception as e:
        print(f"{name} 에러: {e}")

# 4. 알림 보내기 (메시지가 있을 때만)
if final_message:
    requests.post(discord_url, json={"content": f"📢 **오늘의 주식 알림**\n{final_message}"})
    print("알림 전송 완료")
else:
    print("오늘은 보낼 알림이 없습니다.") 30:
            status = f"🚨 [매수 찬스] 과매도 (RSI {today_rsi:.1f})"
        elif today_rsi > 70:
            status = f"💰 [매도 주의] 과열 (RSI {today_rsi:.1f})"
        
        # 특이사항 있을 때만 메시지에 추가
        if status:
            final_message += f"\n**{name} ({price:,.0f}원)**\n{status}\n"
        else:
            print(f"{name}: 특이사항 없음 (RSI {today_rsi:.1f})")

    except Exception as e:
        print(f"{name} 에러: {e}")

# 4. 알림 보내기 (메시지가 있을 때만)
if final_message:
    requests.post(discord_url, json={"content": f"📢 **오늘의 주식 알림**\n{final_message}"})
    print("알림 전송 완료")
else:
    print("오늘은 보낼 알림이 없습니다.")
