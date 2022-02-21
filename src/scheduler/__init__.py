import os
import sys

curr_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(curr_path, "../"))
sys.path.append(src_path)