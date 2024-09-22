# SkinTune Application Backend - ANU Hackathon 2024

In collaboration with [@jamesnoonan](https://github.com/jamesnoonan), [@chethin](https://github.com/Chethin) and [@kpate123](https://github.com/kpate123).

An AB-testing framework application for people with skin issues, suitable for IOS.

## Use-Case:

SkinTune’s demographic are people who have mild-moderate skin issues that would typically require 
multiple consultations to find a somewhat trivial solution. This app removes the need for professional
opinions, which often results in guesswork regardless. Passively take charge of your health by spending 
less than one minute a day journaling your schedule and let SkinTune help find your tailored treatment.

## Neural-Network:

To avoid a brute-force or minimum-distance-vector solution, PyTorch libraries are used to implement a neural network.
The chosen method is stochastic-gradient-descent with Adam's algorithm and a learning rate of `lr=0.001` to optimise inputs.
The network also features a dynamic calculation of epochs (in relation to input size) to ensure speed.

The network features:
10 input nodes, representing the user inputs: 
```
    "cream1": boolean,
    "cream2": boolean,
    "tookHotShower": boolean,
    "relativeHumidity": float,
    "stress": boolean,
    "facewash1": boolean,
    "facewash2": boolean,
    "makeup": boolean,
    "soap": boolean,
    "hoursInside": float
```

From this nodes, a rectified linear unit (ReLU) is applied to maintain gradients.
1 hidden layer with 7 nodes (in line with these [reccommendations](https://medium.com/geekculture/introduction-to-neural-network-2f8b8221fbd3)).
Following this, a sigmoid function is applied to ensure the output node has a `float` between `(0,1)`.

1 output node, representing the predicted skin-feeling:
```
    "skinFeelRating": float
```

## Data-Flow:


## Installation:

For installation / use of the application, please see the [frontend](https://github.com/BillyJaf/hackathon_frontend).
