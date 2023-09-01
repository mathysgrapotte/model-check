"""module for testing the mnn_models module"""
import unittest
import torch
import sys
from torch import nn
from torch.nn import functional as F
sys.path.append("..")
from src.model.mnn_models import BlockNet, Net

class TestBlockNet(unittest.TestCase):
    """test class for the BlockNet class"""
    def setUp(self):
        """sets up the test cases"""
        self.block = BlockNet(3)

    def test_forward(self):
        """tests the forward method"""
        x = torch.randn(1, 4, 101)
        output = self.block(x)
        self.assertEqual(output.shape, torch.Size([1, 1]))

    def test_forward_batch(self):
        """tests the forward method with a batch"""
        x = torch.randn(5, 4, 101)
        output = self.block(x)
        self.assertEqual(output.shape, torch.Size([5, 1]))

class TestNet(unittest.TestCase):
    """test class for the Net class"""
    def setUp(self):
        """sets up the test cases"""
        self.net = Net(3)

    def test_add_block(self):
        """tests the add_block method"""
        self.net.add_block(3)
        self.assertEqual(len(self.net.blocks), 1)
        self.assertEqual(self.net.len, 1)
        self.assertEqual(self.net.linear.in_features, 2)

    def test_forward(self):
        """tests the forward method"""
        x = torch.randn(1, 4, 101)
        output = self.net(x)
        self.assertEqual(output.shape, torch.Size([1, 1]))

    def test_forward_multiple_blocks(self):
        """tests the forward method with multiple blocks"""
        self.net.add_block(3)
        x = torch.randn(1, 4, 101)
        output = self.net(x)
        self.assertEqual(output.shape, torch.Size([1, 1]))

if __name__ == '__main__':
    unittest.main()