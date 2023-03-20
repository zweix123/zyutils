import os, glob

excluded = [
    os.path.basename(filepath)[:-3]
    for filepath in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
]
excluded = ["__init__", "test"]
__all__ = [
    os.path.basename(filepath)[:-3]
    for filepath in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
    if os.path.basename(filepath)[:-3] not in excluded
]

