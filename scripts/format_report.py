#!/usr/bin/env python3
"""
Code Review 报告格式化脚本
Agent 调用此脚本时，只接收输出结果，脚本本身不进入 context window
"""

import sys
import json
from datetime import datetime


def format_report(review_data: dict) -> str:
    """将 Agent 生成的结构化数据格式化为 Markdown 报告"""
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    filename = review_data.get("filename", "未知文件")
    language = review_data.get("language", "未知语言")
    
    lines = [
        f"## 📋 Code Review Report",
        f"",
        f"**文件**：`{filename}`  ",
        f"**语言**：{language}  ",
        f"**审查时间**：{now}  ",
        f"",
        "---",
        "",
    ]
    
    # 严重问题
    critical = review_data.get("critical", [])
    lines.append("### 🔴 严重问题（必须修复）")
    if critical:
        lines.append("| # | 位置 | 问题描述 | 修复建议 |")
        lines.append("|---|------|---------|---------|")
        for i, item in enumerate(critical, 1):
            lines.append(f"| {i} | {item['location']} | {item['issue']} | {item['fix']} |")
    else:
        lines.append("_无严重问题_ ✅")
    lines.append("")

    # 一般建议
    warnings = review_data.get("warnings", [])
    lines.append("### 🟡 一般建议（建议修复）")
    if warnings:
        lines.append("| # | 位置 | 问题描述 | 修复建议 |")
        lines.append("|---|------|---------|---------|")
        for i, item in enumerate(warnings, 1):
            lines.append(f"| {i} | {item['location']} | {item['issue']} | {item['fix']} |")
    else:
        lines.append("_无一般问题_ ✅")
    lines.append("")

    # 综合评分
    scores = review_data.get("scores", {})
    if scores:
        lines.append("### 📊 综合评分")
        lines.append("")
        lines.append("| 维度 | 评分 |")
        lines.append("|------|------|")
        for dim, score in scores.items():
            lines.append(f"| {dim} | {score}/10 |")
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Agent 通过 stdin 传入 JSON 数据
    try:
        data = json.loads(sys.stdin.read())
        print(format_report(data))
    except json.JSONDecodeError:
        # 如果 Agent 没有传入结构化数据，直接跳过格式化
        print("<!-- format_report: no structured data provided, using raw output -->")