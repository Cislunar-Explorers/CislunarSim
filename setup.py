from distutils.core import setup

setup(
    name="cislunar-sim",
    version="0.1",
    author="SSDS",
    author_email="tmf97@cornell.edu",
    description="HOOTL simulator for the Cislunar Explorers missions",
    install_requires=["numpy", "matplotlib", "pytest", "scipy", "astropy", "pandas", "jsonschema", "python-dotenv", "sqlalchemy", "psutil", "bitstring","numba","numpy-quaternion","opencv-python-headless","opencv-python","pyquaternion","tqdm","uptime","parameterized","Adafruit-Blinka","adafruit-circuitpython-busdevic","adafruit-circuitpython-ds3231","adafruit-circuitpython-fxas21002c","adafruit-circuitpython-fxos8700","ADS1115","pigpio"],
    package_dir={"": "src"},
)
