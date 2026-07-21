"""数据模型通用能力。"""

from dataclasses import fields
from typing import Any, Dict, Type, TypeVar


ModelT = TypeVar("ModelT", bound="ForwardCompatibleModel")


class ForwardCompatibleModel:
    """允许 API 响应包含 SDK 尚未声明的字段。"""

    extra_fields: Dict[str, Any]

    @classmethod
    def from_dict(cls: Type[ModelT], data: Dict[str, Any]) -> ModelT:
        """从字典构造模型，并保留未声明字段。"""
        known_field_names = {item.name for item in fields(cls)}
        known_data = {
            key: value for key, value in data.items() if key in known_field_names
        }
        extra_data = {
            key: value for key, value in data.items() if key not in known_field_names
        }
        instance = cls(**known_data)
        object.__setattr__(instance, "extra_fields", extra_data)
        return instance

    def __getattr__(self, name: str) -> Any:
        """允许通过属性方式读取 API 新增但 SDK 尚未声明的字段。"""
        extra_fields = self.__dict__.get("extra_fields", {})
        if name in extra_fields:
            return extra_fields[name]
        raise AttributeError(
            f"{type(self).__name__!s} object has no attribute {name!r}"
        )
