"""Redis Let's Encrypt authenticator plugin."""
import logging
import redis

import zope.component
import zope.interface

from acme import challenges

from letsencrypt import errors
from letsencrypt import interfaces
from letsencrypt.plugins import common

logger = logging.getLogger(__name__)

class Authenticator(common.Plugin):
    zope.interface.implements(interfaces.IAuthenticator)
    zope.interface.classProvides(interfaces.IPluginFactory)

    description = "Redis Authenticator"

    @classmethod
    def add_parser_arguments(cls, add):
        add("redis-hosts", default="127.0.0.1",
            help="Redis host to store challenge.")
        add("redis-port", default=6379,
            help="Redis port to store challenge.")
        add("redis-expire", default=120,
            help="Redis expire in seconds for challenge key.")

    def __init__(self, *args, **kwargs):
        super(Authenticator, self).__init__(*args, **kwargs)
        self._httpd = None

    def prepare(self):  # pylint: disable=missing-docstring,no-self-use
        pass  # pragma: no cover

    def more_info(self):  # pylint: disable=missing-docstring,no-self-use
        return ("")

    def get_chall_pref(self, domain):
        # pylint: disable=missing-docstring,no-self-use,unused-argument
        return [challenges.HTTP01]

    def perform(self, achalls):  # pylint: disable=missing-docstring
        responses = []
        for achall in achalls:
            responses.append(self._perform_single(achall))
        return responses

    def _perform_single(self, achall):
        # put challenge file to Redis hosts
        # then run simple http verification
        response, validation = achall.response_and_validation()
        challenge_uri = achall.chall.path[28:]

        for host in self.conf("redis-hosts").split(","):
          r = redis.Redis(host, self.conf("redis-port"))
          r.setex("acme:" + achall.domain + ":" + challenge_uri,
                  validation,
                  self.conf("redis-expire"))

        if response.simple_verify(
                achall.chall, achall.domain,
                achall.account_key.public_key(), self.config.http01_port):
            return response
        else:
            logger.error(
                "Self-verify of challenge failed, authorization abandoned!")
            return None

    def cleanup(self, achalls):  # pylint: disable=missing-docstring,no-self-use,unused-argument
        return None
