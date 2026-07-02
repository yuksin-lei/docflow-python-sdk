"""
Docflow SDK 枚举类型

定义所有 API 参数的枚举值，避免用户传错参数
"""
from enum import Enum


class ExtractModel(str, Enum):
    """
    提取模型类型（V1.6 命名）

    推荐使用新命名。后端同时兼容旧命名（Model 1/2/3），因此 SDK 保留旧成员作为
    别名，但已标记为**废弃（deprecated）**，请尽快迁移到新命名。

    | 新命名（推荐） | 旧命名（废弃） | 说明                          |
    |--------------|--------------|-------------------------------|
    | Auto         | -            | 智能匹配抽取模型（字段级智能路由，由算法决定实际模型） |
    | Acgpt        | Model 1      | 速度快，抽取结果稳定             |
    | Acgpt_VL     | Model 3      | 多模态，适用简单抽取（≤10 页）    |
    | DF_M1        | Model 2      | 适用复杂文档理解                |
    """
    # ==================== 新命名（推荐） ====================
    Auto = "Auto"          # 智能匹配抽取模型（字段级智能路由）
    Acgpt = "Acgpt"        # 速度快，抽取结果稳定（原 Model 1）
    Acgpt_VL = "Acgpt-VL"  # 多模态，适用简单抽取（≤10 页）（原 Model 3）
    DF_M1 = "DF-M1"        # 适用复杂文档理解（原 Model 2）

    # ============ 旧命名（已废弃，仅作兼容别名，后端仍接受） ============
    # Deprecated: 请改用上方新命名。
    Model_1 = "Model 1"    # 等价于 Acgpt
    Model_2 = "Model 2"    # 等价于 DF_M1
    Model_3 = "Model 3"    # 等价于 Acgpt_VL


class EnabledStatus(str, Enum):
    """
    启用状态（用于查询）

    Attributes:
        ALL: 全部
        DISABLED: 未启用
        ENABLED: 已启用
        OTHER: 其他状态
    """
    ALL = "all"
    DISABLED = "0"
    ENABLED = "1"
    OTHER = "2"


class EnabledFlag(int, Enum):
    """
    启用标志（用于更新）

    Attributes:
        DISABLED: 未启用
        ENABLED: 已启用
    """
    DISABLED = 0
    ENABLED = 1


class AuthScope(int, Enum):
    """
    权限范围

    Attributes:
        PRIVATE: 私有权限
        PUBLIC: 公共权限
    """
    PRIVATE = 0
    PUBLIC = 1


class FieldType(str, Enum):
    """
    字段转换类型（用于 transform_settings.type）

    Attributes:
        DATETIME: 日期时间类型转换
        ENUMERATE: 枚举类型转换
        REGEX: 正则表达式类型转换
    """
    DATETIME = "datetime"
    ENUMERATE = "enumerate"
    REGEX = "regex"

class MismatchAction(str, Enum):
    """
    字段不匹配时的处理动作

    Attributes:
        DEFAULT: 使用默认值
        WARNING: 显示警告
    """
    DEFAULT = "default"
    WARNING = "warning"


class ReviewModel(str, Enum):
    """
    审核模型类型

    Attributes:
        DEEPSEEK_R1: deepseek-r1
        QWQ_32B: qwq-32b
        QWEN3_MAX: qwen3-max
        ORM_O1: ORM-O1
    """
    DEEPSEEK_R1 = "deepseek-r1"
    QWQ_32B = "qwq-32b"
    QWEN3_MAX = "qwen3-max"
    ORM_O1 = "ORM-O1"


class RecognitionStatus(int, Enum):
    """
    文件识别状态

    Attributes:
        PENDING: 待识别
        SUCCESS: 识别成功
        FAILED: 识别失败
        CLASSIFYING: 分类中
        EXTRACTING: 抽取中
        PREPARING: 准备中
    """
    PENDING = 0
    SUCCESS = 1
    FAILED = 2
    CLASSIFYING = 3
    EXTRACTING = 4
    PREPARING = 5
