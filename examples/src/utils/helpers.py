#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
辅助工具函数
"""

import os
import json
import datetime
from pathlib import Path


def ensure_dir(directory):
    """
    确保目录存在，如果不存在则创建
    
    Args:
        directory: 目录路径
    """
    Path(directory).mkdir(parents=True, exist_ok=True)
    return directory


def get_timestamp():
    """
    获取当前时间戳
    
    Returns:
        格式化的时间戳字符串
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def load_json_file(file_path):
    """
    加载JSON文件
    
    Args:
        file_path: JSON文件路径
        
    Returns:
        JSON数据对象
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json_file(data, file_path):
    """
    保存数据到JSON文件
    
    Args:
        data: 要保存的数据
        file_path: 保存路径
    """
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return file_path