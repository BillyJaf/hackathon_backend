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
    optimiser = optim.Adam(net.parameters(), lr=0.001)

    ## Default prediction score
    prediction =  torch.tensor(0.5, dtype=torch.float32)

    ## 10000 epochs:
    for i in range(int(10000/numDays)):
        for day in dayData[:-1]:
            ## Reset the gradient
            optimiser.zero_grad()

            ## Run the input values through the net
            output = net(torch.tensor(day["x"], dtype=torch.float32)).squeeze()

            ## Calculate the loss given the user input
            loss = criterion(output, torch.tensor(day["y"], dtype=torch.float32))

            ## Back propagate and update
            loss.backward()
            optimiser.step()
    
    ## Make a prediction on how you should have felt after your days inputs
    prediction = net(torch.tensor(dayData[-1]["x"], dtype=torch.float32))

    ## Create the inverse model to optimise for the input values:

    # Start with random input values:
    inputs = torch.rand((1, inputSize), requires_grad=True)
    # inputs = torch.randn(1, inputSize, requires_grad=True)

    # Reset the optimiser with a larger lr (inrelation to the epoch count)
    # Note that now the optimisation is for the input values, not the output
    optimiser = optim.Adam([inputs], lr=0.001)

    # Define a loss function (mean squared error between model output and desired output)
    criterion = torch.nn.MSELoss()

     # Target output (1 in our case as we want to maximise)
    maxOutput = torch.tensor(1, dtype=torch.float32)

    # Perform optimisation with 1000 epochs
    for i in range(10000):
        ## Reset the gradient
        optimiser.zero_grad()

        ## Run the input values through the net
        output = net(inputs).squeeze()
        
        ## Calculate the loss from the current inputs
        loss = criterion(output, maxOutput)

        ## Back propagate and update
        loss.backward()
        optimiser.step()

    inputsOutput = inputs.squeeze().tolist()
    ## Convert the data to frontend form:
    for i in range(len(inputsOutput)):
        inputsOutput[i] = float(bound(inputsOutput[i]))
        if (not (i == 3 or i == 9)):
            inputsOutput[i] = float(round(inputsOutput[i]))

    return [inputsOutput, prediction.item()]

def sigmoid(x):
    return 1/(1 + np.exp(-x))

def bound(x):
    if (x > 1):
        return 1
    if (x < 0):
        return 0
    return x

