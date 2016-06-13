from setuptools import setup
from setuptools import find_packages

setup(
    name = 'letsencrypt-redis',
    version = '0.0.1',
    description = 'Add challenge token to Redis',
    packages = find_packages(),
    install_requires = [
        'certbot',
        'redis',
        'pycrypto',
        'zope.interface',
    ],
    entry_points = {
        'certbot.plugins': [
          'auth = letsencrypt_redis.authenticator:Authenticator',
          'installer = letsencrypt_redis.installer:Installer'
        ]
    }
)
