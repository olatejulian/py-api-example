from typing import Any, Generic, TypeVar

from pydantic.generics import GenericModel

HTTPResponseDataType = TypeVar("HTTPResponseDataType")  # pylint: disable=invalid-name


# pylint: disable=too-few-public-methods, dangerous-default-value
class SchemaExtraConfig:
    schema_extra = {
        "example": {
            "status_code": 200,
            "message": "Response message",
            "data": {},
        },
    }

    @classmethod
    def override_schema_extra_example(
        cls,
        status_code: int | None = None,
        data: dict[str, str] = {},
        message: str | None = None,
    ) -> dict[str, Any]:
        override_schema_extra_example = {
            "status_code": status_code,
            "message": message,
            "data": data,
        }

        schema_extra_example = {}

        for key, value in cls.schema_extra["example"].items():
            schema_extra_example[key] = override_schema_extra_example[key] or value

        schema_extra = cls.schema_extra.copy()

        schema_extra["example"] = schema_extra_example

        return schema_extra


class APIResponse(GenericModel, Generic[HTTPResponseDataType]):
    status_code: int
    message: str
    data: dict[str, Any] | HTTPResponseDataType = {}

    class Config:
        schema_extra = SchemaExtraConfig.schema_extra
