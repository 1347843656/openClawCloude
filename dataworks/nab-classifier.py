#!/usr/bin/env python3
"""
DataWorks Not A Bug 快速分类工具

使用方法:
    python nab-classifier.py "错误信息或问题描述"
    
输出:
    - 匹配的 NAB 场景
    - 建议的回复话术
    - 进一步排查建议
"""

import re
import sys
import json

# NAB 规则库
NAB_RULES = [
    {
        "name": "权限问题 - 表不存在",
        "patterns": [r"表不存在", r"table.*not.*exist", r"access.*denied", r"permission.*denied", r"无权限", r"没有.*权限"],
        "category": "权限",
        "response": "亲，这是权限问题哦～请在 DataWorks 申请对应表的读取权限，审批通过后即可~",
        "checks": ["检查 RAM 权限", "检查数据权限申请状态", "确认表名是否正确"]
    },
    {
        "name": "调度问题 - 任务未触发",
        "patterns": [r"任务没跑", r"没触发", r"没有运行", r"not.*trigger", r"not.*run", r"调度.*没"],
        "category": "调度",
        "response": "请检查：1) 调度开关是否打开 2) 依赖节点是否完成 3) 调度时间是否已到~",
        "checks": ["检查调度开关状态", "检查依赖节点状态", "检查调度时间配置"]
    },
    {
        "name": "调度问题 - 依赖未满足",
        "patterns": [r"依赖.*没", r"上游.*没", r"依赖.*失败", r"dependency.*not.*met", r"upstream.*failed"],
        "category": "调度",
        "response": "上游节点还没跑完/失败了，等上游成功后会自动触发哦~",
        "checks": ["检查上游节点状态", "检查依赖配置", "查看任务依赖图"]
    },
    {
        "name": "数据问题 - 数据延迟",
        "patterns": [r"数据没到", r"表是空的", r"没有数据", r"data.*empty", r"data.*not.*ready", r"数据.*延迟"],
        "category": "数据",
        "response": "上游数据还在生产中，预计稍后产出，请耐心等待~",
        "checks": ["检查上游任务状态", "查看数据产出时间", "确认业务日期"]
    },
    {
        "name": "数据问题 - 分区不存在",
        "patterns": [r"分区不存在", r"partition.*not.*exist", r"分区.*没", r"spec.*not.*found"],
        "category": "数据",
        "response": "业务日期的分区还没生成，这是正常的，等上游任务完成后会自动创建~",
        "checks": ["检查分区表达式", "确认业务日期", "查看上游产出情况"]
    },
    {
        "name": "参数问题 - 参数替换失败",
        "patterns": [r"参数.*失败", r"parameter.*replace", r"\$\{.*\}.*错误", r"变量.*未定义"],
        "category": "参数",
        "response": "参数格式应该是 ${参数名}，请检查代码中的参数写法~",
        "checks": ["检查参数格式", "检查调度参数配置", "确认参数定义"]
    },
    {
        "name": "参数问题 - 业务日期不对",
        "patterns": [r"业务日期.*不对", r"bizdate.*wrong", r"日期.*错误", r"时间.*不对"],
        "category": "参数",
        "response": "调度参数里配置的业务日期可能有误，请检查调度参数配置~",
        "checks": ["检查调度参数", "确认业务时间配置", "查看参数替换结果"]
    },
    {
        "name": "语法问题 - SQL 错误",
        "patterns": [r"SQL.*错误", r"syntax.*error", r"语法错误", r"parse.*error"],
        "category": "语法",
        "response": "SQL 有语法错误，请参考 MaxCompute SQL 文档修正~",
        "checks": ["检查 SQL 语法", "查看错误行号", "验证关键字使用"]
    },
    {
        "name": "语法问题 - 函数不支持",
        "patterns": [r"函数不存在", r"function.*not.*exist", r"不支持.*函数", r"undefined.*function"],
        "category": "语法",
        "response": "这个函数 MaxCompute 不支持哦，请查阅支持的函数列表~",
        "checks": ["查阅函数支持列表", "寻找替代函数", "检查函数拼写"]
    },
    {
        "name": "资源问题 - 资源不足",
        "patterns": [r"资源不足", r"resource.*insufficient", r"排队", r"queue", r"CU.*不足"],
        "category": "资源",
        "response": "当前资源组比较繁忙，任务在排队中，稍等就会开始运行~",
        "checks": ["检查资源组使用率", "查看项目配额", "确认资源组状态"]
    },
    {
        "name": "网络问题 - 连接超时",
        "patterns": [r"连接超时", r"timeout", r"连接.*失败", r"connect.*failed", r"网络.*问题"],
        "category": "网络",
        "response": "请检查：1) 网络是否正常 2) 目标 IP 是否在白名单中~",
        "checks": ["检查网络连通性", "检查白名单配置", "验证数据源配置"]
    },
    {
        "name": "数据统计 - 学习数据为 0（统计口径）",
        "patterns": [r"学习数据.*0", r"数据为 0", r"学习数据.*没有", r"任务.*延续", r"统计.*0", r"有任务.*数据.*0"],
        "category": "数据统计",
        "response": "学习数据统计是按【任务开始时间】归属月份的，不是按完成时间。比如任务 1.30 开始，学员 2 月完成，也算在 1 月哦~",
        "checks": ["确认任务开始时间", "确认任务周期", "解释统计口径"]
    },
]

def classify_issue(text):
    """分类问题文本"""
    matches = []
    
    for rule in NAB_RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, text, re.IGNORECASE):
                matches.append(rule)
                break
    
    return matches

def main():
    if len(sys.argv) < 2:
        print("用法：python nab-classifier.py \"错误信息或问题描述\"")
        print("\n示例:")
        print('  python nab-classifier.py "表不存在，无权限访问"')
        print('  python nab-classifier.py "任务没跑，依赖没满足"')
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    print(f"🔍 分析问题：{text}\n")
    
    matches = classify_issue(text)
    
    if matches:
        print(f"✅ 匹配到 {len(matches)} 个可能的 NAB 场景:\n")
        for i, match in enumerate(matches, 1):
            print(f"{i}. 【{match['category']}】{match['name']}")
            print(f"   建议回复：{match['response']}")
            print(f"   进一步检查：{', '.join(match['checks'])}")
            print()
    else:
        print("❌ 未匹配到已知 NAB 场景")
        print("\n建议:")
        print("  1. 收集更多信息（任务 ID、错误截图、发生时间）")
        print("  2. 检查任务配置和日志")
        print("  3. 如确认是新场景，请更新 NAB 规则库")
    
    # 输出 JSON 格式（便于集成）
    print("\n--- JSON 输出 ---")
    result = {
        "input": text,
        "matches": [
            {
                "name": m["name"],
                "category": m["category"],
                "response": m["response"],
                "checks": m["checks"]
            }
            for m in matches
        ],
        "is_nab": len(matches) > 0
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
