from setuptools import find_packages, setup

setup(
    name="Skaak",
    packages=find_packages(include=["skaak"]),
    version="0.12.5",
    description="A Python Chess Library",
    author="George Munyoro",
    license="MIT",
    install_requires=[],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==6.1.1"],
    test_suite="tests",
)
