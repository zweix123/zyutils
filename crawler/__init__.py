# 用于spider目录下的脚本去调用util目录下的封装库
import os, sys

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

del os, sys
