from setuptools import find_packages, setup
setup(
    name="kant",
    packages=find_packages(),
    version="1.0.0",
    description="Knowledge mAnagemeNT",
    author="Miguel Á. González-Santamarta",
    author_email="mgons@unileon.es",
    license="GPL-3.0",
    install_requires=["mongoengine>=0.23.1", "dnspython>=2.0.0"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    test_suite="tests",
)
