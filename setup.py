from setuptools import setup

setup(
    name="btcreport",
    version="0.0.1",
    py_modules=["btcreport"],
    entry_points={
        "console_scripts":[
            "btcreport=btcreport:main"
        ]
    }
)