"""
Use: 
from util import *  # import

file_util.xxx  # use
"""

import os, glob

# 全部导入
current_dir = os.path.dirname(__file__)
module_files = glob.glob(os.path.join(current_dir, "*.py"))
module_names = [
    os.path.basename(f)[:-3]
    for f in module_files
    if not f.endswith("__init__.py") and not f.endswith("test.py")
]
__all__ = [module_name for module_name in module_names]

# 分别导入
# from . import file_util, net_util...
