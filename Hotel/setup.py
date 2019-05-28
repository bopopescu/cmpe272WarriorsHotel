import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='hotel',
    version='1.0.0',
    url='https://github.com/YuvaAthur/cmpe272WarriorsHotel',
    maintainer='CMPE 272 Spring - Warriors team',
    maintainer_email='yuva.athur@sjsu.edu',
    description='Hotel rooms browser built in the Flask tutorial.',
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    extras_require={
        'test': [
            'pytest',
            'coverage',
        ],
    },
)