import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
readme = open(os.path.join(here, 'README.rst')).read()

requires = [
        'tahrir-api',
        'flask'
        ]

setup(
    version='0.1.0',
    description='A webapp which exposes a restful api for tahrir',
    long_description=readme,
    license='AGPLv3+',
    classifiers=[
        "programming Language :: Python",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
    ],
    author="Ross Delinger",
    author_email="rossdylan@csh.rit.edu",
    url="https://github.com/rossdylan/tahrir-rest",
    packages = ["tahrir_rest",],
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points="""
    [paster.app_factory]
    main = tahrir_rest:main
    """
    )
