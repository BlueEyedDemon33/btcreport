from setuptools import setup
from btcreport import __version__

setup(
    name="btcreport",
    version=__version__,
    py_modules=["btcreport"],
    entry_points={
        "console_scripts":[
            "btcreport=btcreport:main"
        ]
    }
)