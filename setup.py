from setuptools import setup, find_packages

setup(
    name="treasure_hoard",
    author="mattdoug604",
    author_email="mattdoug604@gmail.com",
    packages=find_packages(),
    description="Generate a treasure hoard for D&D 5e.",
    python_requires=">=3.4",
    install_requires=["pandas", "xlrd"],
    include_package_data=True,
    entry_points={"console_scripts": ["treasure-hoard=treasure_hoard.__main__:main"]},
)
