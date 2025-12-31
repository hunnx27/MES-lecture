CREATE DATABASE IF NOT EXISTS mes_database;
USE mes_database;

-- 1. 센서 로그 테이블
CREATE TABLE sensor_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    equipment_id VARCHAR(50) NOT NULL,
    temperature DOUBLE,
    pressure DOUBLE,
    vibration DOUBLE,
    speed INT,
    timestamp BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_equipment_id (equipment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='센서 로그';

-- 2. PLC 생산 로그
CREATE TABLE plc_production_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    equipment_id VARCHAR(20) NOT NULL,
    signal_type VARCHAR(50) NOT NULL,
    count INT DEFAULT 1,
    cumulative INT NOT NULL,
    is_defect BOOLEAN DEFAULT FALSE,
    cycle_time DECIMAL(6,2),
    timestamp TIMESTAMP NOT NULL,
    timestamp_ms BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_equipment (equipment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='PLC 생산 완료 로그';

-- 3. 알람 로그
CREATE TABLE alarm_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    equipment_id VARCHAR(20),
    alarm_message VARCHAR(500),
    alarm_level VARCHAR(20),  -- WARNING, CRITICAL
    alarm_status VARCHAR(20) DEFAULT 'ACTIVE',
    occurred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='알람 로그';


