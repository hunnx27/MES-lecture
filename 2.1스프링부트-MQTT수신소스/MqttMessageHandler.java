package com.mes.service;

import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.extern.slf4j.Slf4j;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageHandler;
import org.springframework.messaging.MessagingException;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * MQTT 메시지 핸들러
 * - MQTT Broker로부터 수신한 메시지를 처리
 */
@Slf4j
@Component
public class MqttMessageHandler implements MessageHandler {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Override
    public void handleMessage(Message<?> message) throws MessagingException {
        try {
            // 1. 메시지 정보 추출
            String topic = message.getHeaders().get("mqtt_receivedTopic", String.class);
            String payload = message.getPayload().toString();
            
            log.info("📩 MQTT 메시지 수신");
            log.info("   📍 Topic: {}", topic);
            log.info("   📦 Payload: {}", payload);
            
            // 2. 토픽별 처리
            if (topic != null) {
                if (topic.contains("sensor/data")) {
                    handleSensorData(payload);
                } else if (topic.contains("alarm")) {
                    handleAlarm(payload);
                } else {
                    log.warn("⚠️  알 수 없는 토픽: {}", topic);
                }
            }
            
        } catch (Exception e) {
            log.error("❌ 메시지 처리 오류", e);
        }
    }

    /**
     * 센서 데이터 처리
     */
    private void handleSensorData(String payload) {
        try {
            // JSON 파싱
            Map<String, Object> data = objectMapper.readValue(payload, Map.class);
            
            log.info("🌡️  센서 데이터 파싱 완료:");
            log.info("   - 설비 ID: {}", data.get("equipment_id"));
            log.info("   - 온도: {}°C", data.get("temperature"));
            log.info("   - 압력: {}kPa", data.get("pressure"));
            log.info("   - 진동: {}mm/s", data.get("vibration"));
            log.info("   - 속도: {}RPM", data.get("speed"));
            
            // TODO: 다음 단계에서 DB 저장 구현
            
        } catch (Exception e) {
            log.error("❌ 센서 데이터 파싱 오류", e);
        }
    }

    /**
     * 알람 처리
     */
    private void handleAlarm(String payload) {
        try {
            // JSON 파싱
            Map<String, Object> alarm = objectMapper.readValue(payload, Map.class);
            
            log.warn("⚠️  알람 수신:");
            log.warn("   - 타입: {}", alarm.get("type"));
            log.warn("   - 메시지: {}", alarm.get("message"));
            log.warn("   - 시간: {}", alarm.get("timestamp"));
            
            // TODO: 다음 단계에서 DB 저장 구현
            
        } catch (Exception e) {
            log.error("❌ 알람 파싱 오류", e);
        }
    }
}