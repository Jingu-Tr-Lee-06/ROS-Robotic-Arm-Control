2026 07 21

ROS 2의 주요 컨셉 및 특징, API 계층 구조, 그리고 마이크로 ROS(micro-ROS)의 핵심 기능 요약입니다.

---

### 1. ROS 2 핵심 컨셉 및 특징

* 
**산업용 수준의 상용 로봇 개발 표준**: 아카데믹/연구용 중심이었던 ROS 1과 달리 프로토타이핑부터 실제 산업 생산 배포(Designed for production)까지 전 과정을 지원하는 표준 플랫폼을 목표로 합니다 .


* **DDS(Data Distribution Service) 기반 미들웨어**:
* OMG 표준 실시간 미들웨어 기술인 DDS/RTPS를 기본 통신 프로토콜로 사용합니다.


* 중앙 관리자(`roscore`)에 의존하지 않는 **분산형 P2P 동적 검색(Dynamic Discovery)** 기능을 지원하여 단일 장애점(SPOF) 문제를 해결하고 Plug & Play 방식을 구현합니다 .


* 
**QoS(Quality of Service)** 정책 설정(Reliability, Durability, History 등)을 지원하여 네트워크 환경에 맞춰 데이터 수신 품질 및 실시간성을 보장합니다.




* 
**멀티 플랫폼 & 다중 도메인 지원**: Linux(Ubuntu)뿐만 아니라 Windows, macOS 및 실시간 OS(RTOS) 환경을 공식 지원합니다 .


* 
**보안성(Security) 향상**: DDS-Security 표준을 활용한 암호화, 인증, 접근 제어를 지원하여 로봇 시스템의 인프라 보안을 강화합니다.


* 
**다양한 프로그래밍 언어 지원 (RCL)**: C++(`rclcpp`), Python(`rclpy`) 외에도 C, Java, Rust 등 다양한 언어 라이브러리를 통해 개발 환경을 확장할 수 있습니다.


* 
**허용적 오픈소스 라이선스**: Apache 2.0 라이선스를 채택하여 기업의 지적 재산권을 보호하면서 자유롭게 라이브러리를 수정 및 재배포할 수 있습니다.



---

### 2. ROS 2 API 계층 구조

ROS 2는 통신 미들웨어 계층과 상위 사용자 코드 계층을 추상화하여 분리해 놓았습니다 .

1. 
**User Code (사용자 애플리케이션 계층)** 


* 개발자가 작성하는 노드, 로봇 제어 로직, 센서 데이터 처리 코드 등이 위치합니다.


2. 
**ROS 2 Client Library API (RCL 계층)** 


* 각 언어별 클라이언트 지원 라이브러리 계층입니다.
* 
`rclcpp` (C++), `rclpy` (Python), `rclc` (C) 등을 통해 퍼블리셔/서브스크라이버, 서비스, 액션, 파라미터 등의 API를 제공합니다.




3. 
**ROS 2 Middleware API (RMW 계층)** 


* 
**RMW(ROS Middleware Interface)**: 다양한 DDS 벤더 라이브러리를 단일한 표준 ROS 2 API로 추상화해 주는 C 기반 미들웨어 인터페이스입니다 .


* 유저 코드 영역에 특정 DDS 구현체의 코드가 직접 노출되지 않도록 막아줍니다.




4. 
**DDS Vendor Layer (DDS 미들웨어 계층)** 


* Fast DDS (eProsima), Cyclone DDS (Eclipse), Connext DDS (RTI) 등 실제 데이터 통신 및 네트워크 트래픽 관리를 담당하는 DDS 엔진입니다 .





---

### 3. 마이크로 ROS (micro-ROS) 주요 기능 및 특징

마이크로 ROS는 자원이 극도로 제한된 마이크로컨트롤러(MCU) 및 임베디드 시스템에 ROS 2를 탑재하기 위해 설계된 프레임워크입니다.

* **MCU 최적화 클라이언트 API (`rcl` + `rclc`)**:
* C 언어 기반의 `rcl` 및 확장 편의 라이브러리인 `rclc`를 이용해 노드, 퍼블리시/서브스크라이브, 서비스/클라이언트 등의 통신 매커니즘을 지원합니다 .


* 초기화 단계 이후 **동적 메모리 할당(Dynamic Memory Allocation)을 배제**하도록 설계되어 정적 메모리 풀을 활용하며 실시간성을 강화합니다.




* **경량화 미들웨어 (Micro XRCE-DDS)**:
* 자원 제약 환경(XRCE)에 최적화된 DDS 표준 프로토콜을 사용합니다 .


* Serial(UART), UDP/IP, Wi-Fi, Bluetooth 등 다양한 저전력 전송 계층을 지원합니다.




* **ROS 2와의 원활한 통합 (micro-ROS Agent)**:
* MCU 측의 micro-ROS 노드는 **micro-ROS Agent**를 매개로 하여 네트워크상의 표준 ROS 2 그래프에 결합됩니다.


* 대형 PC나 SBC의 표준 ROS 노드와 동일한 방식 및 CLI 도구(`ros2 topic` 등)로 MCU의 노드와 통신할 수 있습니다.




* **다중 RTOS 및 베어메탈 지원**:
* FreeRTOS, Zephyr, NuttX 등 대표적인 오픈소스 실시간 운영체제(RTOS)를 공식 지원하며 POSIX 환경 포팅을 지원합니다 .





---
개발환경 구축
