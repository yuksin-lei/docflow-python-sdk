"""
审核规则资源类
"""
from typing import Optional, List, Dict, Any
from .base import BaseResource
from ..models.review import (
    ReviewRepoCreateResponse,
    ReviewRepoListResponse,
    ReviewRepoInfo,
    ReviewGroupCreateResponse,
    ReviewRuleCreateResponse
)
from .._constants import DEFAULT_PAGE, API_PREFIX
from ..enums import ReviewModel
from ..exceptions import ValidationError


class ReviewResource(BaseResource):
    """
    审核规则资源类

    提供审核规则库、规则组和规则的管理功能
    """

    # ==================== 规则库管理 ====================

    def create_repo(
        self,
        workspace_id: str,
        name: str,
    ) -> ReviewRepoCreateResponse:
        """
        创建审核规则库

        Args:
            workspace_id: 空间ID
            name: 规则库名称

        Returns:
            ReviewRepoCreateResponse: 创建响应
        """
        payload = {
            "workspace_id": workspace_id,
            "name": name
        }

        response = self.http_client.post(
            f"{API_PREFIX}/review/rule_repo/create",
            json_data=payload
        )

        return ReviewRepoCreateResponse(**response['result'])

    def list_repos(
        self,
        workspace_id: str,
        page: int = DEFAULT_PAGE,
        page_size: int = 10,
    ) -> ReviewRepoListResponse:
        """
        获取审核规则库列表

        Args:
            workspace_id: 空间ID
            page: 页码
            page_size: 每页数量

        Returns:
            ReviewRepoListResponse: 规则库列表
        """
        params = {
            "workspace_id": workspace_id,
            "page": page,
            "page_size": page_size
        }

        response = self.http_client.get(
            f"{API_PREFIX}/review/rule_repo/list",
            params=params
        )

        return ReviewRepoListResponse(**response['result'])

    def get_repo(
        self,
        workspace_id: str,
        repo_id: str,
    ) -> ReviewRepoInfo:
        """
        获取审核规则库详情

        Args:
            workspace_id: 空间ID
            repo_id: 规则库ID

        Returns:
            ReviewRepoInfo: 规则库详情
        """
        params = {
            "workspace_id": workspace_id,
            "repo_id": repo_id
        }

        response = self.http_client.get(
            f"{API_PREFIX}/review/rule_repo/get",
            params=params
        )

        return ReviewRepoInfo(**response['result'])

    def update_repo(
        self,
        workspace_id: str,
        repo_id: str,
        name: Optional[str] = None,
    ) -> None:
        """
        更新审核规则库

        Args:
            workspace_id: 空间ID
            repo_id: 规则库ID
            name: 新的规则库名称
        """
        payload = {
            "workspace_id": workspace_id,
            "repo_id": repo_id
        }

        if name is not None:
            payload["name"] = name

        self.http_client.post(
            f"{API_PREFIX}/review/rule_repo/update",
            json_data=payload
        )

    def delete_repo(
        self,
        workspace_id: str,
        repo_ids: List[str],
    ) -> None:
        """
        删除审核规则库

        Args:
            workspace_id: 空间ID
            repo_ids: 规则库ID列表
        """
        payload = {
            "workspace_id": workspace_id,
            "repo_ids": repo_ids
        }

        self.http_client.post(
            f"{API_PREFIX}/review/rule_repo/delete",
            json_data=payload
        )

    # ==================== 规则组管理 ====================

    def create_group(
        self,
        workspace_id: str,
        repo_id: str,
        name: str,
    ) -> ReviewGroupCreateResponse:
        """
        创建审核规则组

        Args:
            workspace_id: 空间ID
            repo_id: 规则库ID
            name: 规则组名称

        Returns:
            ReviewGroupCreateResponse: 创建响应
        """
        payload = {
            "workspace_id": workspace_id,
            "repo_id": repo_id,
            "name": name
        }

        response = self.http_client.post(
            f"{API_PREFIX}/review/rule_group/create",
            json_data=payload
        )

        return ReviewGroupCreateResponse(**response['result'])

    def update_group(
        self,
        workspace_id: str,
        group_id: str,
        name: Optional[str] = None,
    ) -> None:
        """
        更新审核规则组

        Args:
            workspace_id: 空间ID
            group_id: 规则组ID
            name: 新的规则组名称
        """
        payload = {
            "workspace_id": workspace_id,
            "group_id": group_id
        }

        if name is not None:
            payload["name"] = name

        self.http_client.post(
            f"{API_PREFIX}/review/rule_group/update",
            json_data=payload
        )

    def delete_group(
        self,
        workspace_id: str,
        group_id: str,
    ) -> None:
        """
        删除审核规则组

        Args:
            workspace_id: 空间ID
            group_id: 规则组ID
        """
        payload = {
            "workspace_id": workspace_id,
            "group_id": group_id
        }

        self.http_client.post(
            f"{API_PREFIX}/review/rule_group/delete",
            json_data=payload
        )

    # ==================== 规则管理 ====================

    def create_rule(
        self,
        workspace_id: str,
        repo_id: int,
        group_id: Optional[str] = None,
        name: Optional[str] = None,
        prompt: Optional[str] = None,
        category_ids: Optional[List[str]] = None,
        risk_level: Optional[int] = None,
        referenced_fields: Optional[List[Dict[str, Any]]] = None,
    ) -> ReviewRuleCreateResponse:
        """
        创建审核规则

        Args:
            workspace_id: 空间ID
            repo_id: 审核规则库ID
            group_id: 规则组ID（可选）
            name: 规则名称（可选）
            prompt: 规则提示词（可选）
            category_ids: 分类ID列表（可选）
            risk_level: 风险等级，10:高风险，20:中风险，30:低风险（可选）
            referenced_fields: 引用字段列表（可选）

        Returns:
            ReviewRuleCreateResponse: 创建响应
        """
        payload = {
            "workspace_id": workspace_id,
            "repo_id": repo_id,
        }

        # 添加可选参数
        if group_id is not None:
            payload["group_id"] = group_id
        if name is not None:
            payload["name"] = name
        if prompt is not None:
            payload["prompt"] = prompt
        if category_ids is not None:
            payload["category_ids"] = category_ids
        if risk_level is not None:
            payload["risk_level"] = risk_level
        if referenced_fields is not None:
            payload["referenced_fields"] = referenced_fields

        response = self.http_client.post(
            f"{API_PREFIX}/review/rule/create",
            json_data=payload
        )

        return ReviewRuleCreateResponse(**response['result'])

    def update_rule(
        self,
        workspace_id: str,
        rule_id: str,
        group_id: Optional[str] = None,
        name: Optional[str] = None,
        prompt: Optional[str] = None,
        category_ids: Optional[List[str]] = None,
        risk_level: Optional[int] = None,
        referenced_fields: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        更新审核规则

        Args:
            workspace_id: 空间ID
            rule_id: 规则ID
            group_id: 规则组ID（可选）
            name: 规则名称（可选）
            prompt: 规则提示词（可选）
            category_ids: 分类ID列表（可选）
            risk_level: 风险等级，10:高风险，20:中风险，30:低风险（可选）
            referenced_fields: 引用字段列表（可选）
        """
        payload = {
            "workspace_id": workspace_id,
            "rule_id": rule_id
        }

        # 添加可选参数
        if group_id is not None:
            payload["group_id"] = group_id
        if name is not None:
            payload["name"] = name
        if prompt is not None:
            payload["prompt"] = prompt
        if category_ids is not None:
            payload["category_ids"] = category_ids
        if risk_level is not None:
            payload["risk_level"] = risk_level
        if referenced_fields is not None:
            payload["referenced_fields"] = referenced_fields

        self.http_client.post(
            f"{API_PREFIX}/review/rule/update",
            json_data=payload
        )

    def delete_rule(
        self,
        workspace_id: str,
        rule_id: str,
    ) -> None:
        """
        删除审核规则

        Args:
            workspace_id: 空间ID
            rule_id: 规则ID
        """
        payload = {
            "workspace_id": workspace_id,
            "rule_id": rule_id
        }

        self.http_client.post(
            f"{API_PREFIX}/review/rule/delete",
            json_data=payload
        )

    # ==================== 任务管理 ====================

    def submit_task(
        self,
        workspace_id: str,
        name: str,
        repo_id: str,
        extract_task_ids: Optional[List[str]] = None,
        batch_number: Optional[str] = None,
        model: Optional[ReviewModel] = None,
    ) -> Dict[str, Any]:
        """
        新建审核任务

        Args:
            workspace_id: 空间ID
            name: 任务名称（最大100字符）
            repo_id: 审核规则库ID
            extract_task_ids: 抽取任务ID列表（可选）
            batch_number: 批次号（可选）
            model: 审核模型，deepseek-r1, qwq-32b, qwen3-max, ORM-O1（可选）

        Returns:
            Dict[str, Any]: 包含 task_id 的响应

        Raises:
            ValidationError: 参数校验失败
        """
        # 校验 name
        if not name or not name.strip():
            raise ValidationError(
                "任务名称不能为空",
                i18n_key='error.review_task.name_empty'
            )
        if len(name) > 100:
            raise ValidationError(
                "任务名称不能超过 100 个字符",
                i18n_key='error.review_task.name_too_long',
                max_length=100
            )

        # 校验 repo_id
        if not repo_id:
            raise ValidationError(
                "审核规则库 ID 不能为空",
                i18n_key='error.review_task.repo_id_empty'
            )
        if not repo_id.isdigit():
            raise ValidationError(
                "审核规则库 ID 必须是数字字符串",
                i18n_key='error.review_task.repo_id_invalid'
            )

        # 校验 extract_task_ids 中的每个 ID
        if extract_task_ids:
            for task_id in extract_task_ids:
                if not task_id.isdigit():
                    raise ValidationError(
                        "抽取任务 ID 必须是数字字符串",
                        i18n_key='error.category.id_invalid'
                    )

        payload = {
            "workspace_id": workspace_id,
            "name": name,
            "repo_id": repo_id
        }

        if extract_task_ids is not None:
            payload["extract_task_ids"] = extract_task_ids
        if batch_number is not None:
            payload["batch_number"] = batch_number
        if model is not None:
            payload["model"] = model.value if isinstance(model, ReviewModel) else model

        response = self.http_client.post(
            f"{API_PREFIX}/review/task/submit",
            json_data=payload
        )

        return response['result']

    def delete_task(
        self,
        workspace_id: str,
        task_ids: List[str],
    ) -> None:
        """
        删除审核任务

        Args:
            workspace_id: 空间ID
            task_ids: 审核任务ID列表

        Raises:
            ValidationError: 参数校验失败
        """
        # 校验 task_ids
        if not task_ids:
            raise ValidationError(
                "task_ids 不能为空",
                i18n_key='error.review_task.delete_list_empty'
            )

        # 校验每个 task_id
        for task_id in task_ids:
            if not task_id:
                raise ValidationError(
                    "审核任务 ID 不能为空",
                    i18n_key='error.review_task.id_empty'
                )
            if not task_id.isdigit():
                raise ValidationError(
                    "审核任务 ID 必须是数字字符串",
                    i18n_key='error.review_task.id_invalid'
                )

        payload = {
            "workspace_id": workspace_id,
            "task_ids": task_ids
        }

        self.http_client.post(
            f"{API_PREFIX}/review/task/delete",
            json_data=payload
        )

    def get_task_result(
        self,
        workspace_id: str,
        task_id: str,
        with_task_detail_url: Optional[bool] = None,
        model: Optional[ReviewModel] = None,
    ) -> Dict[str, Any]:
        """
        获取审核结果

        Args:
            workspace_id: 空间ID
            task_id: 审核任务ID
            with_task_detail_url: 是否返回审核详情页URL（可选）
            model: 审核模型，审核模型，deepseek-r1, qwq-32b, qwen3-max, ORM-O1（可选）

        Returns:
            Dict[str, Any]: 审核任务结果

        Raises:
            ValidationError: 参数校验失败
        """
        # 校验 task_id
        if not task_id:
            raise ValidationError(
                "审核任务 ID 不能为空",
                i18n_key='error.review_task.id_empty'
            )
        if not task_id.isdigit():
            raise ValidationError(
                "审核任务 ID 必须是数字字符串",
                i18n_key='error.review_task.id_invalid'
            )

        payload = {
            "workspace_id": workspace_id,
            "task_id": task_id
        }

        if with_task_detail_url is not None:
            payload["with_task_detail_url"] = with_task_detail_url
        if model is not None:
            payload["model"] = model.value if isinstance(model, ReviewModel) else model

        response = self.http_client.post(
            f"{API_PREFIX}/review/task/result",
            json_data=payload
        )

        return response['result']

    def retry_task(
        self,
        workspace_id: str,
        task_id: str,
    ) -> None:
        """
        重新审核任务

        Args:
            workspace_id: 空间ID
            task_id: 审核任务ID

        Raises:
            ValidationError: 参数校验失败
        """
        # 校验 task_id
        if not task_id:
            raise ValidationError(
                "审核任务 ID 不能为空",
                i18n_key='error.review_task.id_empty'
            )
        if not task_id.isdigit():
            raise ValidationError(
                "审核任务 ID 必须是数字字符串",
                i18n_key='error.review_task.id_invalid'
            )

        payload = {
            "workspace_id": workspace_id,
            "task_id": task_id
        }

        self.http_client.post(
            f"{API_PREFIX}/review/task/retry",
            json_data=payload
        )

    def retry_task_rule(
        self,
        workspace_id: str,
        task_id: str,
        rule_id: str,
    ) -> None:
        """
        重新审核任务中的某条规则

        Args:
            workspace_id: 空间ID
            task_id: 审核任务ID
            rule_id: 审核规则ID

        Raises:
            ValidationError: 参数校验失败
        """
        # 校验 task_id
        if not task_id:
            raise ValidationError(
                "审核任务 ID 不能为空",
                i18n_key='error.review_task.id_empty'
            )
        if not task_id.isdigit():
            raise ValidationError(
                "审核任务 ID 必须是数字字符串",
                i18n_key='error.review_task.id_invalid'
            )

        # 校验 rule_id
        if not rule_id:
            raise ValidationError(
                "审核规则 ID 不能为空",
                i18n_key='error.review_task.rule_id_empty'
            )
        if not rule_id.isdigit():
            raise ValidationError(
                "审核规则 ID 必须是数字字符串",
                i18n_key='error.review_task.rule_id_invalid'
            )
        
        payload = {
            "workspace_id": workspace_id,
            "task_id": task_id,
            "rule_id": rule_id
        }

        self.http_client.post(
            f"{API_PREFIX}/review/task/rule/retry",
            json_data=payload
        )
