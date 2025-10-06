from setuptools import setup, find_packages

setup(
    name="wordle-cli",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "sqlalchemy>=1.4.0",
        "psycopg2-binary>=2.9.0",
        "rich>=12.0.0",
        "bcrypt>=3.2.0",
        "alembic>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "wordle=main:main",
        ],
    },
)
