import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
import sklearn.metrics as metrics
import joblib
models={'LR':LinearRegression(),
        'Lasso':Lasso()
}

def train(X_train,y_train,modelName):
    return models[modelName].fit(X_train,y_train)
    
def saveModel(model,path):
    file = open(f'{path}', 'wb')
    joblib.dump(model, file)
    file.close()

def predict(X_test,model):
    return model.predict(X_test)


def regression_results(y_true, y_pred):

    # Regression metrics
    explained_variance=metrics.explained_variance_score(y_true, y_pred)
    mean_absolute_error=metrics.mean_absolute_error(y_true, y_pred) 
    mse=metrics.mean_squared_error(y_true, y_pred) 
    #mean_squared_log_error=metrics.mean_squared_log_error(y_true, y_pred)
    median_absolute_error=metrics.median_absolute_error(y_true, y_pred)
    r2=metrics.r2_score(y_true, y_pred)

    #print('explained_variance: ', round(explained_variance,4))    
    #print('mean_squared_log_error: ', round(mean_squared_log_error,4))
    #print('r2: ', round(r2,4))
    #print('MAE: ', round(mean_absolute_error,4))
    #print('MSE: ', round(mse,4))
    #print('RMSE: ', round(np.sqrt(mse),4))
    return f'RMSE: {round(np.sqrt(mse),4)}'

def eval(y_test,y_pred):
    return regression_results(y_test, y_pred)