import numpy as np
from sklearn.linear_model import LogisticRegression

X_train=np.array([[-1, -1,1], [-2, -1,1], [1, 1,1], [2, 1,1]])
y_train=np.array([1, 1, 2, 3])
lr = LogisticRegression()
re=lr.fit(X_train, y_train)

r = re.score(X_train,y_train)
print(lr.predict(X_train))
print('Score: %.2f' % lr.score(X_train, y_train))
print("=========sigmoid函数转化的值，即：概率p=========")
print(re.predict_proba(X_train))     #sigmoid函数转化的值，即：概率p
