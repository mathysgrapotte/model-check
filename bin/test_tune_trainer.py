"""testing module for tune trainer"""
import sys
import unittest
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

from ray import tune
from torch.utils.data import DataLoader

sys.path.append("..")
from src.learner.tune_trainer import MnnTrainer
from src.model.mnn_models import BlockNet, Net

class TestTuneTrainer(unittest.TestCase):
    """test class for the TuneTrainer class"""
    def setUp(self):
        """sets up the test cases"""
        # create a train loader with data, targets and sequence ids
        data = torch.randn(100, 4, 101)
        targets = torch.randn(100, 1)
        sequence_ids = torch.randint(0, 10, (100,))
        dataset = list(zip(data, targets, sequence_ids))
        self.train_loader = DataLoader(dataset, batch_size=10, shuffle=True)
        self.trainer = MnnTrainer(self.train_loader, self.train_loader, nn.MSELoss())

    def test_train(self):
        """tests the train method"""
        model = Net(3)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        self.trainer.train(model, optimizer)

    def test_train_mnn(self):
        """tests the train_mnn method"""
        config = {'filter_size':3, 'learning_rate':0.001, 'batch_size':10}
        self.trainer.train_mnn(config)

    def test_test_regression(self):
        """tests the test_regression method"""
        model = Net(3)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
        self.trainer.train(model, optimizer)
        test_loss, accuracy = self.trainer.test_regression(model)
        self.assertIsInstance(test_loss, float)
        self.assertIsInstance(accuracy, float)

    def test_eval_regression(self):
        """tests the eval_regression method"""
        targets = np.random.rand(100)
        predictions = np.random.rand(100)
        spearmanr, pearsonr = self.trainer.eval_regression(targets, predictions)
        self.assertIsInstance(spearmanr, float)
        self.assertIsInstance(pearsonr, float)


    def test_tune(self):
        config = {'filter_size':tune.sample_from(lambda _: np.random.randint(1, 10)), 
                  'learning_rate':tune.loguniform(1e-4, 1e-1), 
                  'batch_size':tune.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])}
        self.trainer.tune(config, num_samples=1)


if __name__ == '__main__':
    unittest.main()

