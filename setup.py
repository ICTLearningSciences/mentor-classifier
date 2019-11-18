from setuptools import setup, find_packages

# from os import path

# from m2r import parse_from_file

# import behave_restful.about as about

# readme_file = path.join(path.dirname(path.abspath(__file__)), 'README.md')
readme = "TEMP README"  # parse_from_file(readme_file)


def _read_dependencies():
    requirements_file = "requirements.txt"
    with open(requirements_file) as fin:
        return [line.strip() for line in fin if line]


packages = find_packages()
requirements = _read_dependencies()

setup(
    name="mentor-classifiers",
    version="1.0.0",
    author_email="larrykirschner@gmail.com",
    description="core classifier code for mentor",
    packages=packages,
    install_requires=requirements,
)
