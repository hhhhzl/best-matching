import setuptools
setuptools.setup(
    name="assignmentproblem",
    version='0.0.1',
    author="HectorHe",
    author_email="zhilinhe@usc.edu",
    entry_points={
        'console_scripts': [
            'manager = manager:main',
        ]
    },
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=[],
    package_data={"": ["*.py", "*.json", "*.pk", "*.js"]},
    python_requires=">=3.7",
)
