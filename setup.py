from setuptools import setup, find_packages

setup(
    name="sales_fusion",
    version="1.0.0",
    description="Sales-Fusion Agentic AI Analytics Platform",
    author="Umar Saddiq Ahmed Ali Sayyed",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "prophet",
        "xgboost",
        "scikit-learn",
        "streamlit",
        "fastapi",
        "plotly"
    ],
)
