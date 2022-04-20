from distutils.core import setup

setup(
    name="cislunar-sim",
    version="0.1",
    author="SSDS",
    author_email="tmf97@cornell.edu",
    description="HOOTL simulator for the Cislunar Explorers missions",
    install_requires=["numpy", "matplotlib", "pytest", "scipy", "astropy", "pandas"],
    package_dir={"": "src"},
)
