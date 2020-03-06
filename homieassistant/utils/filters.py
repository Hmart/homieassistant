from django.utils.encoding import force_text
from rest_framework.compat import coreapi, coreschema
from rest_framework.filters import OrderingFilter


class ExtendedOrderingFilter(OrderingFilter):
    def get_schema_fields(self, view):
        assert (
            coreapi is not None
        ), "coreapi must be installed to use `get_schema_fields()`"
        assert (
            coreschema is not None
        ), "coreschema must be installed to use `get_schema_fields()`"

        # If fields are stated explicitly then add them to API Field description
        valid_fields = getattr(view, "ordering_fields", self.ordering_fields)
        if valid_fields is not None and valid_fields != "__all__":
            description = "{ordering_description} Available fields: {fields}".format(
                ordering_description=self.ordering_description,
                fields=" ".join(["`" + field + "`" for field in valid_fields]),
            )
        else:
            description = self.ordering_description

        return [
            coreapi.Field(
                name=self.ordering_param,
                required=False,
                location="query",
                schema=coreschema.String(
                    title=force_text(self.ordering_title),
                    description=force_text(description),
                ),
            )
        ]
