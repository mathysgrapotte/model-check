"""module for hyper parameter optimisation for the mnn model"""

import numpy as np
from ray import tune
from ray.air import session
from ray.tune.schedulers import ASHAScheduler
from scipy.stats import spearmanr
import numpy as np
import torch
import torch.optim as optim
import sys
from abc import ABC

sys.path.append("..")
from src.model.mnn_models import Net, BlockNet

class Trainer(ABC):
    """
    master class for hyper parameter optimisation for all pytorch models
    """

    def __init__(self, train_loader, test_loader, loss_function, eval_regression = spearmanr) -> None:
        super().__init__()
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.loss_function = loss_function
        self.eval_regression = eval_regression

    def train(self, model, optimizer):
        """
        performs one epoch of training

        @param model: the model to train
        @param optimizer: the optimizer to use

        @return: None
        """

        # setting device
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # setting model to train mode
        model.train()

        for batch_idx, (data, target, _) in enumerate(self.train_loader):
            # send data to device
            data, target = data.to(device), target.to(device)

            # convert data and target to float
            data, target = data.float(), target.float()

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            output = model(data)

            # reshape output to match target shape
            output = output.view(target.shape[0], -1)
            loss = self.loss_function(output, target)
            loss.backward()
            optimizer.step()

    def test_regression(self, model):
        """
        performs one epoch of testing

        @param model: the model to test

        @return: the test loss and accuracy
        """

        # setting device
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # setting model to eval mode
        model.eval()

        # initialize test loss
        test_loss = 0

        # initialize predictions and targets lists
        predictions, targets = [], []

        # no gradient calculation
        with torch.no_grad():
            for batch_idx, (data, target, _) in enumerate(self.test_loader):
                # send target to targets list (convert to list first)
                targets += target.view(-1).tolist()

                # send data to device
                data, target = data.to(device), target.view(-1,1).float().to(device)

                # convert data to float
                data = data.float()

                # forward pass
                output = model(data)

                # send predictions to predictions list
                predictions += output.view(-1).tolist()

                # calculate loss
                test_loss += self.loss_function(output, target).item()

        # average loss
        test_loss /= len(self.test_loader.dataset)

        # calculate accuracy
        accuracy = self.eval_regression(np.array(targets), np.array(predictions))[0]

        return test_loss, accuracy    

class MnnTrainer(Trainer):
    """
    class for using raytune to tune hyperparameters for mnn models
    """

    def __init__(self, train_loader, test_loader, loss_function, epochs=10, size=101, eval_regression=spearmanr) -> None:
        super().__init__(train_loader, test_loader, loss_function, eval_regression)
        self.size = size
        self.epochs = epochs

    def train_mnn(self, config):
        """
        trains a mnn model with the given config
        
        @param config: the config to use for training

        @return: None
        """
        # check if self.model exists, if it does not, initialize it, if it does, add a block of the relevant size
        if not hasattr(self, 'model'):
            self.model = Net(config['filter_size'], size=self.size)
        else:
            self.model.add_block(config['filter_size'])

        # intialize Adam optimizer with learning rate from config
        optimizer = optim.Adam(self.model.parameters(), lr=config['learning_rate'])

        # train model for self.epochs epochs
        for epoch in range(self.epochs):
            self.train(self.model, optimizer)

            # get test loss and accuracy
            test_loss, accuracy = self.test_regression(self.model)

            # report test loss and accuracy to session
            session.report({"accuracy": accuracy, "loss": test_loss})

    def tune(self, search_space, num_samples=3):
        """
        tunes the hyperparameters of the model

        @param search_space: the search space to use for tuning
        @param num_samples: the number of samples to use for tuning

        @return: a dictionary of the results
        """

        # assert that search space includes keys for filter_size, learning_rate and batch_size
        assert 'filter_size' in search_space.keys()
        assert 'learning_rate' in search_space.keys()
        assert 'batch_size' in search_space.keys()        

        tuner = tune.Tuner(
            self.train_mnn,
            tune_config=tune.TuneConfig(
                num_samples=num_samples,
                scheduler=ASHAScheduler(metric="accuracy", mode="max")
            ),
            param_space=search_space

        )

        results = tuner.fit()
        #dfs = {result.log_dir: result.metrics_dataframe for result in results}

        return results





