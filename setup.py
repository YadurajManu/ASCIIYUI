from setuptools import setup, find_packages

setup(
    name="asciicam",
    version="1.0.0",
    packages=find_packages(),
    py_modules=["main"],
    install_requires=[
        "opencv-python",
        "numpy",
        "Pillow",
    ],
    entry_points={
        "console_scripts": [
            "asciicam=main:main",
        ],
    },
    author="Yaduraj Singh",
    description="Real-time ASCII Camera in the terminal",
    url="https://github.com/YadurajManu/ASCIIYUI.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
