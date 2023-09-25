#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Integration tests to validate that the Vault ROCK works as expected."""

import logging
import subprocess
import time
import unittest

from vault import Vault

logger = logging.getLogger(__name__)


def wait_for_vault_to_be_available(timeout: int = 30):
    """Wait for Vault to be available."""
    initial_time = time.time()
    vault = Vault("http://localhost:8200")
    while time.time() - initial_time < timeout:
        if vault.is_api_available():
            logger.info("Vault API is available")
            return True
        else:
            time.sleep(1)
    raise TimeoutError("Vault is not available after {} seconds".format(timeout))


class TestVaultRock(unittest.TestCase):
    """Integration tests to validate that the Vault ROCK works as expected."""

    def setUp(self):
        """Starts a Vault container."""
        subprocess.check_call(
            "docker run -d -p 8200:8200 -v ${PWD}/config:/vault/config --entrypoint /bin/bash vault:1.14.3 -c 'vault server -config=/vault/config/config.hcl'",  # noqa: E501
            shell=True,
        )

    def test_given_vault_container_running_when_initialize_then_properly_responds_to_commands(
        self,
    ):
        """Runs basic CLI commands to initialize and unseal Vault."""
        vault = Vault("http://localhost:8200")

        wait_for_vault_to_be_available()

        root_token, unseal_keys = vault.initialize()

        vault.unseal(unseal_keys)

        self.assertEqual(vault.is_initialized(), True)
        self.assertEqual(vault.is_sealed(), False)
