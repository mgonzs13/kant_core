from kant.kant_dto import *


# location
location = TypeDto("location")

pose_x = FluentDto("pose_x", [location], is_numeric=True)
pose_y = FluentDto("pose_y", [location], is_numeric=True)
pose_z = FluentDto("pose_z", [location], is_numeric=True)

quaternion_x = FluentDto("quaternion_x", [location], is_numeric=True)
quaternion_y = FluentDto("quaternion_y", [location], is_numeric=True)
quaternion_z = FluentDto("quaternion_z", [location], is_numeric=True)
quaternion_w = FluentDto("quaternion_w", [location], is_numeric=True)


# robot
robot = TypeDto("robot")
robot_at = FluentDto("robot_at", [robot, location])
