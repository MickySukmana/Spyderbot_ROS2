from setuptools import setup

package_name = 'spyderbot_control_node'
submodule = 'spyderbot_control_node/submodule'
setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name, submodule],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vel',
    maintainer_email='hibatullah.mickysukmana@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
                'control = spyderbot_control_node.joint_trajectory_pub:main',
        ],
    },
)
