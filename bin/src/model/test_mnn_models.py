"""module for testing the mnn_models module"""
import unittest
import torch
import sys
import os
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

    def test_getting_hyper_parameters(self):
        """test getting the hyper_parameters"""

        # first, generate a couple of filter sizes and one sequence size
        filter_sizes = [3, 5, 7]
        sequence_size = 101

        # then, initialize a net with the first filter size, and the sequence_size
        net = Net(filter_sizes[0], sequence_size)

        # then, add the other filter sizes
        for filter_size in filter_sizes[1:]:
            net.add_block(filter_size)

        # then, get the hyper_parameters
        hyper_parameters = net.get_hyper_parameters()

        # then, check if the hyper_parameters are correct
        self.assertEqual(hyper_parameters['filter_size'], filter_sizes)
        self.assertEqual(hyper_parameters['size'], sequence_size)

    def test_building_from_hyper_parameters(self):
        """test building a net from hyper_parameters"""

        # first, generate a couple of filter sizes and one sequence size
        filter_sizes = [3, 5, 7]
        sequence_size = 101

        # then, initialize a net with the first filter size, and the sequence_size
        net = Net(filter_sizes[0], sequence_size)

        # then, add the other filter sizes
        for filter_size in filter_sizes[1:]:
            net.add_block(filter_size)

        # then, get the hyper_parameters
        hyper_parameters = net.get_hyper_parameters()

        # then, build a new net from the hyper_parameters
        new_net = Net()
        new_net.build_model(hyper_parameters)

        # then, check if the new net is the same as the old net
        self.assertEqual(len(new_net.blocks), len(net.blocks))
        self.assertEqual(new_net.len, net.len)
        self.assertEqual(new_net.linear.in_features, net.linear.in_features)

        # then, check if the filter sizes are the same
        for i in range(len(net.blocks)):
            self.assertEqual(new_net.blocks[i].filter_size, net.blocks[i].filter_size)

        # then, check if the sequence size is the same
        self.assertEqual(new_net.size, net.size)

        # then, check if the last block is the same
        self.assertEqual(new_net.last_block.filter_size, net.last_block.filter_size)

    def test_saving_cnn_filter_logo(self):
        """test saving a cnn filter logo"""

        # first, generate a couple of filter sizes and one sequence size
        filter_sizes = [3, 5, 7]
        sequence_size = 101

        # then, initialize a net with the first filter size, and the sequence_size
        net = Net(filter_sizes[0], sequence_size)

        # then, save the logo of the convolution filter weight
        net.save_convolution_weight_logo_for_block("test")

        # check the the file exists
        
        self.assertTrue(os.path.exists("test_last.png"))

if __name__ == '__main__':
    unittest.main()