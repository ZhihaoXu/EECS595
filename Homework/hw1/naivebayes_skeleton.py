# For Programming Problem 2, we will implement a naive Bayesian sentiment classifier which learns to classify movie reviews as positive or negative.
#
# Please implement the following functions below: train(), predict(), evaluate(). Feel free to use any Python libraries such as sklearn, numpy, etc. 
# DO NOT modify any function definitions or return types, as we will use these to grade your work. However, feel free to add new functions to the file to avoid redundant code (e.g., for preprocessing data).
#
# *** Don't forget to additionally submit a README_2 file as described in the assignment. ***

import nltk
import os
from tqdm import tqdm
from math import log

# Description: Load training & testing data
# Inputs: path of the directory
# Outputs: A list containing all the sentences
def load_data(path):
    sentence_files = os.listdir(path)
    sentences = []
    for file in sentence_files:
        if not os.path.isdir(path + "/" + file):
            f = open(path + "/" + file, encoding='ISO-8859–1')
            line = f.readline()
            sentences.append(line)
            f.close()
    return sentences

# Description: compute the conditional probability
# Inputs: a list of sentences
# Outputs: A dictionary containing the conditional probabilities
def token_count(sentences):
    count_dict = {}
    tokenizer = nltk.RegexpTokenizer(r'[a-zA-Z]+')
    for sentence in tqdm(sentences):
        tokens = tokenizer.tokenize(sentence)
        for token in tokens:
            if token in count_dict.keys():
                count_dict[token] += 1
            else:
                count_dict[token] = 1

    V = len(count_dict.keys())
    Count = sum(count_dict.values())
    prob_dict = {}
    for token in count_dict.keys():
        prob_dict[token] = (count_dict[token] + 1) / (Count + V)
    prob_dict['not_matched'] = 1 / (Count + V)
    return prob_dict

# Description: Trains the naive Bayes classifier.
# Inputs: String for the file location of the training data (the "training" directory).
# Outputs: A list representing the trained model with 3 dictionary in it. [prior, train_pos_dict, train_neg_dict]
def train(training_path):
    # load and preprocess data
    train_pos = load_data('HW1_data/training/pos')
    train_neg = load_data('HW1_data/training/neg')

    # compute prior
    prior = {}
    prior['pos'] = len(train_pos)/(len(train_pos) + len(train_neg))
    prior['neg'] = len(train_neg)/(len(train_pos) + len(train_neg))

    # prior conditional probability
    train_pos_dict = token_count(train_pos)
    train_neg_dict = token_count(train_neg)

    trained_model = []
    trained_model.append(prior)
    trained_model.append(train_pos_dict)
    trained_model.append(train_neg_dict)
    return trained_model


# Description: Runs prediction of the trained naive Bayes classifier on the test set, and returns these predictions.
# Inputs: An object representing the trained model (whatever is returned by the above function), and a string for the file location of the test data (the "testing" directory).
# Outputs: An object representing the predictions of the trained model on the testing data, and an object representing the ground truth labels of the testing data.
def predict(trained_model, testing_path):
    test_data_pos = load_data(testing_path + '/pos')
    test_data_neg = load_data(testing_path + '/neg')
    test_data = test_data_pos + test_data_neg
    ground_truth = [1] * len(test_data_neg) + [0]*len(test_data_neg)
    tokenizer = nltk.RegexpTokenizer(r'[a-zA-Z]+')
    model_predictions = []
    for sentence in tqdm(test_data):
        pos_prob = log(trained_model[0]['pos'])
        neg_prob = log(trained_model[0]['neg'])
        tokens = tokenizer.tokenize(sentence)
        for token in tokens:
            if token in trained_model[1].keys():
                pos_prob += log(trained_model[1][token])
            else:
                pos_prob += log(trained_model[1]["not_matched"])
            
            if token in trained_model[2].keys():
                neg_prob += log(trained_model[2][token])
            else:
                neg_prob += log(trained_model[2]["not_matched"])
        if pos_prob > neg_prob:
            model_predictions.append(1)
        else:
            model_predictions.append(0)
    return model_predictions, ground_truth


# Description: Evaluates the accuracy of model predictions using the ground truth labels.
# Inputs: An object representing the predictions of the trained model, and an object representing the ground truth labels for the testing data.
# Outputs: Floating-point accuracy of the trained model on the test set.
def evaluate(model_predictions, ground_truth):
    cum = 0
    for i in range(len(model_predictions)):  
        if model_predictions[i]==ground_truth[i]:
            cum += 1
    accuracy = cum / len(model_predictions)
    return accuracy


# GRADING: We will be using lines like these to run your functions (from a separate file). You can run the file naivebayes.py in the command line (e.g., "python naivebayes.py") to verify that your code works as expected for grading.
TRAINING_PATH='HW1_data/training' # TODO: replace with your path
TESTING_PATH='HW1_data/testing' # TODO: replace with your path

trained_model = train(TRAINING_PATH)
model_predictions, ground_truth = predict(trained_model, TESTING_PATH)
accuracy = evaluate(model_predictions, ground_truth)
print('Accuracy: %s' % str(accuracy))
