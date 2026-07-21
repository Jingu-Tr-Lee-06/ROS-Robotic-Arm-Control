ROS-Robotic-Arm-Control2026 Academic Year Robotic Arm Control Project (KNU, Com-Edu, LJH)July 20, 2026💻 PART 1. Local Development Environment Setup (WSL2 & VS Code & Git)1. WSL2 (Ubuntu 24.04 LTS) Installation & Virtualization OptimizationWindows Subsystem for Linux 2 (WSL2) provides a full Linux environment directly on top of the Windows kernel.Run PowerShell (as Administrator) and enter the command below to explicitly install Ubuntu 24.04:PowerShellwsl --install -d Ubuntu-24.04
If a system reboot is requested, restart your PC.After rebooting, register your user credentials in the virtual terminal that opens automatically:Username: Linux username (all lowercase, no spaces recommended)Password: Password for administrator privileges (sudo) (will not be displayed on screen while typing)💡 Essential WSL2 Tip (Memory Limit)By default, WSL2 can consume up to 80% of host Windows RAM, which may slow down the system. It is recommended to create a .wslconfig file in your Windows user directory (C:\Users\<Username>\) with the following content to limit resource allocation:Ini, TOML[wsl2]
memory=8GB # Recommended: ~50% of total RAM
processors=4
2. GitHub Repository Integration & Git Global ConfigurationConfigure global Git variables for code versioning and remote backup, then set up SSH or HTTPS authentication.Bash# Set global Git user information
git config --global user.name "Your GitHub Name"
git config --global user.email "your_email@example.com"

# Verify settings
git config --list
Create a new repository named ros2_workspace on GitHub, then return to the WSL terminal and clone it:Bash# Navigate to home directory and clone workspace
cd ~
git clone https://github.com/your-username/ros2_workspace.git
cd ros2_workspace
3. VS Code & WSL Remote Development IntegrationSeamlessly integrate VS Code installed on Windows with the Linux file system inside WSL2 to maximize development efficiency.Open the Extensions Marketplace (Ctrl + Shift + X) in Windows VS Code and install the WSL (Microsoft) extension.In the WSL Ubuntu terminal, execute the following command inside your project directory to open Windows VS Code targeting the virtual environment:Bashcode .
Initial Commit & Push Guide: Open the integrated terminal (Ctrl + ~) in VS Code to commit and push your initial code:Bash# Stage changes and commit
git add .
git commit -m "Feat: Initial commit with ROS2 setup environment"

# Push to main branch
git push origin main
🤖 PART 2. Complete ROS 2 Jazzy Jalisco Installation (Ubuntu 24.04 LTS)ROS 2 Jazzy Jalisco officially supports Ubuntu 24.04 Noble Numbat as a primary tier. Execute the commands in order to prevent broken APT package manager dependencies.1. System Locale & Encoding ConfigurationROS 2 requires UTF-8 encoding; otherwise, unexpected errors may occur in inter-node communication. Enforce locale synchronization in advance:Bashsudo apt update && sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8

# Apply immediately to current shell session
export LANG=en_US.UTF-8
2. ROS 2 Official APT Repository & GPG Key RegistrationRegister Open Robotics' official package repository into the system:Bash# Enable dependency packages and Universe repository
sudo apt install software-properties-common -y
sudo add-apt-repository universe -y

# Download and save ROS 2 GPG Key for APT security
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# Add ROS 2 official package source list
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
3. ROS 2 Desktop Package & Build Toolchain InstallationBash# Refresh repository list and upgrade existing packages
sudo apt update
sudo apt upgrade -y

# Install ROS 2 full desktop package (core layer, GUI, simulation)
sudo apt install ros-jazzy-desktop -y

# Install development toolchain: compilers, build tools (colcon), dependency manager (rosdep)
sudo apt install ros-dev-tools -y
4. Automatic Shell Environment Setup (~/.bashrc)Add the setup script to .bashrc so that ROS 2 environment variables are automatically sourced every time a new terminal session is opened:Bash# Add environment setup script
echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

# Source immediately in current shell
source ~/.bashrc
🐢 PART 3. ROS 2 Core Concepts & Advanced CLI PracticeThe communication paradigms in ROS 2 are divided into Nodes, Topics, Services, Actions, and Parameters. Practice advanced CLI commands using the turtlesim package.1. Running Turtlesim & Node Namespace RemappingBash# [Terminal 1] Launch graphical simulator node
ros2 run turtlesim turtlesim_node

# [Terminal 2] Launch keyboard teleoperation control node
ros2 run turtlesim turtle_teleop_key
💡 Advanced: Importance of RemappingIn real-world applications, launching multiple identical sensors or robots without remapping causes node name collisions and communication conflicts. The remapping technique changes node names at runtime to isolate execution.Bash# Assign a custom node name for isolated execution
ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle
2. Advanced Node & Topic Status TrackingA. Node Infrastructure InspectionBash# List all active nodes in the computation graph
ros2 node list

# Inspect detailed architecture (publishers, subscribers, services, actions) of a specific node
ros2 node info /turtlesim
B. Topic Data Stream AnalysisBash# List active topics along with their message types (-t)
ros2 topic list -t

# Stream published topic data packets in real-time (e.g., current position X, Y, and theta)
ros2 topic echo /turtle1/pose

# Measure topic publishing frequency (Hz) to detect communication bottlenecks
ros2 topic hz /turtle1/pose
C. One-Time Data Publishing via CLIInject raw message payloads directly into a topic channel to test node responsiveness:Bash# --once option: Publish once and exit / Move turtle forward along X-axis by 1.0 unit
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"
3. Synchronous Service CallsUnlike topics (asynchronous streaming), services operate on a synchronous Request-Response communication mechanism.Bash# Synchronously call service to spawn a new turtle at (x=2.0, y=2.0, theta=0.2)
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.2, name: 'turtle2'}"

# Call service to clear background trajectories
ros2 service call /clear std_srvs/srv/Empty
4. Parameter Runtime Control & Backup (Dump / Load)Parameters allow updating global variables inside a node dynamically at runtime. Practice modifying simulator background colors (RGB):A. Runtime Parameter Modification & Rendering RefreshBash# 1. Retrieve parameter list of target node
ros2 param list

# 2. Get current value of background_g
ros2 param get /turtlesim background_g

# 3. Modify parameters at runtime (Change RGB values for a dark navy background)
ros2 param set /turtlesim background_r 30
ros2 param set /turtlesim background_g 30
ros2 param set /turtlesim background_b 35

# 4. Request screen refresh via service call
ros2 service call /clear std_srvs/srv/Empty
B. Parameter Dumping & Runtime Injection (Loading)Used in production environments to persist tuned sensor calibrations or PID gains into YAML configuration files and reload them later.Bash# Export all current node parameters into a YAML file
ros2 param dump /turtlesim > ./turtlesim.yaml

# Batch-load parameter settings from a file into a running node
ros2 param load /turtlesim ./turtlesim.yaml

# [Key Command] Launch node with pre-loaded parameter profile from file start-up
ros2 run turtlesim turtlesim_node --ros-args --params-file ./turtlesim.yaml
5. GUI Visualization & Network Monitoring Tool (RQT)RQT is a Qt-based framework used to inspect ROS 2 communication interfaces and monitor computation graphs.Bash# Launch RQT main GUI container
rqt

# Visualize current node communication flow (Publisher-Subscriber graph)
rqt_graph
🛠️ PART 4. Troubleshooting Guideros2: command not found ErrorCause: ROS 2 environment setup script is not sourced in current terminal shell.Solution: Run source /opt/ros/jazzy/setup.bash or verify its inclusion at the bottom of ~/.bashrc.GUI Window (rqt or turtlesim_node) Fails to Render in WSL2Cause: X11 display forwarding or WSLg graphics backend communication issue between WSL2 and Windows host.Solution: Verify echo $DISPLAY is non-empty. If unresolved, run wsl --shutdown in PowerShell and restart WSL2. (Windows 11 natively includes WSLg).July 21, 2026📑 ROS 2 Development & Troubleshooting Comprehensive Report1. ROS 2 Environment & Tool Troubleshooting① Resolving rqt Dock/GUI Unresponsive Detachment IssueSymptom: During rqt execution, plugin panels (e.g., Topic Monitor/Publisher) detach into separate floating windows and become unresponsive to drag or click actions.Cause: Corrupted rqt layout configurations and GUI cache files.Solution:Bash# 1. Terminate running rqt instances
killall rqt

# 2. Remove configuration cache folders (or run rqt --clear-config)
rm -rf ~/.config/ros.org/rqt* ~/.ros/rqt_gui*
② Executable Recognition Error (No executable found)Symptom: Executing ros2 run gong_basic move_turtle returns an error stating the executable cannot be found.Inspection & Fix:Verify workspace build and environment setup sourcing:Bashcolcon build
source install/setup.bash
Check if the script path is properly registered under entry_points in setup.py:Python'console_scripts': [
    'move_turtle = gong_basic.move_turtle:main',
],
2. Python Node Development & Package Refactoring① setup.py Package Configuration OptimizationRoot Cause: Incorrectly importing message modules (e.g., from geometry_msgs.msg import Twist) inside setup.py, leading to build failures.Refactoring: Remove message imports from setup.py, leaving only package metadata and build configurations.Launch File Copy Path Fix (Typo Correction):Fixed typo lunch $\rightarrow$ launch in data_files target path:Python(os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
② Base Node Architecture & Exception HandlingMandatory super().__init__('node_name'):When inheriting from Node, omitting the parent class initializer skips ROS 2 internal communication infrastructure setup, leading to runtime errors.Graceful Ctrl + C (SIGINT) Shutdown Handling:To prevent publisher's context is invalid warnings and duplicate shutdown exceptions (RCLError) when invoking loggers during rclpy.shutdown():Pythontry:
    rclpy.spin(node)
except KeyboardInterrupt:
    print("Node terminated by user.")  # Use print() instead of logger during shutdown
finally:
    if rclpy.ok():
        rclpy.shutdown()
③ ROS 2 Message Types & Timer Rate ConfigurationMessage Type Selection:std_msgs.msg.String: Pure text transmission (no frame_id or stamp).std_msgs.msg.Header: Used when timestamp (stamp) and reference frame (frame_id) are required.geometry_msgs.msg.Twist: Defines linear and angular velocities for robot motion control.Timer Control: Adjusted timer period from 1.0s to 0.1s to publish messages at 10 Hz.3. Turtlesim Geometric Spirograph Pattern ControlGoal: Implement complex and smooth mathematical spiral trajectories using trigonometric functions.Core Logic:Keep linear.x constant in geometry_msgs.msg.Twist while periodically oscillating angular.z using math.cos().Achieved a smooth, continuous inward/outward looping Spirograph pattern on screen.4. Multi-Node / Topic Topology & Launch Remapping① Topic & Node Topology1:N Communication: /massage topic is published by mpub and simultaneously received by 3 subscribers: msub, m2sub, and mtsub.Multi-Subscription: Node mtsub subscribes to both /massage and /header topics simultaneously.                  ┌─────────┐
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
② Remapping via multi_node.launch.pyDynamically rename nodes at launch time using the name attribute without modifying node source code:Pythonfrom launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1:N Publisher and Subscribers
        Node(package='gong_basic', executable='class_pub', name='mpub'),
        Node(package='gong_basic', executable='class_sub', name='msub'),
        Node(package='gong_basic', executable='class_sub', name='m2sub'),
        
        # Header Publisher and Multi-subscriber
        Node(package='gong_basic', executable='header_pub', name='tpub'),
        Node(package='gong_basic', executable='mtsub_node', name='mtsub'),
    ])
Verification: Verified topic branching (1:N) and multi-subscription structures visually using ros2 run rqt_graph rqt_graph.