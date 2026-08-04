import os
import sys
import json
from typing import Any, List

# Add the protocol projection engine to the import path.
mpst_gen_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "..",
    "..",
    "protocol-projection",
)
mpst_gen_path = os.path.abspath(mpst_gen_path)
if mpst_gen_path not in sys.path:
    sys.path.insert(0, mpst_gen_path)

from parsing.InputParser import get_gt_from_file
from evaluation_functionality.EvalSubsetProjection import EvalSubsetProjection
from evaluation_functionality.EvalClassicalProjection import EvalClassicalProjection


class GTProjection:
    """全局类型投影工具，用于读取 .gt 文件并进行投影。"""

    def __init__(self, projection_method: str = "subset"):
        """初始化投影工具。

        Args:
            projection_method: 投影方法，可选 'subset'（子集投影）或 'classical'（经典投影）
        """
        self.projection_method = projection_method.lower()
        if self.projection_method not in ["subset", "classical"]:
            raise ValueError("projection_method 必须是 'subset' 或 'classical'")

    def read_protocol_file(self, file_path: str) -> dict[str, Any]:
        """读取并解析全局类型文件。"""
        result = {
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "exists": False,
            "content": None,
            "error": None
        }

        if not os.path.exists(file_path):
            result["error"] = f"文件不存在: {file_path}"
            return result

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                result["content"] = f.read()
            result["exists"] = True
        except Exception as e:
            result["error"] = f"读取文件失败: {str(e)}"

        return result

    def load_message_types(self, file_path: str) -> dict[str, str]:
        """加载消息类型映射文件 (.type.json)。

        类型映射文件应该与 .gt 文件同名但扩展名为 .type.json，
        包含从消息标签到数据类型的映射。

        Returns:
            消息标签到数据类型的字典，如 {"number": "int", "result": "float"}
        """
        type_file_path = file_path.replace('.gt', '.type.json')
        type_map = {}
        
        if os.path.exists(type_file_path):
            try:
                with open(type_file_path, 'r', encoding='utf-8') as f:
                    type_map = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load type mapping from {type_file_path}: {e}")
        
        return type_map

    def inject_types_into_projection(self, projection_str: str, type_map: dict[str, str]) -> str:
        """将数据类型注入到投影字符串中。

        将投影字符串中的消息标签替换为带类型注解的格式，如 number 变为 number__int。
        这样可以保留类型信息供运行时验证使用。

        Args:
            projection_str: 从协议投影引擎得到的字符串
            type_map: 消息标签到数据类型的映射

        Returns:
            注入类型注解后的投影字符串
        """
        import re
        
        result = projection_str
        
        # 匹配消息发送: Receiver!message 或 消息接收: Sender?message
        # 注意：message 可能是纯标签（如 number），我们需要检查映射
        for msg_label, msg_type in type_map.items():
            # 匹配 !msg_label. 或 ?msg_label. 后跟分隔符
            # 模式：!(msg_label)(\s|$|\.)
            pattern_spl = rf'([?!]){re.escape(msg_label)}\b'
            replacement = rf'\1{msg_label}__{msg_type}'
            result = re.sub(pattern_spl, replacement, result)
        
        return result

    def list_protocols_in_directory(self, directory_path: str) -> list[dict[str, Any]]:
        """列出目录中的所有 .gt 文件。"""
        protocols = []

        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return protocols

        for file_name in os.listdir(directory_path):
            if file_name.endswith('.gt'):
                file_path = os.path.join(directory_path, file_name)
                protocols.append({
                    "file_name": file_name,
                    "file_path": file_path
                })

        return sorted(protocols, key=lambda x: x["file_name"])

    def get_protocol_summary(self, content: str) -> dict[str, Any]:
        """从全局类型内容中提取摘要信息。"""
        summary = {
            "processes": [],
            "content_preview": content[:200] + "..." if len(content) > 200 else content
        }

        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if '->' in line:
                parts = line.split('->')
                if len(parts) >= 2:
                    sender = parts[0].strip()
                    receiver_part = parts[1].split(':')[0].strip() if ':' in parts[1] else parts[1].strip()
                    receiver = receiver_part.split()[0].strip() if receiver_part else ''
                    
                    if sender and sender not in summary["processes"]:
                        summary["processes"].append(sender)
                    if receiver and receiver not in summary["processes"]:
                        summary["processes"].append(receiver)

        return summary

    def project_protocol(self, file_path: str, protocol_name: str, role: str) -> dict[str, Any]:
        """将全局类型投影为指定角色的局部协议。

        Args:
            file_path: .gt 文件的路径
            protocol_name: 协议名称
            role: 要投影的角色

        Returns:
            包含投影结果的字典：
            - file_path: 原始文件路径
            - protocol_name: 协议名称
            - role: 角色
            - local_protocol: 生成的局部协议（已注入类型信息）
            - type_map: 消息类型映射
            - successful_method: 使用的投影方法
            - error: 错误信息
        """
        result = {
            "file_path": file_path,
            "protocol_name": protocol_name,
            "role": role,
            "local_protocol": None,
            "type_map": {},
            "successful_method": None,
            "error": None
        }

        if not os.path.exists(file_path):
            result["error"] = f"文件不存在: {file_path}"
            return result

        if not file_path.endswith(".gt"):
            result["error"] = f"不是全局类型文件（.gt）: {file_path}"
            return result

        try:
            # 加载类型映射
            type_map = self.load_message_types(file_path)
            result["type_map"] = type_map

            # 读取全局类型
            global_type = get_gt_from_file(file_path)

            # 获取所有进程
            all_procs = global_type.get_procs()
            if role not in all_procs:
                result["error"] = f"角色 {role} 不在协议的进程列表中。可用进程: {', '.join(all_procs)}"
                return result

            # 根据投影方法创建评估对象
            if self.projection_method == "subset":
                eval_object = EvalSubsetProjection(global_type)
                projection_type = "subset"
            else:
                eval_object = EvalClassicalProjection(global_type)
                projection_type = "classical"

            # 执行投影
            proj = eval_object.project_onto(role)
            raw_projection = str(proj)

            # 注入类型信息
            typed_projection = self.inject_types_into_projection(raw_projection, type_map)

            result["local_protocol"] = typed_projection
            result["raw_local_protocol"] = raw_projection
            result["successful_method"] = projection_type

        except Exception as e:
            result["error"] = f"投影过程中发生错误: {str(e)}"

        return result

    def get_all_roles(self, file_path: str) -> List[str]:
        """获取全局类型文件中定义的所有角色。"""
        try:
            global_type = get_gt_from_file(file_path)
            return global_type.get_procs()
        except Exception as e:
            return []
