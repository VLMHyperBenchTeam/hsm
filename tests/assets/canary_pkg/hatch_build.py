import os
from hatchling.builders.hooks.plugin.interface import BuildHookInterface

class CustomBuildHook(BuildHookInterface):
    def initialize(self, version, build_data):
        # The core of our High-Fidelity test:
        # This package will fail to build if the environment variable is missing.
        if os.getenv("HSM_CANARY_VAR") != "FLYING":
            raise RuntimeError("CANARY_DIED: Environment variable HSM_CANARY_VAR not found or incorrect!")