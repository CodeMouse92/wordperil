import setuptools


setuptools.setup(
    name="wordperil",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    entry_points={
        'gui_scripts': [
            'main = peril.main:main',
        ],
    },
    install_requires=[
        'pyside2',
        'appdirs'
    ],
)
