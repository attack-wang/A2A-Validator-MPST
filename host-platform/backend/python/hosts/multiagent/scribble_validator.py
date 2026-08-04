import os
import subprocess
from typing import Any


class ScribbleValidator:
    """Scribble 协议工具，用于读取 Scribble 协议文件."""

    def __init__(self, scribblec_path: str = "scribblec"):
        """初始化 Scribble 工具."""
        self.scribblec_path = scribblec_path

    def read_protocol_file(self, file_path: str) -> dict[str, Any]:
        """读取并解析 Scribble 协议文件.

        Args:
            file_path: Scribble 协议文件的路径

        Returns:
            包含协议文件内容的字典，包含以下键：
            - file_path: 文件的完整路径
            - file_name: 文件名
            - content: 文件内容（字符串）
            - exists: 文件是否存在
            - error: 如果文件不存在或读取失败，返回错误信息
        """
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



    def list_protocols_in_directory(self, directory_path: str) -> list[dict[str, Any]]:
        """列出目录中的所有 Scribble 协议文件.

        Args:
            directory_path: 目录路径

        Returns:
            协议文件列表，每个元素包含 file_path 和 file_name
        """
        protocols = []

        if not os.path.exists(directory_path) or not os.path.isdir(directory_path):
            return protocols

        for file_name in os.listdir(directory_path):
            if file_name.endswith('.scr'):
                file_path = os.path.join(directory_path, file_name)
                protocols.append({
                    "file_name": file_name,
                    "file_path": file_path
                })

        return sorted(protocols, key=lambda x: x["file_name"])

    def get_protocol_summary(self, content: str) -> dict[str, Any]:
        """从协议内容中提取摘要信息.

        Args:
            content: Scribble 协议文件内容

        Returns:
            包含摘要信息的字典：
            - module_name: 模块名称
            - global_protocols: 全局协议列表
            - roles: 角色列表
        """
        summary = {
            "module_name": None,
            "global_protocols": [],
            "roles": []
        }

        lines = content.split('\n')
        for line in lines:
            line = line.strip()

            if line.startswith('module '):
                module_end = line.find(';')
                if module_end > 0:
                    summary["module_name"] = line[7:module_end].strip()

            elif line.startswith('global protocol '):
                parts = line.split('(')[0] if '(' in line else line
                protocol_name = parts.replace('global protocol ', '').strip()
                if protocol_name:
                    summary["global_protocols"].append(protocol_name)

            elif 'role ' in line and 'as ' in line:
                role_start = line.find('role ')
                role_end = line.find(' as ')
                if role_start >= 0 and role_end > role_start:
                    role_name = line[role_start + 5:role_end].strip()
                    if role_name:
                        summary["roles"].append(role_name)

        return summary

    def project_protocol(self, file_path: str, protocol_name: str, role: str) -> dict[str, Any]:
        """将全局协议投影为指定角色的局部协议.

        Args:
            file_path: Scribble 协议文件的路径
            protocol_name: 要投影的协议名称
            role: 要投影的角色名称

        Returns:
            包含投影结果的字典：
            - file_path: 原始文件路径
            - protocol_name: 协议名称
            - role: 投影的角色
            - local_protocol: 生成的局部协议
            - error: 错误信息（如果投影失败）
        """
        result = {
            "file_path": file_path,
            "protocol_name": protocol_name,
            "role": role,
            "local_protocol": None,
            "error": None
        }

        if not os.path.exists(file_path):
            result["error"] = f"文件不存在: {file_path}"
            return result

        if not file_path.endswith(".scr"):
            result["error"] = f"不是 Scribble 协议文件（.scr）: {file_path}"
            return result

        try:
            # 获取scribblec.sh所在目录
            scribble_dir = os.path.dirname(self.scribblec_path)
            lib_dir = os.path.join(scribble_dir, "lib")

            if not os.path.exists(lib_dir):
                result["error"] = f"找不到lib目录: {lib_dir}"
                return result

            # 构建classpath
            jars = [
                "antlr-runtime.jar",
                "antlr.jar",
                "commons-io.jar",
                "scribble-ast.jar",
                "scribble-cli.jar",
                "scribble-codegen.jar",
                "scribble-core.jar",
                "scribble-main.jar",
                "scribble-parser.jar"
            ]

            classpath = ";".join([os.path.join(lib_dir, jar) for jar in jars])

            # 构建Java命令，直接执行不通过脚本
            java_cmd = [
                "java",
                "-cp",
                classpath,
                "org.scribble.cli.CommandLine",
                file_path,
                "-project",
                protocol_name,
                role
            ]

            # 执行Java命令
            proc = subprocess.Popen(
                java_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout, stderr = proc.communicate(timeout=30)

            if proc.returncode == 0:
                result["local_protocol"] = stdout if stdout else "投影成功"
                result["successful_method"] = "java"
            else:
                result["error"] = f"Java命令执行失败: {stderr if stderr else f'返回码: {proc.returncode}'}"

        except Exception as e:
            result["error"] = f"投影过程中发生错误: {str(e)}"

        return result
