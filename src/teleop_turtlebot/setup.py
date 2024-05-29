from setuptools import setup

package_name = 'teleop_turtlebot'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    py_modules=[
        'teleop_turtlebot.teleop_node'
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Seu Nome',
    maintainer_email='seu_email@exemplo.com',
    description='Pacote de teleoperação para TurtleBot3 usando ROS2',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'teleop_node = teleop_turtlebot.teleop_node:main'
        ],
    },
)
