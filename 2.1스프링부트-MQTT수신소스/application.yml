# application.yml
# Spring Boot MQTT 수신 설정

server:
  port: 8080

spring:
  application:
    name: mes-mqtt-receiver

# MQTT 설정
mqtt:
  broker:
    url: tcp://localhost:1883
    username: # 필요시 입력
    password: # 필요시 입력
  client:
    id: spring-boot-mqtt-client
  topics:
    sensor-data: factory/sensor/data
    alarm: factory/alarm
  qos: 1  # 0: 최대 1회, 1: 최소 1회, 2: 정확히 1회

# 로깅 설정
logging:
  level:
    root: INFO
    com.mes: DEBUG
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss} - %msg%n"