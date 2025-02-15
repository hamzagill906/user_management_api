from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.inspectors.base import call_view_method
from drf_yasg import openapi
class CustomAutoSchema(SwaggerAutoSchema):
    def get_view_response_serializer(self):
        return call_view_method(self.view, 'get_serializer')

    def get_view_serializer(self):
        if call_view_method(self.view, 'get_serializer_create'):
            return call_view_method(self.view, 'get_serializer_create')
        return call_view_method(self.view, 'get_serializer')

    def get_view_query_serializer(self):
        return call_view_method(self.view, 'get_query_serializer')

    def get_default_response_serializer(self):
        body_override = self._get_request_body_override()
        if body_override and body_override is not openapi.Schema.EMPTY:
            return body_override

        return self.get_view_response_serializer()

    def get_query_serializer(self):
        if self.overrides.get('query_serializer', None) is None:
            self.overrides['query_serializer'] = self.get_view_query_serializer()
        return super(CustomAutoSchema, self).get_query_serializer()