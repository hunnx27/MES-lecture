package com.mes;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * MES MQTT 수신 애플리케이션
 */
@Slf4j
@SpringBootApplication
public class MesApplication {

    public static void main(String[] args) {
        SpringApplication.run(MesApplication.class, args);
        
        log.info("========================================");
        log.info("🚀 MES MQTT 수신 서비스 시작!");
        log.info("========================================");
        log.info("📡 MQTT Broker 연결 대기 중...");
        log.info("🎯 구독 토픽:");
        log.info("   - factory/sensor/data");
        log.info("   - factory/alarm");
        log.info("========================================");
    }
}