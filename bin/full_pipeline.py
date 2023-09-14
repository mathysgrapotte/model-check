from src.data.generate_fasta import *
from src.data.pytorch_loaders import *
from src.learner.tune_trainer import *
from src.model.mnn_models import *
from torch.utils.data import DataLoader

# this is a simple test pipeline
if __name__ == '__main__':
    config = {'filter_size':tune.sample_from(lambda _: np.random.randint(1, 10)),
              'learning_rate':tune.loguniform(1e-4, 1e-1),
              'batch_size':tune.choice([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])}
    generateFasta = False
    # generate a simple motif fasta file 
    path_to_fasta = 'test.fasta'
    if generateFasta:
        dna_sequence_length = 100
        motif_tag = 5
        non_motif_tag = 0
        motif = 'aattttttttttttaa'

        singleFixedMotifDataset = GenerateSingleFixedMotifDataset(path_to_fasta, dna_sequence_length, motif, motif_tag, non_motif_tag)

        # write the fasta file
        singleFixedMotifDataset.write_fasta()

    # load the fasta file using the pytorch fasta loader
    pytorch_loader = fastaDataset(path_to_fasta)

    train_set = DataLoader(pytorch_loader, batch_size=10, shuffle=True)

    # check if we can access the first batch
    for batch_idx, (data, target, sequence_names) in enumerate(train_set):
        print(data.shape)
        print(target.shape)
        print(sequence_names)
        break


    # define the loss function
    loss_function = nn.MSELoss()

    # define the model
    model = Net(filter_size=4, size=100)

    # define the optimizer
    optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

    # initiate the tune trainer
    tune_trainer = Trainer(train_set, train_set, loss_function)

    # make sure that the model is training (i.e. the weights are changing) after running a tune_trainer.train() call
    # compare the weights before and after training
    print('weights before training')
    print(list(model.parameters())[0])
    print('weights after training')
    tune_trainer.train(model=model, optimizer=optimizer)
    print(list(model.parameters())[0])

    # run a testing run from the tune_trainer
    print('testing run')
    print(tune_trainer.test_regression(model=model))

    mnn_trainer = MnnTrainer(train_loader=train_set, test_loader=train_set, loss_function=loss_function, epochs=1, size=100)

    # run a tune run
    dfs = mnn_trainer.tune(search_space=config)
    best_result = dfs.get_best_result(metric='accuracy', mode='max')
    checkpoint = best_result.checkpoint.to_dict()
    # printing accuracy of the best model
    print("printing accuracy of the best model")
    print(best_result.metrics)
    print("printing model")
    print(mnn_trainer.model)
    print("model has been printed")









