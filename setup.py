from setuptools import setup

setup(
    name="btcreport",
    version="0.1.0",
    py_modules=["btcreport"],
    install_requires=[
        "btcget==0.0.*",
        "prettytable==3.9.0"
    ],
    entry_points={
        "console_scripts":[
            "btcreport=btcreport:main"
        ]
    }
)