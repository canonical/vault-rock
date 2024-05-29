#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Integration tests to validate that the Vault ROCK works as expected."""

import logging
import subprocess
import time
import requests
import pytest


from vault import Vault

logger = logging.getLogger(__name__)


def wait_for_vault_to_be_available(timeout: int = 30) -> None:
    """Wait for Vault to be available."""
    initial_time = time.time()
    vault = Vault("http://localhost:8200")
    while time.time() - initial_time < timeout:
        try:
            if vault.is_api_available():
                logger.info("Vault API is available")
                return
        except Exception:
            pass
        time.sleep(1)
    raise TimeoutError("Vault is not available after {} seconds".format(timeout))


@pytest.fixture(scope="module")
def run_container():
    """Starts a Vault container."""
    subprocess.check_call(
        "docker run -d -p 8200:8200 vault-rock:test",
        shell=True,
    )


def test_given_vault_container_running_when_ui_is_enabled_then_ui_is_available(run_container):
    """Validate that UI is available."""
    wait_for_vault_to_be_available()
    response = requests.get("http://localhost:8200/ui/vault/init")

    assert response.status_code == 200
    assert "Vault UI is not available in this binary." not in response.text  # This is the message when UI is disabled  # noqa: E501
    assert "vault/config/environment" in response.text  # This is a common element in the UI


def test_given_vault_container_running_when_initialize_then_properly_responds_to_commands(
    run_container
):
    """Runs basic CLI commands to initialize and unseal Vault."""
    vault = Vault("http://localhost:8200")

    wait_for_vault_to_be_available()

    _, unseal_keys = vault.initialize()

    vault.unseal(unseal_keys)

    assert vault.is_initialized()
    assert not vault.is_sealed()
