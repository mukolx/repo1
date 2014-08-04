from distutils.core import setup

setup(
    name='simple_lis2d_utils',
    version='0.1.1',
    author='Micah Mukolwe',
    author_email='mukolx@mail.com',
    packages=['lis_utils'],
    license='LICENSE.txt',
    description='Python utililites to manipulate LISFLOOD-FP model files and results.',
    long_description=open('README.txt').read(),
    install_requires=[
        "scipy",
        "numpy",
        "gdal",
        "matplotlib",
    ],
)
