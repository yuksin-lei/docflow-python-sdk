#!/bin/bash

# 发布脚本 - 自动创建 tag 并触发 PyPI 发布
# 使用方法: ./release.sh [version]
# 如果不指定 version，则使用 pyproject.toml 中的版本号

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# 检查是否在 git 仓库中
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "当前目录不是 git 仓库"
    exit 1
fi

# 检查工作目录是否干净
if [ -n "$(git status --porcelain)" ]; then
    print_warning "工作目录有未提交的更改："
    git status --short
    echo ""
    read -p "是否继续？(y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "已取消"
        exit 1
    fi
fi

# 获取版本号
if [ -n "$1" ]; then
    VERSION="$1"
    print_info "使用指定版本号: $VERSION"
else
    # 从 pyproject.toml 读取版本号
    if [ ! -f "pyproject.toml" ]; then
        print_error "未找到 pyproject.toml 文件"
        exit 1
    fi

    VERSION=$(grep '^version = ' pyproject.toml | cut -d'"' -f2)

    if [ -z "$VERSION" ]; then
        print_error "无法从 pyproject.toml 中读取版本号"
        exit 1
    fi

    print_info "从 pyproject.toml 读取版本号: $VERSION"
fi

# 验证版本号格式
if [[ ! $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+([.-][a-zA-Z0-9]+)?$ ]]; then
    print_error "版本号格式错误: $VERSION"
    print_info "正确格式示例: 1.0.0, 1.2.3, 2.0.0-beta.1"
    exit 1
fi

TAG_NAME="v$VERSION"

# 检查 tag 是否已存在
if git rev-parse "$TAG_NAME" >/dev/null 2>&1; then
    print_error "Tag $TAG_NAME 已存在"
    print_info "如果要重新发布，请先删除旧 tag："
    echo "  git tag -d $TAG_NAME"
    echo "  git push origin :$TAG_NAME"
    exit 1
fi

# 检查远程 tag
if git ls-remote --tags origin | grep -q "refs/tags/$TAG_NAME"; then
    print_error "远程已存在 tag $TAG_NAME"
    print_info "请先删除远程 tag："
    echo "  git push origin :$TAG_NAME"
    exit 1
fi

# 获取当前分支
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
print_info "当前分支: $CURRENT_BRANCH"

# 确认信息
echo ""
echo "========================================"
echo "📦 准备发布"
echo "========================================"
echo "版本号: $VERSION"
echo "Tag 名称: $TAG_NAME"
echo "当前分支: $CURRENT_BRANCH"
echo "========================================"
echo ""

read -p "确认发布？(y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_info "已取消发布"
    exit 0
fi

# 创建 tag
print_info "创建 tag: $TAG_NAME"
git tag -a "$TAG_NAME" -m "Release version $VERSION"
print_success "Tag 创建成功"

# 推送 tag
print_info "推送 tag 到远程仓库"
git push origin "$TAG_NAME"
print_success "Tag 推送成功"

# 完成
echo ""
echo "========================================"
print_success "发布流程已启动！"
echo "========================================"
echo ""
print_info "GitHub Actions 正在自动发布到 PyPI"
print_info "查看发布进度："
echo "  https://github.com/yuksin-lei/docflow-sdk/actions"
echo ""
print_info "发布完成后，可以在以下位置查看："
echo "  PyPI: https://pypi.org/project/docflow-sdk/$VERSION/"
echo "  GitHub Release: https://github.com/yuksin-lei/docflow-sdk/releases/tag/$TAG_NAME"
echo ""
print_info "安装新版本："
echo "  pip install docflow-sdk==$VERSION"
echo ""
