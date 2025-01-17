import scipy.io as spi
import numpy as np
import matplotlib.pyplot as plt
import time

mat=spi.loadmat("base_apprentissage.mat")
data_train=np.transpose(mat['data'])
label_train=np.array(mat['label'])[0] #label: chiffre numérisé
label_train=label_train.astype(int) #Les labels sont stockés en flottants, on les convertit en entiers

mat = spi.loadmat("base_test.mat")
data_test = np.transpose(mat['data'])
label_test = np.array(mat['label'])[0]
label_test =label_test.astype(int)

# ajout overfit
data_test_overfit=data_train[:2000]

tuples=[]
for i in range(28):
    for j in range(28):
        tuples+=[(i,j)]
        
tuples_x=np.array([tuples[i][0] for i in range(784)])
tuples_y=np.array([tuples[i][1] for i in range(784)])

def smooth(v):
    P=np.reshape(v,(28,28))
    def p(x,y):
        S=[P[i,j]*np.e**(-((x-i)**2+(y-j)**2)/(2*0.9**2)) for i,j in tuples]
        return sum(S)
    return p(tuples_x,tuples_y)

def smooth_fcl(v):
    P = np.reshape(v, (28,28))
    x, y = tuples_x, tuples_y
    return sum([P[i,j]*np.e**(-((x-i)**2+(y-j)**2)/(2*0.9**2)) for i,j in tuples])

smooth_train=[smooth_fcl(data_train[i]) for i in range(8000)]
smooth_test=[smooth_fcl(data_test[i]) for i in range(2000)]

#ajout overfit
label_test_overfit=label_train[:2000]
smooth_test_overfit=[smooth_fcl(data_train[i]) for i in range(2000)]

def T_X(v):
    P=np.reshape(v,(28,28))
    P_=np.gradient(P)[0]
    return np.reshape(P_,(1,-1))[0]

p_x_train=[T_X(smooth_train[i]) for i in range(8000)]
p_x_test=[T_X(smooth_test[i]) for i in range(2000)]

#ajout overfit
p_x_test_overfit=[T_X(smooth_test_overfit[i]) for i in range(2000)]

def T_Y(v):
    P=np.reshape(v,(28,28))
    P_=np.gradient(P)[1]
    return np.reshape(P_,(1,-1))[0]

p_y_train=[T_Y(smooth_train[i]) for i in range(8000)]
p_y_test=[T_Y(smooth_test[i]) for i in range(2000)]

#ajout overfit
p_y_test_overfit=[T_Y(smooth_test_overfit[i]) for i in range(2000)]
