import re
from pathlib import Path
from typing import List

from setuptools import find_namespace_packages, setup


def get_version(package: str) -> str:
    """
    Extract package version, located in the `src/package/__version__.py`.
    """
    version = Path("src", package, "__version__.py").read_text()
    pattern = r"__version__ = ['\"]([^'\"]+)['\"]"
    return re.match(pattern, version).group(1)  # type: ignore


def get_requirements(req_file: str) -> List[str]:
    """
    Extract requirements from provided file.
    """
    req_path = Path(req_file)
    requirements = req_path.read_text().split("\n") if req_path.exists() else []
    return requirements


def get_long_description(readme_file: str) -> str:
    """
    Extract README from provided file.
    """
    readme_path = Path(readme_file)
    long_description = (
        readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    )
    return long_description


AEDIFICATOR_DUMMY_TEXT = "Built by aedificator. Fill in manually."


setup(
    name="anyiotools",
    version=get_version("anyiotools"),
    description=AEDIFICATOR_DUMMY_TEXT,
    long_description=get_long_description("README.md"),
    long_description_content_type="text/markdown",
    author=AEDIFICATOR_DUMMY_TEXT,
    author_email=AEDIFICATOR_DUMMY_TEXT,
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src"),
    install_requires=get_requirements("requirements.txt"),
    extras_require={"dev": get_requirements("dev-requirements.txt")},
)
