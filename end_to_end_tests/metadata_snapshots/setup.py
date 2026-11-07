import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="test-3-1-features-client",
    version="0.1.0",
    description="A client library for accessing Test 3.1 Features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.11, <4",
    install_requires=["httpx2 >= 2.13.1, < 3", "attrs >= 22.2.0"],
    package_data={"test_3_1_features_client": ["py.typed"]},
)
