"""
Assignment 05: Neural Networks
Author: Jiawei Wang

Build a multi-layer ANN for Iris Recognition
Attribute Information:
   1. sepal length in cm
   2. sepal width in cm
   3. petal length in cm
   4. petal width in cm
   5. class:
      -- Iris Setosa
      -- Iris Versicolour
      -- Iris Virginica
"""

import numpy as np
import random


# Load file
def load_file(filename):
    iris_data = list()
    with open(filename, 'r') as file:
        for line in file:
            line = line.split(',')
            del line[-1] # delete label
            for i in range(len(line)):
                line[i] = float(line[i])
            iris_data.append(line)
    return iris_data


# Normalize:  Turn iris_data into 0-centralized normal distribution
def normalize(iris_data):
    dataset_mean = []
    dataset_std_dev = []

    for i in range(len(iris_data[0])):
            # numpy.mean returns mean for each column
            mean = np.mean([row[i] for row in iris_data])
            # Compute the standard deviation of the given data (array elements) along the specified axis(if any)
            std_dev = np.std([row[i] for row in iris_data])

            dataset_mean.append(mean)
            dataset_std_dev.append(std_dev)

            # edit every element
            for j in range(len(iris_data)):
                iris_data[j][i] = (iris_data[j][i] - mean)/(std_dev * std_dev)
    return dataset_mean, dataset_std_dev, iris_data


# labelize iris_data
def labelizer(iris_data):
    # 150 lines of data
    # first 50 lines: Iris-setosa
    # middle 50 lines: Iris-versicolor
    # last 50 lines: Iris-virginica
    # label them
    for i in range(50):
        iris_data[i].append([1.0, 0.0, 0.0])
    for i in range(50, 100):
        iris_data[i].append([0.0, 1.0, 0.0])
    for i in range(100, 150):
        iris_data[i].append([0.0, 0.0, 1.0])

    # random shuffle order
    np.random.shuffle(iris_data)

    return iris_data


# Divide dataset into training, validation and testing data
def divider(iris_data):
    # 60 : 20 : 20
    training_data = iris_data[0:90]
    validation_data = iris_data[90:120]
    testing_data = iris_data[120:150]

    return training_data, validation_data, testing_data


#  seeds weights matrix with random values between 0 and 0.5
def seed_matrix(low, high):
    matrix = []
    for i in range(low):
        row = []
        for j in range(high):
            row.append(random.uniform(0, 0.5))
        matrix.append(row)
    return matrix


# Sigmoid activation function
def sigmoid_activation(potential):
    return 1.0/(1.0 + np.exp(-1 * potential))


# Potential function
def potential(input, weights):
    return np.dot(input, weights)


# Error function for outer layer of neurons
def error_outer(expected, output, output_potential):
    error = []
    for i in range(len(expected)):
        error.append(((expected[i] - output[i]) * sigmoid_deriv(output_potential[i])))
    return error


# Error function for all hidden neurons
def error_inner(weights, error, output_potential):
    layer_error = []
    for i in range(len(weights)):
        sum = 0
        for j in range(len(weights[i])):
            sum += weights[i][j] * error[j]
        layer_error.append(sum * sigmoid_deriv(output_potential[i]))
    return layer_error


# Calculate new weight matrix based on error produced
def calc_new_weight(weights, outputs, errors):
    #max = 1
    for i in range(len(weights)):
        for j in range(len(weights[0])):
            weights[i][j] = weights[i][j] + LEARNING_RATE * outputs[i] * errors[j]

    return weights


# Implement sum of squares to calculate error of data
def sum_of_sqs(target, output):
    ss = 0
    for i in range(len(target)):
        ss += (target[i] - output[i]) * (target[i] - output[i])
    return ss / 2.0


# Implement sigmoid activation function's derivative
def sigmoid_deriv(potential):
    return sigmoid_activation(potential) * (1.0 - sigmoid_activation(potential))


def check_results(output, expected):
    for i in range(len(expected)):
        if (output[i] > 0.5) != expected[i]:
            return False
    return True


def normalize_datapoint(data):
    for i in range(len(data)):
        data[i] = (float(data[i]) - dataset_mean[i])/(dataset_std_dev[i])
    return data


def test_input(data):
    p_inner = potential(data, input_hidden_matrix)
    hidden_output = sigmoid_activation(p_inner)
    p_outer = potential(hidden_output, hidden_output_matrix)
    return sigmoid_activation(p_outer)


# Main
iris_data = load_file('ANN - Iris data.txt')
dataset_mean, dataset_std_dev, iris_data = normalize(iris_data)

num_correct = 0
while num_correct/30 <= 0.8:
    iris_data = labelizer(iris_data)
    training_data, validation_data, testing_data = divider(iris_data)
    # seed weight matrices: 4×4 and 3×3 2d list
    input_hidden_matrix = seed_matrix(4, 4)
    hidden_output_matrix = seed_matrix(4, 3)

    LEARNING_RATE = 0.1
    num_epochs = 0
    done_training = False
    last_v_error = 100

    # Train ANN
    while not done_training:
        num_epochs += 1

        for row in training_data:
            # forward propagation
            ann_input = sigmoid_activation(np.array(row[0:4]))
            p_inner = potential(ann_input, input_hidden_matrix)
            hidden_output = sigmoid_activation(p_inner)
            p_outer = potential(hidden_output, hidden_output_matrix)
            output = sigmoid_activation(p_outer)

            # backward propagation
            error_o = error_outer(row[4], output, p_outer)
            error_h = error_inner(hidden_output_matrix, error_o, p_inner)
            hidden_output_matrix = calc_new_weight(hidden_output_matrix, hidden_output, error_o)
            input_hidden_matrix = calc_new_weight(input_hidden_matrix, ann_input, error_h)

        sum_v = 0
        v_error = 0

        # Validation
        for row in validation_data:

            # forward propagation
            p_inner = potential(row[0:4], input_hidden_matrix)
            hidden_output = sigmoid_activation(p_inner)
            p_outer = potential(hidden_output, hidden_output_matrix)
            output = sigmoid_activation(p_outer)

            # validation error
            v_error += sum_of_sqs(row[4], output)

        # stop training when the validation error starts to increase again
        if v_error/len(validation_data) > last_v_error:
            done_training = True
        else:
            last_v_error = v_error/len(validation_data)

    num_correct = 0
    for row in testing_data:
        p_inner = potential(row[0:4], input_hidden_matrix)
        hidden_output = sigmoid_activation(p_inner)
        p_outer = potential(hidden_output, hidden_output_matrix)
        output = sigmoid_activation(p_outer)

        if check_results(output, row[4]):
            num_correct += 1

print('ANN finished training in ' + str(num_epochs) + ' iterations.')
print('Accuracy for testing data: ' + str(num_correct/len(testing_data)))

# Prediction
done_inputs = False
while not done_inputs:
    print('------------------------------------------------')
    data = input('Please enter your data, each value separated with a space: ')
    data = data.split(' ')
    data = normalize_datapoint(data)
    result = test_input(data)
    if check_results(result, [1, 0, 0]):
        print("This is an Iris-setosa.")
    elif check_results(result, [0, 1, 0]):
        print("This is an Iris-versicolor.")
    elif check_results(result, [0, 0, 1]):
        print("This is an Iris-virginica.")
    else:
        print("No prediction based on these values.")
    loop = input('Would you like to try again? (yes/no) ')
    if loop == 'no' or loop == 'N' or loop == 'n':
        done_inputs = True
        print('ANN finished')
