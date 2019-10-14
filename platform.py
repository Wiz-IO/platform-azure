from platform import system
from platformio.managers.platform import PlatformBase

class AzurePlatform(PlatformBase):
    def configure_default_packages(self, variables, targets):
        framework = variables.get("pioframework", [])
        if "arduino" in framework or "linux" in framework:
            del self.packages["toolchain-gccarmnoneeabi"]
        else:
            del self.packages["toolchain-arm-poky-linux-musleabi-hf"]

        return PlatformBase.configure_default_packages(self, variables, targets)
            