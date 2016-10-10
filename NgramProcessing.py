# coding=utf-8
__author__ = 'qiangzi'

import nltk
import codecs
import fileIOprocessing
from nltk.tag.util import untag
import performanceTest
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt



class NgramProcessing:
	'''
	'''
	'''
	训练语料准备
	'''
	# corpusText=fileIOprocessing.fileInput('usefulCorpus/useCorpus.utf8.sentenceSeg.txt','utf-8','||\n')
	corpusText=fileIOprocessing.fileInput('usefulCorpus/useParaCorpus.utf8.sentenceSeg.txt','utf-8','||\n')

	print type(corpusText)
	print len(corpusText)
	trainCorpus=[]
	for sent in corpusText:
		wt = sent.split('\n')
		sentence=[]
		for i in range(len(wt)):
			if wt[i]!='':
				word_tag=wt[i].split('|')
				word=word_tag[0]
				tag=word_tag[1]
				t = (word,tag)
				sentence.append(t)
		trainCorpus.append(sentence)

	'''
	训练语料校验
	'''
	# print
	# for s in trainCorpus:
	# 	for wt in s:
	# 		for x in wt:
	# 			print x,
	# 	print

	'''
	训练语料 和 测试语料 分割
	'''

	size = int(len(trainCorpus)*0.9)
	trainSents=trainCorpus[:size]
	num=0
	for p in trainSents:
		for t in p:
			if t[0]=='<space>' and t[1]=='Sentence-Breaking':
				num+=1
	print 'trainSents\'s num=',num
	num=0
	testSents=trainCorpus[size:]
	for p in testSents:
		for t in p:
			if t[0]=='<space>' and t[1]=='Sentence-Breaking':
				num+=1
	print 'testSents\'s num=',num
	print '训练语料 和 测试语料 的分割位置索引：'
	print size


	answerList=performanceTest.sentenceSeg(testSents)       #       分句答案
	'''
	Ngram工具调用
	'''
	t0=nltk.DefaultTagger('NN')
	t1=nltk.UnigramTagger(trainSents,backoff=t0)
	t2=nltk.BigramTagger(trainSents,backoff=t1)
	t3=nltk.TrigramTagger(trainSents,backoff=t2)
	t4=nltk.TrigramTagger(trainSents,backoff=t3)
	tn=nltk.NgramTagger(n=10,train=trainSents,backoff=t3)

	print
	print '*****'*50
	print
	print '实验三：Ngram模型参数n的优化'
	print
	print '*****'*50
	print
	print '~!~*~!~'*50
	print
	'''
			测试n在[5,20]区间内时，试验性能的变化
	'''
	T=[]        #       模型  存储List
	T1=[]        #       模型  存储List
	tagPrecision=[]     #       模型标注准确率 存储List
	tagResult=[]        #       模型标注结果  存储List
	spacePerformance=[]     #       模型空格标注结果性能  存储List
	sentenceSegResult=[]       #       模型句子切分结果  存储List
	sentenceSegPerformance=[]       #       模型句子切分结果性能  存储List
	print '模型训练step1开始：'
	for i in range(21):     #       模型训练
		n=i
		# #无回退实验
		# if n!=0:
		# 	T.append(nltk.NgramTagger(n=n,train=trainSents))

		#逐次降元回退
		if n!=0:
			if n==1:
				T1.append(nltk.NgramTagger(n=n,train=trainSents,backoff=t0))
			else:
				T1.append(nltk.NgramTagger(n=n,train=trainSents,backoff=T1[-1]))

	print '模型训练step2开始：'
	for i in range(21):     #       模型训练
		n=i
		#最佳回退实验
		if n!=0:
			T.append(nltk.NgramTagger(n=n,train=trainSents,backoff=T1[2]))


	print '模型训练结束!!!!!!'

	print '模型准确率评估：'
	for t in T:     #       模型标注准确率
		tagPrecision.append(t.evaluate(testSents))
	print '准确率评估结束!!!!!!'

	print '标注测试开始：'
	for t in T:        #       模型标注结果
		result=[]
		for para in testSents:
			result.append(t.tag(untag(para)))
		tagResult.append(result)
	print '标注结束!!!!!!'

	print '标注性能评估：'
	for r in tagResult:     #       模型空格标注结果性能
		spacePerformance.append(performanceTest.spaceBreakingEvaluate(r,testSents))
	print '标注性能评估结束!!!!!!'

	print '句子切分开始：'
	for r in tagResult:       #       模型句子切分结果
		sentenceSegResult.append(performanceTest.sentenceSeg(r))
	print '句子切分结束!!!!!!'

	print '句子切分效果评估:'
	for r in sentenceSegResult:       #       模型句子切分结果性能
		sentenceSegPerformance.append(performanceTest.evaluateTest(r,answerList))
	print '句子切分效果评估结束!!!!!!'

	print '模型标注准确率','~~~'*50
	for i in range(20):
		print i,'   :   ',tagPrecision[i]
	print
	print '模型空格标注结果性能','~~~'*50
	for i in range(20):
		print i,'   :   ',spacePerformance[i][0],spacePerformance[i][1],spacePerformance[i][2]
	print '模型句子切分结果性能','~~~'*50
	for i in range(20):
		print i,'   :   ',sentenceSegPerformance[i][0],sentenceSegPerformance[i][1],sentenceSegPerformance[i][2]
	# '''
	# 结果绘图
	#
	# 		tagPrecision=[]     #       模型标注准确率 存储List
	# 		spacePerformance=[]     #       模型空格标注结果性能  存储List
	# 		sentenceSegPerformance=[]       #       模型句子切分结果性能  存储List
	#
	# '''
	# pl.title('Experiment Performance')        #       图表的标题
	# pl.xlabel('Ngram Iterm  \'n\'')       #       X轴的名称
	# pl.ylabel('Performance Evaluation \'%\'')       #       Y轴的名称
	#
	# x=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]        #       X轴内容
	# y1=tagPrecision       #       标注准确率曲线
	# plot1=pl.plot(x,y1)
	# pl.legend(['tagPrecision'])
	# pl.show()
	# # pl.savefig('processingResult/figureResult/tagPrecision.png')
	# pl.close()
	#
	# y2=spacePerformance       #       空格标注性能曲线
	# y21=[]
	# y22=[]
	# y23=[]
	# for i in y2:
	# 	y21.append(i[0])        #       spaceCorrect
	# 	y22.append(i[1])        #       falseBreaking
	# 	y23.append(i[2])        #       spaceBreakingRecall
	#
	# plot21=plt.plot(x,y21)
	# plot22=plt.plot(x,y22,'r')
	# plot23=plt.plot(x,y23,'g')
	# # plt.plot('')
	# # 曲线说明
	# pl.legend([plot21, plot22,plot23], ('spaceCorrect', 'falseBreaking','spaceBreakingRecall'))
	# pl.show()
	# # pl.savefig('processingResult/figureResult/spacePerformance.png')
	# pl.close()
	#
	# y3=sentenceSegPerformance       #       句子切分性能曲线
	# y31=[]
	# y32=[]
	# y33=[]
	# for i in y3:
	# 	y31.append(i[0])        #       句子切分准确率
	# 	y32.append(i[1])        #       句子切分召回率
	# 	y33.append(i[2])        #       句子切分F值
	#
	# plot31=pl.plot(x,y31)
	# plot32=pl.plot(x,y32,'r')
	# plot33=pl.plot(x,y33,'g')
	# # 曲线说明
	# pl.legend([plot31, plot32,plot33],('sentenceSegPrecision', 'sentenceSegRecall','sentenceSegValueOfF'))
	# pl.show()
	# # pl.savefig('processingResult/figureResult/sentenceSegPerformance.png')
	# pl.close()
	print
	print '~!~*~!~'*50

	#
	# '''
	# 初步标记结果的性能评估
	# '''
	# # print
	# # print '*****'*50
	# # print
	# # print '单词标记性能结果'
	# # print
	# # print '*****'*50
	# # print
	# # print '~!~*~!~'*50
	# # print 'DefaultTagger 的   准确度性能评估：'
	# # print t0.evaluate(testSents)
	# # print '一元Ngram算法=UnigramTagger 的   准确度性能评估：'
	# # print t1.evaluate(testSents)
	# # print '二元Ngram算法=BigramTagger  的   准确度性能评估：'
	# # print t2.evaluate(testSents)
	# # print '三元Ngram算法TrigramTagger  的   准确度性能评估：'
	# # print t3.evaluate(testSents)
	# # print 'N=10元Ngram算法TrigramTagger  的   准确度性能评估：'
	# # print tn.evaluate(testSents)
	# # print '~!~*~!~'*50
	#
	# '''
	# 测试集标注结果
	# '''
	# tagResult1=[]
	# tagResult2=[]
	# tagResult3=[]
	# tagResultN=[]
	# for para in testSents:
	# 	tagResult3.append(t3.tag(untag(para)))
	# for para in testSents:
	# 	tagResult2.append(t2.tag(untag(para)))
	# for para in testSents:
	# 	tagResult1.append(t1.tag(untag(para)))
	# for para in testSents:
	# 	tagResultN.append(tn.tag(untag(para)))
	#
	# print
	# print '*****'*50
	# print
	# print '实验一：段落标记性能结果'
	# print
	# print '*****'*50
	# print
	# '''
	# 段落标记性能结果
	# '''
	# tagEvaluate1=performanceTest.spaceBreakingEvaluate(tagResult1,testSents)
	# tagEvaluate2=performanceTest.spaceBreakingEvaluate(tagResult2,testSents)
	# tagEvaluate3=performanceTest.spaceBreakingEvaluate(tagResult3,testSents)
	# tagEvaluateN=performanceTest.spaceBreakingEvaluate(tagResultN,testSents)
	# print '~!~*~!~'*50
	# print '一元Ngram算法  的   性能评估：'
	# for i in range(len(tagEvaluate1)):
	# 	if i==0:
	# 		print 'spaceCorrect = ',tagEvaluate1[i],
	# 	elif i==1:
	# 		print 'false-breaking = ',tagEvaluate1[i],
	# 	else:
	# 		print 'spaceBreaking召回率 = ',tagEvaluate1[i],
	# print
	# print '二元Ngram算法  的   性能评估：'
	# for i in range(len(tagEvaluate2)):
	# 	if i==0:
	# 		print 'spaceCorrect = ',tagEvaluate2[i],
	# 	elif i==1:
	# 		print 'false-breaking = ',tagEvaluate2[i],
	# 	else:
	# 		print 'spaceBreaking召回率 = ',tagEvaluate2[i],
	# print
	# print '三元Ngram算法  的   性能评估：'
	# for i in range(len(tagEvaluate3)):
	# 	if i==0:
	# 		print 'spaceCorrect = ',tagEvaluate3[i],
	# 	elif i==1:
	# 		print 'false-breaking = ',tagEvaluate3[i],
	# 	else:
	# 		print 'spaceBreaking召回率 = ',tagEvaluate3[i],
	# print
	# print 'N=10元Ngram算法  的   性能评估：'
	# for i in range(len(tagEvaluateN)):
	# 	if i==0:
	# 		print 'spaceCorrect = ',tagEvaluateN[i],
	# 	elif i==1:
	# 		print 'false-breaking = ',tagEvaluateN[i],
	# 	else:
	# 		print 'spaceBreaking召回率 = ',tagEvaluateN[i],
	# print
	# print '~!~*~!~'*50
	# # print 'testSents type:'
	# # print type(testSents)
	# # print 'testSents len:'
	# # print len(testSents)
	# print
	# print '*****'*50
	# print
	# print '实验二：句子切分性能结果'
	# print
	# print '*****'*50
	# print
	# '''
	# 句子切分结果处理
	# '''
	#
	# tagList1=performanceTest.sentenceSeg(tagResult1)
	# tagList2=performanceTest.sentenceSeg(tagResult2)
	# tagList3=performanceTest.sentenceSeg(tagResult3)
	# tagListN=performanceTest.sentenceSeg(tagResultN)
	#
	# '''
	# 句子切分的性能查看
	# '''
	# sentEvaluate1=performanceTest.evaluateTest(tagList1,answerList)
	# sentEvaluate2=performanceTest.evaluateTest(tagList2,answerList)
	# sentEvaluate3=performanceTest.evaluateTest(tagList3,answerList)
	# sentEvaluateN=performanceTest.evaluateTest(tagListN,answerList)
	# print '~!~*~!~'*50
	# print '一元Ngram算法  的   性能评估：'
	# for i in range(len(sentEvaluate1)):
	# 	if i==0:
	# 		print '准确率=',sentEvaluate1[i],
	# 	elif i==1:
	# 		print '召回率=',sentEvaluate1[i],
	# 	else:
	# 		print 'F值=',sentEvaluate1[i],
	# print
	# print '二元Ngram算法  的   性能评估：'
	# for i in range(len(sentEvaluate2)):
	# 	if i==0:
	# 		print '准确率=',sentEvaluate2[i],
	# 	elif i==1:
	# 		print '召回率=',sentEvaluate2[i],
	# 	else:
	# 		print 'F值=',sentEvaluate2[i],
	# print
	# print '三元Ngram算法  的   性能评估：'
	# for i in range(len(sentEvaluate3)):
	# 	if i==0:
	# 		print '准确率=',sentEvaluate3[i],
	# 	elif i==1:
	# 		print '召回率=',sentEvaluate3[i],
	# 	else:
	# 		print 'F值=',sentEvaluate3[i],
	# print
	# print 'N=10元Ngram算法  的   性能评估：'
	# for i in range(len(sentEvaluateN)):
	# 	if i==0:
	# 		print '准确率=',sentEvaluateN[i],
	# 	elif i==1:
	# 		print '召回率=',sentEvaluateN[i],
	# 	else:
	# 		print 'F值=',sentEvaluateN[i],
	# print
	# print '~!~*~!~'*50
	#
	# print
	# print '*****'*50
	# print
	# print '实验三：Ngram模型参数n的优化'
	# print
	# print '*****'*50
	# print
	# print '~!~*~!~'*50
	# print
	# '''
	# 		测试n在[5,20]区间内时，试验性能的变化
	# '''
	# T=[]        #       模型  存储List
	# tagPrecision=[]     #       模型标注准确率 存储List
	# tagResult=[]        #       模型标注结果  存储List
	# spacePerformance=[]     #       模型空格标注结果性能  存储List
	# sentenceSegResult=[]       #       模型句子切分结果  存储List
	# sentenceSegPerformance=[]       #       模型句子切分结果性能  存储List
	# print '模型训练开始：'
	# for i in range(16):     #       模型训练
	# 	n=i+5
	# 	if n==5:
	# 		T.append(nltk.NgramTagger(n=n,train=trainSents,backoff=t4))
	# 	else:
	# 		T.append(nltk.NgramTagger(n=n,train=trainSents,backoff=T[-1]))
	# print '模型训练结束!!!!!!'
	#
	# print '模型准确率评估：'
	# for t in T:     #       模型标注准确率
	# 	tagPrecision.append(t.evaluate(testSents))
	# print '准确率评估结束!!!!!!'
	#
	# print '标注测试开始：'
	# for t in T:        #       模型标注结果
	# 	result=[]
	# 	for para in testSents:
	# 		result.append(t.tag(untag(para)))
	# 	tagResult.append(result)
	# print '标注结束!!!!!!'
	#
	# print '标注性能评估：'
	# for r in tagResult:     #       模型空格标注结果性能
	# 	spacePerformance.append(performanceTest.spaceBreakingEvaluate(r,testSents))
	# print '标注性能评估结束!!!!!!'
	#
	# print '句子切分开始：'
	# for r in tagResult:       #       模型句子切分结果
	# 	sentenceSegResult.append(performanceTest.sentenceSeg(r))
	# print '句子切分结束!!!!!!'
	#
	# print '句子切分效果评估:'
	# for r in sentenceSegResult:       #       模型句子切分结果性能
	# 	sentenceSegPerformance.append(performanceTest.evaluateTest(r,answerList))
	# print '句子切分效果评估结束!!!!!!'
	#
	# print
	# print '~!~*~!~'*50
	#
	# '''
	# 对比实验结果：将结果写入本地文件
	# '''
	# sent0=''
	# sent1=''
	# sent2=''
	# sent3=''
	# sentN=''
	# for p in range(len(answerList)):
	#
	# 	for s in range(len(answerList[p])):
	# 		sent0+=answerList[p][s]+'\n'
	# 	for s in range(len(tagList1[p])):
	# 		sent1+=tagList1[p][s]+'\n'
	# 	for s in range(len(tagList2[p])):
	# 		sent2+=tagList2[p][s]+'\n'
	# 	for s in range(len(tagList3[p])):
	# 		sent3+=tagList3[p][s]+'\n'
	# 	for s in range(len(tagListN[p])):
	# 		sentN+=tagListN[p][s]+'\n'
	#
	# 	sent0+=u'||'+'\n'
	# 	sent1+=u'||'+'\n'
	# 	sent2+=u'||'+'\n'
	# 	sent3+=u'||'+'\n'
	# 	sentN+=u'||'+'\n'
	#
	# fileIOprocessing.fileOutput('processingResult/answerSentenceSeg.txt','utf-8',sent0)
	# fileIOprocessing.fileOutput('processingResult/tagSentenceSeg1.txt','utf-8',sent1)
	# fileIOprocessing.fileOutput('processingResult/tagSentenceSeg2.txt','utf-8',sent2)
	# fileIOprocessing.fileOutput('processingResult/tagSentenceSeg3.txt','utf-8',sent3)
	# fileIOprocessing.fileOutput('processingResult/tagSentenceSegN.txt','utf-8',sentN)
	# print
	#
	#
	#
