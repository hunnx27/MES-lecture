
import serial
import json
import time

# 아두이노가 연결된 포트와 보드 속도를 설정합니다.
# Windows: 'COMx', Linux: '/dev/ttyUSBx' 또는 '/dev/ttyACMx'
# 실제 포트 이름은 장치 관리자 등에서 확인해야 합니다.
SERIAL_PORT = 'COM4' 
BAUD_RATE = 9600

try:
    # 시리얼 포트 열기
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # 시리얼 포트 연결 대기

    print(f"{SERIAL_PORT} 포트가 열렸습니다. 아두이노 데이터 수신 중...")

    while True:
        if ser.in_waiting > 0:
            # 아두이노에서 보낸 한 줄의 데이터를 읽고 디코딩
            line = ser.readline().decode('utf-8').strip()
            
            if line:
                try:
                    # JSON 문자열을 파이썬 딕셔너리로 파싱
                    json_data = json.loads(line)
                    print("수신된 JSON 데이터 (딕셔너리):", json_data)
                    
                    # 파싱된 데이터의 특정 값 출력
                    print(f"센서 종류: {json_data['sensor']}, 값: {json_data['value']} {json_data['unit']}")
                    
                except json.JSONDecodeError:
                    print("잘못된 JSON 형식의 데이터 수신:", line)
        
        time.sleep(0.1)

except serial.SerialException as e:
    print(f"시리얼 포트 연결 오류: {e}")
except KeyboardInterrupt:
    print("프로그램 종료")
finally:
    if ser and ser.isOpen():
        ser.close()
        print("시리얼 포트가 닫혔습니다.")