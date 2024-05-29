#!/usr/bin/env python3
# Copyright 2023 Canonical Ltd.
# See LICENSE file for licensing details.

"""Contains all the specificities to communicate with Vault through its API."""

import logging
from typing import List, Tuple

import hvac  # type: ignore[import]
import requests  # type: ignore[import]

logger = logging.getLogger(__name__)


class Vault:
    """Class to interact with Vault through its API."""

    def __init__(self, url: str):
        """Initialize Vault CLI client."""
        self._client = hvac.Client(url=url, verify=False)

    def initialize(
        self, secret_shares: int = 1, secret_threshold: int = 1
    ) -> Tuple[str, List[str]]:
        """Initialize Vault.

        Returns:
            A tuple containing the root token and the unseal keys.
        """
        initialize_response = self._client.sys.initialize(
            secret_shares=secret_shares, secret_threshold=secret_threshold
        )
        logger.info("Vault is initialized")
        return initialize_response["root_token"], initialize_response["keys"]

    def is_initialized(self) -> bool:
        """Return whether Vault is initialized."""
        return self._client.sys.is_initialized()

    def is_sealed(self) -> bool:
        """Return whether Vault is sealed."""
        return self._client.sys.is_sealed()

    def unseal(self, unseal_keys: List[str]) -> None:
        """Unseal Vault."""
        for unseal_key in unseal_keys:
            self._client.sys.submit_unseal_key(unseal_key)
        logger.info("Vault is unsealed")

    def is_api_available(self) -> bool:
        """Return whether Vault is available."""
        self._client.sys.read_health_status()
        try:
            self._client.sys.read_health_status()
        except requests.exceptions.ConnectionError:
            return False
        return True

    def set_token(self, token: str) -> None:
        """Set the Vault token for authentication."""
        self._client.token = token
