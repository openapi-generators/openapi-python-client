import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="{{ project_name }}",
    version="{{ version }}",
    description="{{ description }}",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir={"": "{{ package_name }}"},
    packages=find_packages(where="{{ package_name }}"),
    python_requires=">=3.6, <4",
    install_requires=["httpx >= 0.15.0, < 0.17.0", "attrs >= 20.1.0", "python-dateutil >= 2.8.1, < 3"],
    package_data={"": ["CHANGELOG.md"], "{{ package_name }}": ["py.typed"]},
)
