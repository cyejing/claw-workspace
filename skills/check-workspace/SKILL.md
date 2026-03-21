---
name: check-workspace
description: 当用户想要查看描述文件的时候使用
---

## 描述
当用户输入 "查看描述文件" 时，将展示workspace目录中文件的具体内容，包括：
- AGENTS.md
- SOUL.md  
- USER.md
- HEARTBEAT.md
- IDENTITY.md
- TOOLS.md
- MEMORY.md

## 附加
额外列出 skills 目录下的技能名称和描述内容

## 实现
该技能通过调用read工具读取指定文件内容，并以友好的格式展示给用户。

## 使用方法
用户输入：查看描述文件
系统响应：展示所有相关文件的内容


