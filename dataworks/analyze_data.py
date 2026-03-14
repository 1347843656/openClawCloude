#!/usr/bin/env python3
"""
分析 DataWorks 业务流程和节点数据
"""

import csv
import json
import glob
from collections import defaultdict

# 找到正确的文件名
workflow_file = glob.glob('dataworks*.csv')[0]
print(f"使用文件：{workflow_file}")

# 分析业务流程架构
print("=" * 60)
print("📊 DataWorks 业务流程架构分析")
print("=" * 60)

workflows = []
with open(workflow_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        workflows.append(row)
        print(f"\n📁 业务名称：{row.get('业务名称', 'N/A')}")
        print(f"   工作空间 ID: {row.get('工作空间 ID', 'N/A')}")
        print(f"   使用类型：{row.get('使用类型', 'N/A')}")

print(f"\n✅ 共 {len(workflows)} 个业务流程")

# 分析节点数据
print("\n" + "=" * 60)
print("📊 节点数据分析")
print("=" * 60)

nodes = []
node_types = defaultdict(int)
workflow_nodes = defaultdict(list)
resource_groups = set()

with open('node.csv', 'r', encoding='utf-8') as f:
    # 没有表头，手动解析
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) >= 12:
            node = {
                'node_id': parts[0],
                'workspace_id': parts[1],
                'workflow_id': parts[2],
                'workflow_name': parts[3],
                'schedule': parts[4],
                'node_name': parts[5],
                'project_id': parts[6],
                'node_type': parts[7],
                'resource_group': parts[9],
                'graph': parts[10],
                'status': parts[11],
                'create_time': parts[13] if len(parts) > 13 else ''
            }
            nodes.append(node)
            node_types[node['node_type']] += 1
            workflow_nodes[node['workflow_name']].append(node)
            resource_groups.add(node['resource_group'])

print(f"\n📈 节点总数：{len(nodes)}")

print("\n📋 节点类型分布:")
for ntype, count in sorted(node_types.items(), key=lambda x: -x[1]):
    print(f"   {ntype}: {count} 个")

print("\n📋 业务流程节点分布:")
for wf_name, wf_nodes in sorted(workflow_nodes.items()):
    print(f"   {wf_name}: {len(wf_nodes)} 个节点")

print(f"\n📋 资源组数量：{len(resource_groups)}")

# 保存分析结果
analysis = {
    'workflows': workflows,
    'total_nodes': len(nodes),
    'node_types': dict(node_types),
    'workflow_node_count': {k: len(v) for k, v in workflow_nodes.items()},
    'resource_groups': list(resource_groups)
}

with open('analysis_result.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)

print("\n✅ 分析结果已保存到 analysis_result.json")

# 输出节点类型说明
print("\n" + "=" * 60)
print("📝 节点类型说明")
print("=" * 60)

type_desc = {
    'VIRTUAL': '虚拟节点 - 用于流程控制和依赖管理',
    'PARAM_HUB': '参数中心节点 - 管理调度参数',
    'CONTROLLER_ASSIGNMENT': '控制分配节点 - 任务分发',
    'CONTROLLER_TRAVERSE': '控制遍历节点 - 数据遍历同步',
    'CONTROLLER_JOIN': '控制汇聚节点 - 数据汇聚'
}

for ntype, desc in type_desc.items():
    count = node_types.get(ntype, 0)
    print(f"   {ntype}: {desc} ({count}个)")
