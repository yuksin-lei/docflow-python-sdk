"""
工作空间相关数据模型
"""
from dataclasses import dataclass
from typing import Optional, List, Any, Dict


@dataclass
class WorkspaceInfo:
    """工作空间信息"""

    workspace_id: str
    name: str
    auth_scope: Optional[int] = None
    description: Optional[str] = None
    manage_account_id: Optional[str] = None
    manage_account_name: Optional[str] = None
    callback_url: Optional[str] = None
    callback_retry_time: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceInfo":
        """从字典创建对象"""
        manage_account_id = data.get("manage_account_id", data.get("manageAccountId"))
        return cls(
            workspace_id=str(data.get("workspace_id", data.get("workspaceId", ""))),
            name=data.get("name", ""),
            auth_scope=data.get("auth_scope", data.get("authScope")),
            description=data.get("description"),
            manage_account_id=str(manage_account_id) if manage_account_id is not None else None,
            manage_account_name=data.get("manage_account_name", data.get("manageAccountName")),
            callback_url=data.get("callback_url", data.get("callbackUrl")),
            callback_retry_time=data.get("callback_retry_time", data.get("callbackRetryTime")),
        )


@dataclass
class WorkspaceCreateResponse:
    """创建工作空间响应"""

    workspace_id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceCreateResponse":
        """从字典创建对象"""
        return cls(
            workspace_id=str(data.get("workspace_id", data.get("workspaceId", "")))
        )


@dataclass
class WorkspaceListResponse:
    """工作空间列表响应"""

    total: int
    page: int
    page_size: int
    workspaces: List[WorkspaceInfo]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceListResponse":
        """从字典创建对象"""
        workspaces_data = data.get("workspaces", data.get("list", []))
        workspaces = [WorkspaceInfo.from_dict(ws) for ws in workspaces_data]

        return cls(
            total=data.get("total", 0),
            page=data.get("page", 1),
            page_size=data.get("page_size", data.get("pageSize", 20)),
            workspaces=workspaces,
        )


@dataclass
class WorkspaceDetailResponse:
    """工作空间详情响应"""

    workspace_id: str
    name: str
    auth_scope: Optional[int] = None
    description: Optional[str] = None
    manage_account_id: Optional[str] = None
    manage_account_name: Optional[str] = None
    callback_url: Optional[str] = None
    callback_retry_time: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceDetailResponse":
        """从字典创建对象"""
        manage_account_id = data.get("manage_account_id", data.get("manageAccountId"))
        return cls(
            workspace_id=str(data.get("workspace_id", data.get("workspaceId", ""))),
            name=data.get("name", ""),
            auth_scope=data.get("auth_scope", data.get("authScope")),
            description=data.get("description"),
            manage_account_id=str(manage_account_id) if manage_account_id is not None else None,
            manage_account_name=data.get("manage_account_name", data.get("manageAccountName")),
            callback_url=data.get("callback_url", data.get("callbackUrl")),
            callback_retry_time=data.get("callback_retry_time", data.get("callbackRetryTime")),
        )
