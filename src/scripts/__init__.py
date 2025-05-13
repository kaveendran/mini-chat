import sys
import os

# Get the root directory path (parent directory of src)
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add root directory to Python path if not already present
if root_dir not in sys.path:
    sys.path.append(root_dir)
