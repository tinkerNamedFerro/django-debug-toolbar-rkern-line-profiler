from setuptools import setup, find_packages


setup(
    name='django-debug-toolbar-rkern-line-profiler',
    description='Django Debug Toolbar Line Profile Panel (rkern)',
    version='0.0.1',
    url='https://github.com/peergradeio/django-debug-toolbar-rkern-line-profiler',
    author='Malthe Jørgensen',
    author_email='malthe.jorgensen@gmail.com',
    long_description=open('README.md').read(),
    license='MIT',
    packages=find_packages(exclude=('tests', 'example')),
    include_package_data=True,
    install_requires=['django-debug-toolbar>=1.0', 'line-profiler>=2.0'],
)
