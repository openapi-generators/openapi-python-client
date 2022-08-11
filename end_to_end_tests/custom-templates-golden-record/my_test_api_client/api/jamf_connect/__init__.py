""" Contains methods for accessing the API Endpoints """

import types

from . import get_v1_jamf_connect_history


class JamfConnectEndpoints:
    @classmethod
    def get_v1_jamf_connect_history(cls) -> types.ModuleType:
        """
        Get Jamf Connect history

        """
        return get_v1_jamf_connect_history
