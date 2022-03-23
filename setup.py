from distutils.core import setup

setup(
    name="cislunar-sim",
    version=0.1,
    author="SSDS",
    description="HOOTL simulator for the Cislunar Explorers missions",
    install_requires=["numpy", "matplotlib", "pytest", "scipy"],
    package_dir={"": "src"},
)
