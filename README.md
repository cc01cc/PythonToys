# PythonToys

由 Python 构建的一系列小工具合集

## 许可证

本项目采用 Apache 2.0 许可证授权

作者（或原始版权持有者）依然保留对代码的版权（Copyright）。

## 1. 开发指南

- git 远程常驻分支包括：`main`, `develop`
- 新功能开发时，从 `develop` 分支新建 `feature, hotfix, bugfix` 分支（会定期清理）
  - 分支命名示例 `feature/250622/add_new_feature`
- 新建分支后，本地创建 `local` 或 `private` 分支进行开发
- 开发每个阶段完成时，使用 `--squash` 合并到 `feature, hotfix, bugfix` 分支中

.git/hooks 中推荐添加 `pre-push` 文件，并添加以下内容，避免本地分支被 push：

```bash
#!/bin/sh
current_branch=$(git symbolic-ref --short HEAD)

if echo "$current_branch" | grep -qiE "local|private"; then
  echo "错误：分支名含敏感词！" >&2
  exit 1
fi
```

常用 git 命令参考：

```bash
# 删除分支
git branch -d feature/xxx
# merge local 分支
git merge --squash local
# merge 分支
git merge feature/xxx
```

## 2. Paste Image Tool 工具介绍

本工具可实现从剪贴板捕获图片→自动保存→生成 Markdown 图片链接→复制回剪贴板的完整流程。适用于技术文档编写、笔记记录等需要频繁插入图片的场景。

[具体文档详见 ./docs/paste_image_tool.md](./docs/paste_image_tool.md)
