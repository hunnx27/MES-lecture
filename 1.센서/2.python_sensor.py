import json
import time
import random
from datetime import datetime


# 설비 목록 (Arduino 형식과 일치하도록 하이픈 포함)
EQUIPMENTS = ['EQ-001', 'EQ-002', 'EQ-003', 'EQ-004']

def generate_sensor_data(equipment_id):
    """센서 데이터 생성"""
    # 정상 범위의 센서값
    base_temp = 70
    base_pressure = 120
    base_vibration = 2.5
    
    # 랜덤 변동 추가
    temperature = round(base_temp + random.uniform(-10, 20), 2)
    pressure = round(base_pressure + random.uniform(-20, 40), 2)
    vibration = round(base_vibration + random.uniform(-1, 1), 2)
    
    # 10% 확률로 비정상 값 생성 (알람 테스트)
    if random.random() < 0.1:
        if random.choice([True, False]):
            temperature = round(base_temp + random.uniform(15, 30), 2)  # 온도 과열
        else:
            pressure = round(base_pressure + random.uniform(35, 60), 2)  # 압력 과다
    
    # speed: simulate RPM similar to Arduino `random(950,1000)`
    speed = random.randint(950, 1000)

    # provide epoch ms timestamp to match microcontroller style (millis())
    timestamp_ms = int(datetime.now().timestamp() * 1000)

    return {
        'equipment_id': equipment_id,
        'temperature': temperature,                 # 온도
        'pressure': pressure,                       # 압력
        'vibration': vibration,                     # 진동
        'timestamp': datetime.now().isoformat(),
        'timestamp_ms': timestamp_ms,
        'speed': speed
    }


def main():
    
    try:
        print("센서 시뮬레이터 시작...")
        print(f"장비: {EQUIPMENTS}")
        print("전송 주기: 1초\n")
        
        while True:
            print("# 센서 데이터 전송")
            for equipment_id in EQUIPMENTS:
                # 센서 데이터 생성
                sensor_data = generate_sensor_data(equipment_id)
                print(json.dumps(sensor_data))
            
            # 1초 대기
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n!! 센서 시뮬레이터 종료")
    except Exception as e:
        print(f"!! 오류 발생: {e}")

if __name__ == "__main__":
    main()