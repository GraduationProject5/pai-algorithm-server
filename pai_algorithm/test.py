from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation



res1='一、通过关于调整股票期权激励计划行权价格的议案：根据有关规定，公司２００７年度利润分配方案实施完成后，公司股票期权激励计划行权价格由６．４３元／股调整为６．２３元／股。二、通过关于制订公司《资金调拨管理办法》的议案。（来源：上海证券报）　证券声明：本频道资讯内容系转引自合作媒体及合作机构，不代表证券自身观点与立场，建议投资者对此资讯谨慎判断，据此入市，风险自担。'
res2=res1
res3=res1
corpus = [res1,res2,res3]

cntVector = CountVectorizer()
cntTf = cntVector.fit_transform(corpus)

lda = LatentDirichletAllocation(n_topics=2,
                                learning_offset=50.,
                                random_state=0)
docres = lda.fit_transform(cntTf)
print(docres)
