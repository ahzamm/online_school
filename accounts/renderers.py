import json

from rest_framework import renderers


class UserRender(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None,
               renderer_contex=None):

        # If word "ErrorDetail" is presented in message then append "error" in
        # message to better differentiate error messages
        response = json.dumps({'errors': data}) \
            if 'ErrorDetail' in str(data) \
            else json.dumps(data)

        return response
