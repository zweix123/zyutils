import unittest

from io import StringIO
import sys



# class Testzp(unittest.TestCase):
#     def check_(self, value: Any, expected_output: str) -> None:
#         with StringIO() as output:
#             sys.stdout = output
#             zp(value)
#             self.assertEqual(output.getvalue(), expected_output)
#         sys.stdout = sys.__stdout__
