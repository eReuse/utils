from setuptools import find_packages, setup

setup(
    name="eReuse-Utils",
    version='0.1',
    packages=find_packages(),
    url='https://github.com/eReuse/utils',
    license='AGPLv3 License',
    author='eReuse.org team',
    description='Common functionality for eReuse.org software',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: System :: Logging',
        'Topic :: Utilities',
    ],
)
