"""Add project folder to sys.path"""
import sys, os
# todo: could be more elegant
p = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(p)
del p
del os
del sys