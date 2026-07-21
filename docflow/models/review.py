"""
审核规则相关数据模型
"""
from typing import List, Optional, Any, Dict
from dataclasses import dataclass, field
from .._constants import DEFAULT_PAGE
from ._base import ForwardCompatibleModel


@dataclass
class ReviewRule(ForwardCompatibleModel):
    """审核规则"""
    rule_id: str
    name: str
    prompt: Optional[str] = None
    category_ids: Optional[List[str]] = None
    risk_level: Optional[int] = None
    referenced_fields: Optional[List[Dict[str, Any]]] = None


@dataclass
class ReviewGroup(ForwardCompatibleModel):
    """审核规则组"""
    group_id: str
    name: str
    rules: List[ReviewRule] = field(default_factory=list)

    def __post_init__(self):
        """初始化后处理"""
        if isinstance(self.rules, list):
            self.rules = [
                ReviewRule.from_dict(r) if isinstance(r, dict) else r
                for r in self.rules
            ]


@dataclass
class ReviewRepoInfo(ForwardCompatibleModel):
    """审核规则库信息"""
    repo_id: str
    name: str
    groups: List[ReviewGroup] = field(default_factory=list)
    category_ids: Optional[List[str]] = None

    def __post_init__(self):
        """初始化后处理"""
        if isinstance(self.groups, list):
            self.groups = [
                ReviewGroup.from_dict(g) if isinstance(g, dict) else g
                for g in self.groups
            ]


@dataclass
class ReviewRepoCreateResponse(ForwardCompatibleModel):
    """创建审核规则库响应"""
    repo_id: str


@dataclass
class ReviewRepoListResponse(ForwardCompatibleModel):
    """审核规则库列表响应"""
    repos: List[ReviewRepoInfo] = field(default_factory=list)
    total: int = 0
    page: int = DEFAULT_PAGE
    page_size: int = 10

    def __post_init__(self):
        """初始化后处理"""
        if isinstance(self.repos, list):
            self.repos = [
                ReviewRepoInfo.from_dict(r) if isinstance(r, dict) else r
                for r in self.repos
            ]


@dataclass
class ReviewGroupCreateResponse(ForwardCompatibleModel):
    """创建审核规则组响应"""
    group_id: str


@dataclass
class ReviewRuleCreateResponse(ForwardCompatibleModel):
    """创建审核规则响应"""
    rule_id: str
