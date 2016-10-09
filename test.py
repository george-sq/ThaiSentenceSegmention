# coding=utf-8
__author__ = 'qiangzi'


import nltk
from nltk.corpus import brown
from nltk.tag.util import untag

brown_tagged_sents = brown.tagged_sents(categories='news')
brown_sents = brown.sents(categories='news')

print "brown_tagged_sents's type:"
print type(brown_tagged_sents)
print "brown_tagged_sents's len:"
print len(brown_tagged_sents)
print brown_tagged_sents[:3]

print
print '*****'*50
print

print "brown_sents's type:"
print type(brown_sents)
print "brown_sents's len:"
print len(brown_sents)
print brown_sents[:3]

print
print '*****'*50
print

size = int(len(brown_tagged_sents)*0.9)
train_sents=brown_tagged_sents[:size]
test_sents=brown_tagged_sents[size:]

print
print '*****'*50
print

print 'train_sents type:'
print type(train_sents)
print 'train_sents len:'
print len(train_sents)
print 'train_sents :'
for s in train_sents[:10]:
	print 'type(s) :'
	print type(s)
	print 'trainsents :'
	print s

print
print '*****'*50
print

t0=nltk.DefaultTagger('NN')
t1=nltk.UnigramTagger(train_sents,backoff=t0)
t2=nltk.BigramTagger(train_sents,backoff=t1)

print 't0 type:'
print type(t0)
print 't1 type:'
print type(t1)
print 't2 type:'
print type(t2)

print
print '*****'*50
print

print 'test_sents type:'
print type(test_sents)
print 'test_sents len:'
print len(test_sents)

print
print '*****'*50
print
# for sent in test_sents:
# 	print sent

print 'brown_sents[0] type:'
print type(brown_sents[0])
print 'brown_sents[0] len:'
print len(brown_sents[0])
print 'brown_sents[0] :'
print brown_sents[0]


print 't2.evaluate :'
print t2.evaluate(test_sents)

print
print '*****'*50
print

print 'brown_sents[0]:'
print brown_sents[0]
sentences = brown_sents[0]

print 'sentences type:'
print type(sentences)
print 'sentences len:'
print len(sentences)

print
print '*****'*50
print
# for sent in sentences:
# 	print sent

print 'brown_sents[0] To Tags:'
print t2.tag_sents([sentences])

print
print '*****'*50
print

print
print '*****'*50
print

# print 'test_sents To Tags:'
# print t2.tag_sents(test_sents)

print
print '*****'*50
print

print t0,t1,t2

print
print '---****---'*50
print

for i in range(len(test_sents)):
	print str(i)+':'
	print 'test_sents['+str(i)+'] type:'
	print type(test_sents[i])
	print type(test_sents[i][0])
	print 'test_sents['+str(i)+'] :'
	print test_sents[i]
	print 'untag(test_sents['+str(i)+']) type:'
	print type(untag(test_sents[i]))
	print 'untag(test_sents['+str(i)+']):'
	print untag(test_sents[i])
	print 't2.tag_sents '+str(i)+' :'
	print t2.tag_sents([untag(test_sents[i])])
	print '^^^^^^^'*50

print
print '*****'*50
print
'''
Tn=nltk.***Tagger(训练语料，回退标注器)标注器
Tn.tag_*(训练语料)
Ngram使用的语料情况：
训练语料-->数据类型：[[句子=（单词,词性），...],...]
测试语料-->数据类型：[[句子=单词,单词...],...]

'''