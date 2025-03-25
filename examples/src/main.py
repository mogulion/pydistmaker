#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
示例应用程序入口点
"""

import argparse
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


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="文件处理示例应用")
    parser.add_argument(
        "-i", "--input", 
        required=True, 
        help="输入文件路径"
    )
    parser.add_argument(
        "-o", "--output", 
        required=True, 
        help="输出文件路径"
    )
    parser.add_argument(
        "--json", 
        action="store_true", 
        help="是否处理JSON文件"
    )
    
    args = parser.parse_args()
    
    try:
        processor = Processor()
        
        if args.json:
            processor.process_json(args.input, args.output)
        else:
            processor.process_file(args.input, args.output)
            
        logger.info(f"处理完成，输出文件: {args.output}")
        return 0
    except Exception as e:
        logger.error(f"处理失败: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())