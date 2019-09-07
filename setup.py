from setuptools import setup, find_namespace_packages

setup(
    name='courier_snap',
    version='0.1',
    description='Snap your couriers!',
    author='LolitoDevs',
    packages=find_namespace_packages(include=['courier_snap.*']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Topic :: Utilities'
    ],
    install_requires=[
        'attrs',
        'numpy',
        'matplotlib'
    ],
    zip_safe=True,
    python_requires='>=3.6',
)
