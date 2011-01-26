from distutils.core import setup 
setup(
    name = "django-banklink",
    packages = ["django_banklink"],
    version = "0.14",
    description = "django application for Swedbank payment gateway",
    author = "Kristaps Kulis",
    author_email = "kristaps@true-vision.net",
    url = "http://www.github.com/truevision/django_banklink",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Topic :: Office/Business :: Financial',
    ],
    requires = ['M2Crypto (>=0.20)'], 
    )
