import torch
import numpy as np 
from torch import nn
from torch import optim

class NeuralNetwork(nn.Module):

    def __init__(self, inputs: int):
        super(NeuralNetwork, self).__init__()
        hiddenLayerCount: int = int(1 + 2*inputs/3)

        self.fc1 = nn.Linear(inputs, hiddenLayerCount)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hiddenLayerCount, 1)
        self.sigmoid = nn.Sigmoid()
 
    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.sigmoid(x)
        return x
    

# Main function
#
# Parameters
# ----------
# dayData: dict[]
#     List of dict:
#     "x" : float[]
#     "y" : float
#
# Returns
# -------
# [inputs: float[], prediction: float]
#     inputs is the set of inputs that maximises the happiness
#     prediction is the models prediction of your day, defaults to 0.5 on the first day.
# Raises
# ------
# Exception: "No input data provided."
#     No input data was provided.

def main(dayData):
    
    ## Train the model on the input data:

    numDays = len(dayData)

    ## If there is no data provided, the model can't be created
    if (numDays == 0):
        raise Exception("No input data provided.") 
    
    inputSize = len(dayData[0]["x"])
    net = NeuralNetwork(inputSize)

    ## Mean-Squared-Error
    criterion = nn.MSELoss()

    ## Adam optimisation for stochastic gradient descent
    ## High learning rate on small input size, minimum learning rate of 0.001 (default optim lr)
    ## lr=max(0.1/numDays, 0.001)
    optimiser = optim.Adam(net.parameters(), lr=0.005)

    ## Default prediction score
    prediction =  torch.tensor(0.5, dtype=torch.float32)

    ## If there is more than one day of data, predict how the user feels
    if (numDays > 1): 
        for day in dayData[:-1]:
            ## 1000 epochs:
            for i in range(5000):
                ## Reset the gradient
                optimiser.zero_grad()

                ## Run the input values through the net
                output = net(torch.tensor(day["x"], dtype=torch.float32)).squeeze()


                ## Calculate the loss given the user input
                loss = criterion(output, torch.tensor([day["y"]], dtype=torch.float32))

                ## Back propagate and update
                loss.backward()
                optimiser.step()
        
        ## Make a prediction on how you should have felt after your days inputs
        prediction = net(torch.tensor(dayData[-1]["x"], dtype=torch.float32)).squeeze()

        ## Now feed the most recent day after this prediction
        for i in range(5000):
            optimiser.zero_grad()
            output = net(torch.tensor(dayData[-1]["x"], dtype=torch.float32)).squeeze()
            loss = criterion(output, torch.tensor([dayData[-1]["y"]], dtype=torch.float32))
            loss.backward()
            optimiser.step()
    
    ## Otherwise, this is the first input, maintain the default prediction of 0.5
    else:
        for i in range(5000):
            optimiser.zero_grad()
            output = net(torch.tensor(dayData[0]["x"], dtype=torch.float32)).squeeze()
            loss = criterion(output, torch.tensor([dayData[0]["y"]], dtype=torch.float32))
            loss.backward()
            optimiser.step()




    ## Create the inverse model to optimise for the input values:

    # Start with random input values:
    inputs = torch.randn(1, inputSize, requires_grad=True)

    # Reset the optimiser with a larger lr (inrelation to the epoch count)
    # Note that now the optimisation is for the input values, not the output
    optimiser = optim.Adam([inputs], lr=0.005)

    # Define a loss function (mean squared error between model output and desired output)
    criterion = torch.nn.MSELoss()

     # Target output (1 in our case as we want to maximise)
    maxOutput = torch.tensor([1], dtype=torch.float32)

    # Perform optimisation with 10000 epochs
    for i in range(10000):
        ## Reset the gradient
        optimiser.zero_grad()

        ## Run the input values through the net
        output = net(inputs)
        
        ## Calculate the loss from the current inputs
        loss = criterion(output, maxOutput)

        ## Back propagate and update
        loss.backward()
        optimiser.step()

        inputsOutput = inputs.detach().squeeze().tolist()
        sigmoidOutputs = [sigmoid(x) for x in inputsOutput]

    return [sigmoidOutputs, prediction.item()]

def sigmoid(x):
    return 1/(1 + np.exp(-x))

