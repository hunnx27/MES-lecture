import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime
import threading

# MQTT 브로커 설정
BROKER = 'localhost'
PORT = 1883
TOPIC = 'factory/sensor'

# MQTT Topics
TOPIC_SENSOR = 'factory/sensor'        # 센서 데이터
TOPIC_PLC = 'factory/plc'             # PLC 생산 완료 신호


# 설비 목록 (Arduino 형식과 일치하도록 하이픈 포함)
EQUIPMENTS = ['EQ-001', 'EQ-002', 'EQ-003', 'EQ-004']

# 설비별 사이클 타임 (초) - 제품 1개 생산하는데 걸리는 시간
CYCLE_TIMES = {
    'EQ-001': 8,   # 사출기 1호: 8초에 1개
    'EQ-002': 10,  # 사출기 2호: 10초에 1개
    'EQ-003': 5,   # 포장기 1호: 5초에 1개
    'EQ-004': 15   # 검사기 1호: 15초에 1개
}

# 설비별 생산 카운터
production_counters = {eq: 0 for eq in EQUIPMENTS}

mqtt_client = None

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"MQTT 브로커 연결 성공: {BROKER}:{PORT}")
    else:
        print(f"MQTT 브로커 연결 실패: {rc}")

def on_publish(client, userdata, mid):
    pass

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
    timestamp = datetime.now().isoformat()
    timestamp_ms = int(datetime.now().timestamp() * 1000)

    return {
        'equipment_id': equipment_id,
        'temperature': temperature,
        'pressure': pressure,
        'vibration': vibration,
        'speed': speed,
        'timestamp': timestamp,
        'timestamp_ms': timestamp_ms
    }

# ==========================================
# 1. 센서 데이터 전송 스레드 (매 1초)
# ==========================================
def sensor_thread():
    """센서 측정값을 1초마다 전송"""
    global mqtt_client
    
    print("📊 센서 데이터 전송 스레드 시작\n")
    
    while True:
        for equipment_id in EQUIPMENTS:
            sensor_data = generate_sensor_data(equipment_id)
            
            # MQTT 전송
            topic = f"{TOPIC_SENSOR}/{equipment_id}"
            payload = json.dumps(sensor_data)
            result = mqtt_client.publish(topic, payload)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                print(f"📊 [센서] {equipment_id}: "
                      f"온도={sensor_data['temperature']}°C, "
                      f"압력={sensor_data['pressure']}kPa, "
                      f"진동={sensor_data['vibration']}mm/s, "
                      f"RPM={sensor_data['speed']}")
        
        time.sleep(1)  # 1초 대기

# ==========================================
# 2. PLC 생산 완료 신호 스레드 (사이클마다)
# ==========================================
def plc_production_thread(equipment_id):
    """PLC처럼 생산 완료 신호를 사이클 타임마다 전송"""
    global mqtt_client
    
    cycle_time = CYCLE_TIMES[equipment_id]
    print(f"🏭 [{equipment_id}] PLC 가동 시작 (사이클: {cycle_time}초)")
    
    # 설비별로 시작 시간을 다르게 (동시 생산 방지)
    initial_delay = EQUIPMENTS.index(equipment_id) * 2
    time.sleep(initial_delay)
    
    while True:
        time.sleep(cycle_time)  # 사이클 타임 대기
        
        # 생산 완료!
        production_counters[equipment_id] += 1
        
        # 5% 확률로 불량 발생
        is_defect = random.random() < 0.05
        
        # PLC 생산 완료 신호
        plc_signal = {
            'equipment_id': equipment_id,
            'signal_type': 'PRODUCTION_COMPLETE',
            'count': 1,
            'cumulative': production_counters[equipment_id],
            'is_defect': is_defect,
            'cycle_time': cycle_time,
            'timestamp': datetime.now().isoformat(),
            'timestamp_ms': int(datetime.now().timestamp() * 1000)
        }
        
        # MQTT 전송
        topic = f"{TOPIC_PLC}/{equipment_id}"
        payload = json.dumps(plc_signal)
        result = mqtt_client.publish(topic, payload)
        
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            if is_defect:
                print(f"⚠️  [PLC] {equipment_id}: 생산 완료 +1개 → 불량품! (누적: {production_counters[equipment_id]})")
            else:
                print(f"✅ [PLC] {equipment_id}: 생산 완료 +1개 (누적: {production_counters[equipment_id]})")

def main():
    global mqtt_client
    
    try:
        # MQTT 클라이언트 생성
        mqtt_client = mqtt.Client()
        mqtt_client.on_connect = on_connect
        mqtt_client.on_publish = on_publish
        
        # 브로커 연결
        mqtt_client.connect(BROKER, PORT, 60)
        mqtt_client.loop_start()
        
        time.sleep(1)  # 연결 대기
        
        # 센서 데이터 전송 스레드 (1개)
        t_sensor = threading.Thread(target=sensor_thread, daemon=True)
        t_sensor.start()
        
        # 각 설비마다 PLC 생산 완료 신호 스레드
        for equipment_id in EQUIPMENTS:
            t_plc = threading.Thread(
                target=plc_production_thread,
                args=(equipment_id,),
                daemon=True
            )
            t_plc.start()
        
        # 메인 스레드는 계속 실행
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n⏹️  시뮬레이터 종료")
        print("\n📊 최종 생산 실적:")
        print("=" * 50)
        total_production = 0
        for eq in sorted(production_counters.keys()):
            count = production_counters[eq]
            total_production += count
            print(f"   {eq}: {count:4d}개 생산")
        print("=" * 50)
        print(f"   합계: {total_production:4d}개")
        print("=" * 50)
        
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()