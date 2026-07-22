# ROS-Robotic-Arm-Control
2026 Academic Year Robotic Arm Control Project(KNU, Com-Edu, LJH)

---
July 20, 2026

## 💻 PART 1. 로컬 개발 환경 구축 (WSL2 & VS Code & Git)

### 1. WSL2 (Ubuntu 24.04 LTS) 설치 및 가상화 최적화

Windows Subsystem for Linux 2(WSL2)는 Windows 커널 위에서 완벽한 Linux 환경을 제공한다.

1. **PowerShell(관리자 권한) 실행** 후 아래 명령어를 입력하여 Ubuntu 24.04 버전을 명시적으로 설치한다.
```powershell
wsl --install -d Ubuntu-24.04

```


2. **PC 재부팅** 요구 메시지가 출력되면 시스템을 재시작한다.
3. 재부팅 후 자동으로 열리는 가상 터미널에서 계정 정보를 등록한다.
* **Username**: 리눅스 계정명 (공백 없는 소문자 권장)
* **Password**: 관리자 권한(`sudo`) 인증용 비밀번호 (입력 시 화면에 표시되지 않음)



> 💡 **WSL2 필수 팁 (메모리 제한)**
> WSL2는 기본적으로 Windows RAM의 최대 80%까지 점유하여 호스트 PC가 느려질 수 있다. Windows 사용자 폴더(`C:\Users\<사용자명>\`)에 `.wslconfig` 파일을 생성하고 아래 내용을 저장하여 자원을 제한하는 것이 좋다.
> ```ini
> [wsl2]
> memory=8GB # 본인 RAM의 50% 수준 권장
> processors=4
> 
> ```
> 
> 

---

### 2. GitHub 저장소 연동 및 Git 전역 설정

코드 버전 관리 및 원격 백업을 위해 Git의 전역 변수를 설정하고 SSH 기반 통신 또는 HTTPS 인증을 준비한다.

```bash
# Git 전역 사용자 정보 설정
git config --global user.name "Your GitHub Name"
git config --global user.email "your_email@example.com"

# 설정 정상 반영 확인
git config --list

```

GitHub에서 `ros2_workspace`라는 빈 리포지토리를 생성한 뒤, WSL 터미널로 돌아와 클론(Clone)을 진행한다.

```bash
# 홈 디렉토리로 이동 후 작업 공간 클론
cd ~
git clone https://github.com/your-username/ros2_workspace.git
cd ros2_workspace

```

---

### 3. VS Code와 WSL 원격 개발 패키지 연동

Windows에 설치된 VS Code와 WSL2 내부의 리눅스 파일 시스템을 완전히 결합하여 개발 효율을 극대화한다.

1. Windows VS Code의 확장 마켓플레이스(`Ctrl + Shift + X`)에서 **WSL (Microsoft)** 확장을 설치한다.
2. WSL Ubuntu 터미널 내 프로젝트 폴더에서 다음 명령을 실행하면 Windows의 VS Code 가 가상 환경 내부를 바라보며 실행된다.
```bash
code .

```


3. **첫 커밋 및 푸시 가이드**: VS Code 내장 터미널(`Ctrl + ~`)을 열어 초기 코드를 원격 저장소에 반영한다.
```bash
# 변경사항 스테이징 및 커밋
git add .
git commit -m "Feat: Initial commit with ROS2 setup environment"

# 메인 브랜치로 푸시
git push origin main

```



---

## 🤖 PART 2. ROS 2 Jazzy Jalisco 완벽 설치 (Ubuntu 24.04 LTS)

ROS 2 Jazzy Jalisco는 Ubuntu 24.04 Noble Numbat 버전을 공식 티어로 지원한다. APT 패키지 매니저가 깨지지 않도록 순서대로 명령어를 수행해야 한다.

### 1. 시스템 로케일(Locale) 인코딩 설정

ROS 2는 시스템 인코딩 언어 설정이 `UTF-8`이 아닐 경우 노드 간 통신에서 예기치 못한 에러가 발생한다. 이를 사전에 강제 동기화한다.

```bash
sudo apt update && sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# 현재 셸 세션에 즉시 반영
export LANG=en_US.UTF-8

```

---

### 2. ROS 2 공식 APT 저장소 및 보안 키(GPG Key) 등록

Ubuntu 기본 레포지토리 외에 Open Robotics에서 제공하는 공식 패키지 저장소를 시스템에 등록한다.

```bash
# 의존성 패키지 및 Universe 저장소 활성화
sudo apt install software-properties-common -y
sudo add-apt-repository universe -y

# APT 보안을 위한 ROS 2 GPG Key 다운로드 및 저장
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# ROS 2 공식 패키지 소스 리스트 추가
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

```

---

### 3. ROS 2 데스크톱 패키지 및 빌드 툴체인 설치

```bash
# 저장소 리스트를 갱신하고 기존 시스템 패키지 업그레이드
sudo apt update
sudo apt upgrade -y

# ROS 2 핵심 레이어 및 GUI/시뮬레이션 포함 풀 패키지 설치
sudo apt install ros-jazzy-desktop -y

# ROS 2 개발용 컴파일러, 빌드도구(colcon), 의존성 관리자(rosdep) 툴체인 일괄 설치
sudo apt install ros-dev-tools -y

```

---

### 4. 셸 환경 변수 자동 스크립트(`~/.bashrc`) 등록

새로운 터미널 탭이 생성될 때마다 ROS 2 명령어가 메모리에 자동 로드되도록 환경 스크립트를 지정한다.

```bash
# 환경 설정 스크립트 추가
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

# 현재 셸 터미널에 즉시 적용
source ~/.bashrc

```

---

## 🐢 PART 3. ROS 2 핵심 개념 구조화 및 심화 CLI 실습

ROS 2의 통신 패러다임은 노드(Node), 토픽(Topic), 서비스(Service), 액션(Action), 파라미터(Parameter)로 구분된다. 대표 예제인 `turtlesim`을 통해 실무형 명령어를 심층적으로 학습한다.

### 1. Turtlesim 실행 및 노드 네임스페이스 리매핑 (Remapping)

```bash
# [Terminal 1] 시뮬레이터 그래픽 노드 실행
ros2 run turtlesim turtlesim_node

# [Terminal 2] 키보드 텔레오퍼레이션 제어 노드 실행
ros2 run turtlesim turtle_teleop_key

```

> 💡 **심화: 리매핑(Remapping)의 중요성**
> 현업에서 동일한 센서나 동일한 로봇을 여러 대 띄워야 할 때 노드 이름이 충돌하면 통신이 꼬이게 된다. 이때 실행 시점에 이름을 변경하는 리매핑 기술이 필수적이다.
> ```bash
> # 특정 이름을 부여하여 단독 노드로 분리 실행
> ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle
> 
> ```
> 
> 

---

### 2. 노드 및 토픽 상태 추적 심화

#### A. 노드(Node) 인프라 확인

```bash
# 현재 그래프 상에서 살아있는 모든 노드 검색
ros2 node list

# 특정 노드가 발행(Publish)하고 구독(Subscribe)하는 채널 정보의 상세 아키텍처 조회
ros2 node info /turtlesim

```

#### B. 토픽(Topic) 데이터 스트림 분석

```bash
# 현재 개설된 토픽 목록과 통신 메시지 타입(-t)을 함께 출력 (디버깅 필수 명령어)
ros2 topic list -t

# 실시간으로 발행되는 토픽의 데이터 패킷 열람 (거북이의 현재 X, Y 좌표, 각도 스트리밍)
ros2 topic echo /turtle1/pose

# 토픽의 통신 빈도수(Hz)를 측정하여 데이터 병목 현상 체크
ros2 topic hz /turtle1/pose

```

#### C. CLI를 이용한 1회성 데이터 발행 (Publishing)

지정한 토픽 채널로 원시 메시지(Raw Message) 구조를 직접 주입하여 노드의 반응을 테스트한다.

```bash
# --once 옵션: 1회만 발행 후 종료 / 구조체 데이터 전송을 통해 거북이를 x축 방향으로 1.0 전진시킴
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"

```

---

### 3. 서비스(Service) 동적 동기 통신 호출

서비스는 토픽(비동기 스트리밍)과 달리 요청(Request)과 응답(Response)으로 이루어진 일회성 동기 통신 메커니즘이다.

```bash
# 새로운 거북이 객체를 특정 좌표(x=2.0, y=2.0, theta=0.2)에 생성하는 서비스 동적 호출
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.2, name: 'turtle2'}"

# 시뮬레이터 내부의 궤적을 모두 지우고 초기화하는 서비스 호출
ros2 service call /clear std_srvs/srv/Empty

```

---

### 4. 파라미터(Parameter) 런타임 제어 및 백업(Dump / Load)

파라미터는 노드 내부 전역 변수를 외부에서 실시간으로 갱신하는 기능이다. 시뮬레이터의 배경색(RGB)을 조절하며 런타임 제어를 실습한다.

#### A. 실시간 파라미터 갱신 및 렌더링 반영

```bash
# 1. 대상 노드의 파라미터 리스트 확보
ros2 param list

# 2. 현재 지정된 Green 채널 값 가져오기
ros2 param get /turtlesim background_g

# 3. 파라미터 런타임 수정 (RGB 값을 변경하여 어두운 네이비 계열 배경 연출)
ros2 param set /turtlesim background_r 30
ros2 param set /turtlesim background_g 30
ros2 param set /turtlesim background_b 35

# 4. 변경된 파라미터 설정 값을 화면 노드에 렌더링 리프레시 요청
ros2 service call /clear std_srvs/srv/Empty

```

#### B. 파라미터 상태 백업(Dump) 및 런타임 인젝션(Load)

실무에서 튜닝된 로봇의 센서 캘리브레이션 값이나 PID 제어 게인 값을 파일로 영구 저장하고 재사용할 때 사용한다.

```bash
# 현재 노드가 가진 모든 파라미터 세팅 상태를 YAML 구조 파일로 내보내기
ros2 param dump /turtlesim > ./turtlesim.yaml

# 실행 중인 기존 노드에 파일 기반으로 파라미터 설정을 한 번에 강제 주입(Load)
ros2 param load /turtlesim ./turtlesim.yaml

# [핵심] 노드 최초 구동 시점부터 백업된 파라미터 프로필 파일 적용하여 실행하기
ros2 run turtlesim turtlesim_node --ros-args --params-file ./turtlesim.yaml

```

---

### 5. GUI 시각화 및 노드 네트워크 분석 도구 (RQT)

ROS 2 인터페이스 아키텍처를 시각적으로 확인하고 동적 그래프를 모니터링하기 위한 Qt 기반 핵심 프레임워크다.

```bash
# RQT 종합 플러그인 컨테이너 실행
rqt

# 현재 활성화된 노드 간의 데이터 송수신 흐름(발행-구독 구조)을 가시화하는 컴퓨테이션 그래프 출력
rqt_graph

```

---

## 🛠️ PART 4. 예기치 못한 에러 발생 시 대처 가이드 (Troubleshooting)

1. **`ros2: command not found` 오류 발생 시**
* 원인: 현재 사용 중인 터미널 셸에 ROS 2 환경 변수가 로드되지 않음.
* 해결: `source /opt/ros/jazzy/setup.bash` 명령어를 실행하거나 `~/.bashrc` 파일 하단에 정상적으로 기재되었는지 확인한다.


2. **WSL2 환경에서 `rqt`나 `turtlesim_node` 실행 시 GUI 창이 뜨지 않는 경우**
* 원인: WSL2와 Windows 호스트 간 X11 디스플레이 포워딩 및 WSLg 그래픽 백엔드 통신 오류.
* 해결: WSL 터미널에서 `echo $DISPLAY`를 입력하여 값이 비어있지 않은지 확인하고, 해결되지 않을 시 PowerShell에서 `wsl --shutdown` 후 가상머신을 완전히 재부팅한다. Windows 11 최신 빌드 기준 WSLg가 내장되어 별도 설정 없이 연동되는 것이 정상이다.
---
July 21, 2026

# 📑 ROS 2 개발 및 트러블슈팅 종합 정리 보고서

---

## 1. ROS 2 환경 및 도구 트러블슈팅 (Troubleshooting)

### ① rqt GUI 독(Dock) 창 분리/먹통 현상 해결

* **증상**: rqt 실행 중 플러그인(퍼블리셔 등) 창이 독립적으로 튀어나와 드래그 및 조작이 불가능한 현상.
* **원인**: rqt의 독 레이아웃 및 GUI 캐시 설정 파일이 충돌/꼬임.
* **해결방법**:
```bash
# 1. 실행 중인 rqt 프로세스 종료
killall rqt

# 2. 캐시 설정 폴더 및 파일 삭제 (또는 rqt --clear-config 명령어 실행)
rm -rf ~/.config/ros.org/rqt* ~/.ros/rqt_gui*

```



### ② 실행 파일 인식 에러 (`No executable found`)

* **증상**: `ros2 run gong_basic move_turtle` 실행 시 노드를 찾을 수 없다는 오류 발생.
* **점검 및 해결**:
1. 워크스페이스 빌드 및 환경변수 로드 여부 확인:
```bash
colcon build
source install/setup.bash

```


2. `setup.py`의 `entry_points` 항목에 실행 경로 등록 여부 점검:
```python
'console_scripts': [
    'move_turtle = gong_basic.move_turtle:main',
],

```





---

## 2. 파이썬 노드 개발 및 패키지 정제 (Node & Package Practice)

### ① `setup.py` 패키지 설정 최적화

* **오류 원인**: `setup.py` 내부에 메시지 모듈(`from geometry_msgs.msg import Twist`)을 잘못 import하여 빌드 시 문제 발생.
* **정제 내용**: `setup.py`에는 메시지 import 구문을 제거하고 패키지 메타데이터 및 빌드 설정만 유지.
* **Launch 파일 복사 설정 (경로 오타 수정)**:
* `lunch` $\rightarrow$ `launch` 오타 수정 후 `data_files` 경로 지정:
```python
(os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),

```





### ② 노드 기본 구조 및 예외 처리 (Exception Handling)

* **`super().__init__('노드이름')` 필수 작성**:
`Node` 클래스 상속 시 부모 클래스 초기화 구문이 누락되면 내부 ROS 2 통신 인프라가 구성되지 않아 Runtime Error가 발생함.
* **`Ctrl + C` (SIGINT) 종료 시 이중 셧다운/경고 방지**:
종료 시점(`rclpy.shutdown()`)에 logger 호출 시 발생할 수 있는 `publisher's context is invalid` 경고 및 `RCLError` 예외 처리:
```python
try:
    rclpy.spin(node)
except KeyboardInterrupt:
    print("노드가 사용자에 의해 종료되었습니다.")  # get_logger() 대신 print 사용
finally:
    if rclpy.ok():
        rclpy.shutdown()

```



### ③ ROS 2 메시지 타입 및 주기 설정

* **메시지 타입 선택**:
* `std_msgs.msg.String`: 순수 텍스트 데이터 transmission용 (`frame_id`, `stamp` 없음).
* `std_msgs.msg.Header`: 타임스탬프(`stamp`)와 좌표계 정보(`frame_id`)가 필요할 때 활용.
* `geometry_msgs.msg.Twist`: 거북이 등 로봇 제어를 위한 선속도(`linear`) 및 각속도(`angular`) 정의.


* **타이머 제어**: 주기를 `1.0s` $\rightarrow$ `0.1s`로 변경하여 **10Hz** 주기로 메시지 발행.

---

## 3. Turtlesim 기하학적 나선 문양(Spirograph) 제어

* **구현 목표**: 삼각함수를 적용하여 매끄럽고 복잡한 나선 궤적 그리기.
* **핵심 로직**:
* `geometry_msgs.msg.Twist`의 `linear.x`는 일정하게 유지하고, `angular.z`를 `math.cos()` 기반으로 주기적으로 변동시킴.
* 내접/외접을 반복하는 매끄러운 Spirograph 패턴 완성.



---

## 4. 다중 노드 / 토픽 구조 설계 및 Launch 매핑

### ① 토픽 및 노드 토폴로지 (Topology)

* **1:N 통신**: `/massage` 토픽 1개를 `mpub`가 발행하고, `msub`, `m2sub`, `mtsub` 3개의 구독자가 동시 수신.
* **다중 구독 (Multi-Subscription)**: `mtsub` 노드가 `/massage` 토픽과 `/header` 토픽 2개를 동시 구독.

```
                  ┌─────────┐
                  │  tpub   │
                  └────┬────┘
                       │ /header
                       ▼
┌─────────┐       ┌─────────┐
│  mpub   ├──┬───►│  mtsub  │
└─────────┘  │    └─────────┘
   /massage  ├──► ┌─────────┐
             │    │  msub   │
             │    └─────────┘
             └──► ┌─────────┐
                  │  m2sub  │
                  └─────────┘

```

### ② `multi_node.launch.py`를 활용한 리매핑(Remapping)

노드 소스 코드를 직접 수정하지 않고, Launch 파일에서 `name` 파라미터를 지정하여 노드 이름을 동적으로 변경 실행:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1:N 퍼블리셔 및 구독자
        Node(package='gong_basic', executable='class_pub', name='mpub'),
        Node(package='gong_basic', executable='class_sub', name='msub'),
        Node(package='gong_basic', executable='class_sub', name='m2sub'),
        
        # Header 퍼블리셔 및 다중 구독자
        Node(package='gong_basic', executable='header_pub', name='tpub'),
        Node(package='gong_basic', executable='mtsub_node', name='mtsub'),
    ])

```

* **결과 검증**: `ros2 run rqt_graph rqt_graph` 실행을 통해 1:N 토픽 분기 및 다중 수신 그래픽 구조가 시각적으로 정상 동작함을 확인.



1. ROS 2 통신 품질 관리: QoS (Quality of Service)ROS 2는 기본 통신 미들웨어로 DDS(Data Distribution Service)를 사용하므로, 네트워크 환경이나 로봇 시스템의 특성에 맞게 데이터 통신 방식을 세밀하게 제어할 수 있는 QoS 정책을 제공합니다.주요 QoS 정책 항목History (기록 정책)KEEP_ALL: 발행되는 모든 데이터를 보관합니다.KEEP_LAST: 설정된 depth 크기만큼의 최신 데이터만 보관합니다.Reliability (신뢰성 정책)RELIABLE: 데이터 수신을 철저히 보장하며 누락을 방지합니다 (데이터 수신 집중).BEST_EFFORT: 데이터 손실 가능성이 있더라도 빠른 전송 속도를 중시합니다.Durability (내구성 정책)TRANSIENT_LOCAL: 구독(Subscription) 생성 이전의 과거 데이터까지 보관하여 전달합니다.VOLATILE: 구독 생성 이전의 데이터는 무효화하고 이후 데이터만 처리합니다.Deadline (마감 시간)정해진 주기 안에 데이터가 정상적으로 수발신되지 않을 경우 EventCallback을 실행합니다.Lifespan (수명)생성된 데이터가 정해진 주기 안에서만 유효하다고 판정하며, 시간이 지나면 폐기합니다.Liveliness (활성 상태)정해진 주기 안에 노드나 토픽이 살아있는지(생사 여부)를 확인합니다.코드 구현 예시 (Python - rclpy) > ```pythonself.qos_profile = QoSProfile(history=QoSHistoryPolicy.KEEP_ALL,reliability=QoSReliabilityPolicy.RELIABLE,durability=QoSDurabilityPolicy.TRANSIENT_LOCAL)센서 데이터 등의 경우 미리 정의된 프리셋인 `qos_profile_sensor_data`를 임포트하여 간편하게 사용할 수도 있습니다.
2. ROS 2의 시간(Time) 체계로봇 시스템에서는 정확한 동기화와 타임스탬프 기록이 필수적입니다. ROS 2는 세 가지 기준의 시간을 지원합니다.ROS_TIME노드가 생성된 시점을 기준으로 하는 시간입니다.시뮬레이션 환경 등에서는 use_sim_time 파라미터를 통해 가상 시간(/clock 토픽 발행)을 사용할 수 있습니다.SYSTEM_TIME시스템(PC 등)의 실제 물리적 시간입니다. 시스템 간 동기화가 안 될 수 있어 sudo ntpdate ntp.ubuntu.com 등을 통한 시간 동기화가 필요할 수 있습니다.STEADY_TIME하드웨어 타임아웃 등을 측정하기 위해 사용하는 시간입니다. 무조건 단조증가(Monotonically increasing)한다는 특성이 있어 시스템 시간이 변경되어도 영향을 받지 않습니다.3. ROS 2 표준 단위 및 좌표계ROS는 데이터 교환 시 혼선을 줄이기 위해 국제단위계(SI Unit)를 표준으로 채택하고 있습니다.SI 단위계길이($m$), 질량($Kg$), 시간($s$), 전류($A$), 평면각($rad$), 주파수($Hz$), 온도($^\circ C$), 전압($V$)좌표계 및 표현 방식오른손 법칙을 따르며, 반시계 방향이 정방향(+)입니다.기본적으로 ENU(East, North, Up) 좌표계를 사용하며, 축은 $x$ (빨강), $y$ (초록), $z$ (파랑)로 표현됩니다.카메라 등 좌표계 표현 방식이 다른 경우 접미사로 _optical, _ned 등을 붙여 구분합니다.회전 표현은 주로 쿼터니언(Quaternion), 회전 매트릭스, 고정축 방식을 사용하며, 특이점(Gimbal lock) 문제가 있는 오일러 각도는 권장하지 않습니다.4. 파라미터(Parameter)와 런치(Launch) 파일다수의 노드와 로봇(예: 터틀심 여러 마리)을 구동할 때는 설정값을 관리하는 파라미터와 이를 일괄 실행하는 런치 시스템이 핵심적인 역할을 담당합니다.네임스페이스(Namespace) 적용 방법동일한 노드를 여러 개 띄울 때 이름 충돌을 방지하기 위해 네임스페이스를 할당합니다.CLI 명령어 방식--ros-args --remap __ns:=/robot1 형태로 실행 시 직접 인자를 전달합니다.Launch 파일 방식    * Python 기반 런치 파일 내에서 Node 객체를 선언할 때 namespace 인자를 직접 지정하거나 환경변수를 활용할 수 있습니다.예시 코드 구조:PythonNode(
    namespace='robot1',
    package='turtlesim',
    executable='turtlesim_node',
    parameters=[param_dir] # 파라미터 파일 경로 연동 가능
)

제공된 교안 및 학습 자료를 바탕으로 ROS 2의 통신 구조와 핵심 통신 방식(메커니즘), 그리고 QoS(서비스 품질) 설정에 대해 체계적으로 정리해 드립니다.

1. ROS 2 통신 아키텍처 및 핵심 구조
ROS 2는 중앙 관리자(roscore)에 의존하던 ROS 1과 달리, DDS(Data Distribution Service) 표준을 미들웨어로 채택하여 분산형 P2P 구조를 가집니다.

API 및 미들웨어 계층 구조
User Code (사용자 애플리케이션): 개발자가 작성하는 노드와 제어 로직

RCL (ROS Client Library): rclcpp(C++), rclpy(Python) 등 언어별 클라이언트 API

RMW (ROS Middleware Interface): 특정 DDS 구현체에 종속되지 않도록 통신 계층을 추상화한 C 기반 표준 인터페이스

DDS Vendor Layer: Fast DDS, Cyclone DDS, Connext DDS 등 실제 네트워크 트래픽과 데이터 전송을 담당하는 엔진

2. ROS 2의 4가지 주요 통신 메커니즘
ROS 2 노드 간 상호작용은 데이터의 성격과 목적에 따라 네 가지 방식으로 나뉩니다.

① 토픽 (Topic) - 단방향 비동기 스트리밍
특징: 퍼블리셔(Publisher)가 데이터를 발행(Publish)하고, 서브스크라이버(Subscriber)가 구독(Subscribe)하는 비동기식 1:N / N:N 다중 통신입니다.

용도: 센서 데이터(LiDAR, 카메라 등)나 로봇의 상태 정보처럼 주기적으로 연속해서 흘러 들어오는 데이터를 전송할 때 사용합니다.

② 서비스 (Service) - 동기식 요청/응답
특징: 클라이언트(Client)가 서버(Server)에 요청(Request)을 보내고, 서버가 처리를 마친 뒤 응답(Response)을 반환하는 동기식 1:1 통신입니다.

용도: 터틀심 스폰 명령어(turtlesim/srv/Spawn)나 펜 색상 변경(turtlesim/srv/SetPen)처럼 일회성 명령 및 결과 확인이 필요할 때 사용합니다.

③ 액션 (Action) - 비동기식 장기 실행 제어
특징: 서비스와 유사하지만, 목표(Goal) 요청, 중간 피드백(Feedback) 수신, 최종 결과(Result) 반환의 구조를 가집니다. 특히 실행 도중 언제든지 명령을 취소(Cancel)할 수 있습니다.

용도: 로봇의 자율 주행(Navigation)이나 로봇 팔(Manipulator) 제어 등 시간이 오래 걸리며 중간 진행 상황 모니터링이 필요한 작업에 적합합니다.

④ 파라미터 (Parameter) - 노드 설정 관리
특징: 노드의 성격이나 동작 속성(값)을 설정하고 변경하는 통신 방식입니다.

용도: 런치 파일이나 CLI 환경에서 노드의 변수 값을 동적으로 주입하거나 변경할 때 사용합니다.

3. 통신 품질 제어: QoS (Quality of Service)
ROS 2는 DDS 기반이므로 네트워크 환경과 로봇의 목적에 맞추어 통신 속도나 신뢰성을 세밀하게 튜닝할 수 있는 QoS 정책을 제공합니다.

History (기록 정책)

KEEP_ALL: 발행되는 모든 데이터를 보관합니다.

KEEP_LAST: 설정된 depth 크기만큼의 최신 데이터만 보관합니다.

Reliability (신뢰성 정책)

RELIABLE: 데이터 유실 없는 정확한 수신에 집중합니다.

BEST_EFFORT: 데이터 손실 가능성이 있더라도 지연 없는 빠른 속도를 중시합니다.

Durability (내구성 정책)

TRANSIENT_LOCAL: 구독(Subscription) 생성 시점에 이미 발행되었던 과거 데이터까지 보관하여 전달합니다.

VOLATILE: 구독 생성 이전의 데이터는 무효화합니다.

Deadline / Lifespan / Liveliness

주기에 따른 데이터 수발신 여부 확인(Deadline), 유효 시간 판정(Lifespan), 노드 및 토픽의 생사 확인(Liveliness)을 수행합니다.