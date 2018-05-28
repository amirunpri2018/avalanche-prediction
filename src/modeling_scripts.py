import pandas as pd
import pickle
import numpy as np

def train_test_split_time(df, splitdate_str, y_col):
    splitdate = pd.to_datetime(splitdate_str)
    train_df = df[df.index <= splitdate]
    test_df = df[df.index > splitdate]

    # train set
    X_train = train_df.copy()
    y_train = X_train.pop(y_col)
    # test set
    X_test = test_df.copy()
    y_test = X_test.pop(y_col)

    return X_train, y_train, X_test, y_test

def train_estimator(est, params, X_train, y_train, standardize=True):
    if standardize:
        pipe = Pipeline([
            ('standardizer', StandardScaler()),
            ('est', est)])
        pipe.fit(X_train, y_train)
        return pipe.named_steps['est'], pipe.named_steps['standardizer']
    else:
        est.fit(X_train, y_train)
        return est, None

def predict_classifier(X_test, y_test, est, standardizer):
    ''' applies .predict() method of fitted classifier to X,y data '''
    pdb.set_trace()
    X_scaled = standardizer.transform(X_test)
    y_hat = est.predict(X_scaled)
    y_proba = est.predict_proba(X_scaled)
    importances = est.feature_importances_
    return y_hat, y_proba, importances

def print_scores(y_true, y_hat, method_list):
    for method in method_list:
        score = method(y_true, y_hat)
        print('test {} = {:0.3f}'.format(method.__name__, score))

def feature_importances(feat_list, label_list, color_list):
    feat_sort_l = []
    for item, label, color in zip(feat_list, label_list, color_list):
        names = list(item[0])
        importances = item[1]
        # make ordered list
        feat_sort_l.append(sorted(zip(names, importances),
                key=lambda x:abs(x[1]), reverse=True))
        # plot
        feat_importance_plot(names, importances, label, color, figsize=(6,6))
    return feat_sort_l