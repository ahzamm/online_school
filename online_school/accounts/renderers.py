import json

from rest_framework import renderers


class UserRender(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_type=None, renderer_contex=None):

        return (
            json.dumps({"errors": data})
            if "ErrorDetail" in str(data)
            else json.dumps(data)
        )
