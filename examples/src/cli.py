#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
命令行接口示例
"""

import click
import logging
import sys
from pathlib import Path

from core.processor import Processor

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """文件处理工具命令行接口"""
    pass


@cli.command("process")
@click.option("-i", "--input", required=True, help="输入文件路径")
@click.option("-o", "--output", required=True, help="输出文件路径")
@click.option("--json", is_flag=True, help="是否处理JSON文件")
def process(input, output, json):
    """处理文件"""
    try:
        processor = Processor()
        
        if json:
            processor.process_json(input, output)
        else:
            processor.process_file(input, output)
            
        logger.info(f"处理完成，输出文件: {output}")
        return 0
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(cli())