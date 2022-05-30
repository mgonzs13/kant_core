from setuptools import find_packages, setup
setup(
    name="kant",
    packages=find_packages(include=["kant"]),
    version="0.1.0",
    description="Knowledge mAnagemeNT for PDDL",
    author="Miguel Á. González-Santamarta",
    license="GPL-3.0",
    install_requires=["mongoengine==0.23.1", "dnspython==2.0.0"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.0.2"],
    test_suite="tests",
)
