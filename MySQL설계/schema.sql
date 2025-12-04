CREATE DATABASE IF NOT EXISTS smart_factory;
USE smart_factory;

-- 설비 마스터
CREATE TABLE equipment_master (
  equipment_id VARCHAR(50) PRIMARY KEY,
  equipment_name VARCHAR(100) NOT NULL,
  equipment_type VARCHAR(50),
  status ENUM('RUNNING', 'STOPPED', 'MAINTENANCE') DEFAULT 'STOPPED',
  location VARCHAR(100),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 센서 데이터
CREATE TABLE sensor_data (
  id INT AUTO_INCREMENT PRIMARY KEY,
  equipment_id VARCHAR(50),
  temperature DECIMAL(5,2),
  pressure DECIMAL(6,2),
  vibration DECIMAL(5,2),
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (equipment_id) REFERENCES equipment_master(equipment_id),
  INDEX idx_equipment_time (equipment_id, timestamp)
);

-- 작업 지시서
CREATE TABLE work_order (
  work_order_id INT AUTO_INCREMENT PRIMARY KEY,
  equipment_id VARCHAR(50),
  work_type VARCHAR(50),
  target_quantity INT,
  actual_quantity INT DEFAULT 0,
  status ENUM('PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED') DEFAULT 'PENDING',
  start_time TIMESTAMP NULL,
  end_time TIMESTAMP NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (equipment_id) REFERENCES equipment_master(equipment_id)
);

-- 알람 로그
CREATE TABLE alarm_log (
  alarm_id INT AUTO_INCREMENT PRIMARY KEY,
  equipment_id VARCHAR(50),
  alarm_type ENUM('WARNING', 'CRITICAL', 'INFO') DEFAULT 'WARNING',
  message TEXT,
  status ENUM('ACTIVE', 'ACKNOWLEDGED', 'RESOLVED') DEFAULT 'ACTIVE',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  resolved_at TIMESTAMP NULL,
  FOREIGN KEY (equipment_id) REFERENCES equipment_master(equipment_id)
);

-- 생산 실적
CREATE TABLE production_result (
  result_id INT AUTO_INCREMENT PRIMARY KEY,
  work_order_id INT,
  equipment_id VARCHAR(50),
  produced_quantity INT,
  defect_quantity INT DEFAULT 0,
  production_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (work_order_id) REFERENCES work_order(work_order_id),
  FOREIGN KEY (equipment_id) REFERENCES equipment_master(equipment_id)
);

-- 품질 검사
CREATE TABLE quality_check (
  check_id INT AUTO_INCREMENT PRIMARY KEY,
  work_order_id INT,
  check_type VARCHAR(50),
  result ENUM('PASS', 'FAIL') DEFAULT 'PASS',
  inspector VARCHAR(50),
  check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  notes TEXT,
  FOREIGN KEY (work_order_id) REFERENCES work_order(work_order_id)
);

-- 샘플 데이터
INSERT INTO equipment_master (equipment_id, equipment_name, equipment_type, status, location) VALUES
('EQ-001', '사출기 1호', 'INJECTION', 'RUNNING', 'A동 1층'),
('EQ-002', '사출기 2호', 'INJECTION', 'RUNNING', 'A동 1층'),
('EQ-003', '포장기 1호', 'PACKAGING', 'STOPPED', 'B동 2층'),
('EQ-004', '검사기 1호', 'INSPECTION', 'RUNNING', 'B동 1층');

INSERT INTO work_order (equipment_id, work_type, target_quantity, status) VALUES
('EQ-001', '플라스틱 부품 생산', 1000, 'IN_PROGRESS'),
('EQ-002', '금속 부품 생산', 500, 'PENDING');