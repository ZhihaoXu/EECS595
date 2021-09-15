# Homework 1 Programming 2
Author: Zhihao Xu  

In the Programming Problem 2, we are asked to implement a naive Bayesian sentiment classifier which learns to classify movie reviews as positive or negative. The whole program consist of three parts:
- **Training Module**  
  In this module, I implement two helper functions:

    ```{python}
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
    ```
  First function is `load_data`, given path of the data as input, return positive/negative data a list of sentences.

    ```{python}
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
    ```
  Second function is `token_count`, which is used to compute the conditional probability. The formular is given by
  $$
  P(w_k | c_j) = \frac{n_k + 1}{n + |V|},
  $$
  where $n_k$ is the number of occurrences of $w_k$ in class $c_j$, n is the total number of words in $c_j$ and $|V|$ is the number of distinct words in $c_j$. Here I alse use the regular expression `/[a-zA-Z]+/` to remove numbers, symbol and other meaningless characters.

    ```{python}
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
    ```
  Above is the main function of training module, which returns a list containing three dictionaries. The format of the output is [prior, train_pos_dict, train_neg_dict].


- **Testing Module**  
  The main function in this part is given by 
    ```{python}
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
    ```
  The decision function here used is 
  $$
  c_{NB} = \argmax_{c_j \in C} \left(\log P(c_j) + \sum_{i \in positions}\log P(x_i|c_j)\right ).
  $$
  Since the conditional probability is really small, here I use the sum of log probability to avoid the computation limit of the software.

- **Evaluation Module**  
This module is relatively simple, I just compare the model prediction and the ground truth one by one and compute the accuracy. The final accuracy I get here is 0.807.  

    ```{python}
    def evaluate(model_predictions, ground_truth):
        cum = 0
        for i in range(len(model_predictions)):  
            if model_predictions[i]==ground_truth[i]:
                cum += 1
        accuracy = cum / len(model_predictions)
        return accuracy
    ```