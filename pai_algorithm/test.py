import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

X_train=np.array([[-7, -1,1], [-2, -1,1], [1, 1,1], [2, 1,1]])
y_train=np.array([3, 3, 2, 6])
lr = KNeighborsClassifier(n_neighbors=4)
re=lr.fit(X_train, y_train)

#r = re.score(X_train,y_train)
print(re.predict(X_train))
#print('Score: %.2f' % lr.score(X_train, y_train))
print("=========sigmoid函数转化的值，即：概率p=========")
print(re.predict_proba(X_train))     #sigmoid函数转化的值，即：概率p
