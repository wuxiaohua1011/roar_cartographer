import os
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

# tutorial based on https://fishros.com/d2lros2/#/chapt10/10.5%E9%85%8D%E7%BD%AEFishbot%E8%BF%9B%E8%A1%8C%E5%BB%BA%E5%9B%BE
def generate_launch_description():
    # 定位到功能包的地址
    pkg_share = FindPackageShare(package="roar_cartographer").find("roar_cartographer")

    # =====================运行节点需要的配置=======================================================================
    # 是否使用仿真时间，我们用gazebo，这里设置成true
    use_sim_time = LaunchConfiguration("use_sim_time", default="true")
    # 地图的分辨率
    resolution = LaunchConfiguration("resolution", default="0.05")
    # 地图的发布周期
    publish_period_sec = LaunchConfiguration("publish_period_sec", default="1.0")
    # 配置文件夹路径
    configuration_directory = LaunchConfiguration(
        "configuration_directory", default=os.path.join(pkg_share, "config")
    )
    # 配置文件
    configuration_basename = LaunchConfiguration(
        "configuration_basename", default="roar_bot_2d.lua"
    )

    # =====================声明三个节点，cartographer/occupancy_grid_node=================================
    cartographer_node = Node(
        package="cartographer_ros",
        executable="cartographer_node",
        name="cartographer_node",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
        arguments=[
            "-configuration_directory",
            configuration_directory,
            "-configuration_basename",
            configuration_basename,
        ],
        remappings=[
            ("points2", "/carla/ego_vehicle/center_lidar"),
            ("imu", "/carla/ego_vehicle/imu"),
            ("odom", "/carla/ego_vehicle/odometry"),
        ],
    )

    occupancy_grid_node = Node(
        package="cartographer_ros",
        executable="occupancy_grid_node",
        name="occupancy_grid_node",
        output="screen",
        parameters=[{"use_sim_time": use_sim_time}],
        arguments=[
            "-resolution",
            resolution,
            "-publish_period_sec",
            publish_period_sec,
        ],
    )

    # ===============================================定义启动文件========================================================
    ld = LaunchDescription()
    ld.add_action(cartographer_node)
    ld.add_action(occupancy_grid_node)

    return ld
