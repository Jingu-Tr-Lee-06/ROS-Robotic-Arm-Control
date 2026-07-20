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