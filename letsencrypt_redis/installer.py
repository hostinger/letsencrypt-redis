"""Redis Let's Encrypt installer plugin."""
import logging
import redis
import ssl
import subprocess

import zope.component
import zope.interface

from letsencrypt import errors
from letsencrypt import interfaces
from letsencrypt.plugins import common

logger = logging.getLogger(__name__)

class Installer(common.Plugin):
    zope.interface.implements(interfaces.IInstaller)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "Redis Installer"

    @classmethod
    def add_parser_arguments(cls, add):
        add("redis-hosts", default="127.0.0.1",
            help="Redis host to store key/cert pair.")
        add("redis-port", default=6379,
            help="Redis port to store key/cert pair.")

    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ("")

    def get_all_names(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def deploy_cert(self, domain, cert_path, key_path, chain_path, fullchain_path=None):
        # put key/cert to Redis hosts as binary (DER)
        def private_to_der(key_path):
            command = "openssl rsa -in %s -outform DER" % key_path
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            return p.communicate()[0]

        key = private_to_der(key_path)
        cert = ssl.PEM_cert_to_DER_cert(open(cert_path).read())

        values = {
            "key": key,
            "cert": cert
        }

        for host in self.conf("redis-hosts").split(","):
          r = redis.Redis(host, self.conf("redis-port"))
          r.hmset("ssl:" + domain, values)

    def enhance(self, domain, enhancement, options=None):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def supported_enhancements(self):  # pylint: disable=missing-docstring,no-self-use
        return []  # pragma: no cover

    def get_all_certs_keys(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def save(self, title=None, temporary=False):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def rollback_checkpoints(self, rollback=1):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def recovery_routine(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def view_config_changes(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def config_test(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def restart(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover
