# coding=utf-8
__author__ = 'qiangzi'

from itertools import chain
import nltk
import sklearn
import codecs
import re


# print sklearn.__version__
# nltk.download()
# print nltk.corpus.conll2002.fileids()
# print type(nltk.corpus.conll2002.iob_sents('esp.train'))
# print len(nltk.corpus.conll2002.iob_sents('esp.train'))
# for s in nltk.corpus.conll2002.iob_sents('esp.train'):
# 	print s
# print nltk.corpus.conll2002.iob_sents('esp.train')[0]
# print list(nltk.corpus.conll2002.iob_sents('esp.train'))[10]
# train_sents = list(nltk.corpus.conll2002.iob_sents('esp.train'))
'''
CRF使用的语料目标格式如下：
[句子]+(单词，词性，实体标记)
=[(u'Melbourne', u'NP', u'B-LOC'),......]
'''

class corpusCleaning(object):
	'''原始语料清洗'''
	def extractionTokens(wt):
		'''对原始语料的  标识符和标签  进行抽取重组

		:rtype: var: tuple(word,tag)
		'''
		t=wt.split('/')
		# if t[0]=='<space>':
		# 	t[1]='NSB'
		# t[1]='NSB'
		return tuple(t)


	# if re.search(r'^\/+',s):
	# 	if s!='//':
	# 		print '第'+str(i+1)+'行'
	# 		print s
	# 		print textRaw[i-1]
	# 		print '~~~'*50
	# print '**~~~**'*50
	# if re.search(r'\/\/$',s) and len(s)!=2:
	# 	print '第'+str(i+1)+'行'
	# 	print s
	'''
！！！！！！！！！！！！！！！！！！原始语料主处理流程！！！！！！！！！！！！！！！！！！！！！！！！！！！
	'''
	rawInFile=codecs.open('rawCorpus/rawOrchid97.crp.utf.sentenceSeg.txt','r','utf-8')
	rawInReader=rawInFile.read()
	textRaw=rawInReader.split('\n')
	print len(rawInReader)
	print len(textRaw)

	chapterChannel=0
	paragraphChannel=0
	sentenceChannel=0
	p=1
	thaiSentencesCorpus=[]
	thaiParagraphsCorpus=[]
	thaiSentence=[]
	'''
	段落级语料准备
	'''
	for i in range(len(textRaw)):#迭代原始语料
		s = textRaw[i]
		s1 = []
		if i<len(textRaw)-1:
			s1=textRaw[i+1]
		if len(s)==2 and re.search(r'^\/\/',s)!=None and paragraphChannel==2:#段落结束标志控制
			t=(u'<space>',u'Sentence-Breaking')
			thaiSentence.append(t)
			if re.search(r'^\#P[0-9]',s1)!=None or i==len(textRaw)-1:
				thaiParagraphsCorpus.append(thaiSentence)
				paragraphChannel=0
				thaiSentence=[]
		if paragraphChannel==1:#根据语料情况，剔除每一句语料的第一行为整句的内容
			if re.search(r'\/[A-Z]*@?[A-Z]+$',s)!=None:
				paragraphChannel+=1

		if paragraphChannel==2 and re.search(r'\/[A-Z]*@?[A-Z]+$',s)!=None:#段落句子内容部分
			wt=extractionTokens(s)
			thaiSentence.append(wt)

		if re.search(r'^\#P[0-9]',s)!=None and paragraphChannel==0:#段落开始位置标志控制
			paragraphChannel=1


	'''
	句子级语料准备
	'''
	for i in range(len(textRaw)):#迭代原始语料
		s = textRaw[i]
		if len(s)==2 and re.search(r'^\/\/',s)!=None and sentenceChannel==2:#句子结束标志控制
			t=(u'<space>',u'Sentence-Breaking')
			thaiSentence.append(t)
			thaiSentencesCorpus.append(thaiSentence)
			thaiSentence=[]
			sentenceChannel=0
		if sentenceChannel==1:#根据语料情况，剔除每一句语料的第一行为整句的内容
			if re.search(r'\/[A-Z]*@?[A-Z]+$',s)!=None:
				sentenceChannel+=1

		if sentenceChannel==2:#句子内容部分
			wt=extractionTokens(s)
			thaiSentence.append(wt)

		if re.search(r'^\#[0-9]',s)!=None and sentenceChannel==0:#句子开始位置标志控制
			sentenceChannel=1

	rawInFile.close()
	'''
	原始语料处理结果——检验
	'''
	print 'thaiSentencesCorpus type :'
	print type(thaiSentencesCorpus)
	print 'thaiSentencesCorpus len :'
	print len(thaiSentencesCorpus)#23125句
	print 'thaiParagraphCorpus type :'
	print type(thaiParagraphsCorpus)
	print 'thaiParagraphCorpus len :'
	print len(thaiParagraphsCorpus)#
	# st=thaiSentencesCorpus[:100]
	# print len(st)
	# for j in range(len(st)):
	# 	print '第'+str(j+1)+'句'
	# 	print '((('*50
	# 	print type(st[j])
	# 	print len(st[j])
	# 	print st[j]
	# 	print ')))'*50

	'''
	原始语料处理结果——存储
	'''
	useSentOutFile=codecs.open('usefulCorpus/useSentCorpus.utf8.sentenceSeg.txt','w','utf-8')
	useParaOutFile=codecs.open('usefulCorpus/useParaCorpus.utf8.sentenceSeg.txt','w','utf-8')
	sents = thaiSentencesCorpus
	paras = thaiParagraphsCorpus
	writerSentList = []
	writerParaList = []

	#句子级存储
	for i in range(len(sents)):
		sentence = sents[i]
		wordAndTag=''
		for j in range(len(sentence)):
			wt = sentence[j]
			# if len(wt)!=2:
			# 	s1=sentence[j-1]
			# 	s2=sentence[j-2]
			# 	print '~~~'*50
			# 	print s2
			# 	print s1
			# 	for s in wt:
			# 		print s
			word=wt[0]
			tag=wt[1]
			wordAndTag+=wt[0]+u'|'+wt[1]+u'\n'
		wordAndTag+=str(u'||\n')
		writerSentList.append(wordAndTag)
	for w in writerSentList:
		useSentOutFile.writelines(w)

	#段落级存储
	for i in range(len(paras)):
		sentence = paras[i]
		wordAndTag=''
		for j in range(len(sentence)):
			wt = sentence[j]
			word = wt[0]
			tag = wt[1]
			wordAndTag+=wt[0]+u'|'+wt[1]+u'\n'
		wordAndTag+=str(u'||\n')
		writerParaList.append(wordAndTag)
	for w in writerParaList:
		useParaOutFile.writelines(w)

	useParaOutFile.close()
	useSentOutFile.close()






