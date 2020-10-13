from setuptools import setup


setup(
    name="flick",
    version='0.1',
    py_modules=['joints'],
    install_requires=[
        'Click',
        'texttable',
    ],
    entry_points='''
        [console_scripts]
        flick=joints:cli
    ''',
)

