# coding=utf-8
__author__ = 'qiangzi'



import codecs
import nltk
import fileIOprocessing
from nltk.tag.util import untag


def sentenceSeg(tagList):
	'''
	@:rtype List    -->     ['切分好的句子',...]，切分好的句子=word|...
	:param tagList:     -->     [段落[(word,tag),...],...]
	'''
	paraList = []
	for para in tagList:
		sentStr = ''
		sentList = []
		for i in range(len(para)):
			word = para[i][0]
			tag = para[i][1]
			sentStr += word + u'|'
			if tag == 'Sentence-Breaking' or i == len(para) - 1:
				sentList.append(sentStr)
				sentStr = ''
		paraList.append(sentList)

	return paraList


def evaluateTest(tagList, answerList):
	'''
	@:rtype List    -->     ['准确率','召回率','F值']
	:param tagList:     -->     [段落['句子',...],...]  句子=word|word|...
	:param answerList:     -->     [段落['句子',...],...]  句子=word|word|...
	'''
	paramlen = 0
	if len(answerList) != len(tagList):  # 错误参数提醒
		for i in range(10):
			print 'len(answerList)!=len(tagList)'
	else:
		paramlen = len(answerList)


	a = 0  # 实际样本总数
	b = 0  # 标记出的样本总数
	c = 0  # 正确标记的样本总数
	for i in range(len(answerList)):#获取实际样本总数
		a += len(answerList[i])
	for i in range(len(tagList)):#获取标记出的样本总数
		b += len(tagList[i])

	for i in range(paramlen):#获取正确标记的样本总数
		alist = answerList[i]
		tlist = tagList[i]
		for j in range(len(tlist)):
			sent=tlist[j]
			for s in alist:
				if sent==s:
					c+=1


	accuracy=round(c/float(b),9)      #       准确率
	recall=round(c/float(a),9)        #       召回率
	F=round((2*accuracy*recall)/(accuracy+recall),9)             #       F值
	return [accuracy,recall,F]

def spaceBreakingEvaluate(tagList, answerList):
	'''
	@:rtype List    -->     ['spaceCorrect','false-breaking','spaceBreaking召回率']
	:param tagList:     -->     [段落[（词，标签）,...],...]
	:param answerList:     -->     [段落[（词，标签）,...],...]

	spaceCorrect    =   totalCorrectSpace   /   totalSpace
	false-breaking  =   totalfalseSentenceBreaking  /   totalSpace
	spaceBreaking召回率    =   (totalSentenceBreaking   -   totalfalseSentenceBreaking)  /   totalSentenceBreaking

	'''
	totalSpace=0        #       所有空格符号<space>的总数
	totalCorrectSpace=0     #       所有正确标注的空格符号<space>的总数
	totalSentenceBreaking=0     #       所有句末空格符号<space>的总数
	totalfalseSentenceBreaking=0        #       错误标注句末空格符号<space>的总数
	if len(tagList)==len(answerList):#参数错误挺行
		lenParam=len(answerList)
		for i in range(lenParam):
			answerParagraph=answerList[i]
			tagParagraph=tagList[i]
			for j in range(len(answerParagraph)):
				answerWt=answerParagraph[j]
				tagWt=tagParagraph[j]
				if answerWt[0]=='<space>':      #     统计所有空格符号<space>的总数
					totalSpace+=1

					if answerWt[0]==tagWt[0] and answerWt[1]==tagWt[1]:     #       模型标注与答案一致
						totalCorrectSpace+=1        #       统计所有正确标注的空格符号<space>的总数

					if answerWt[1]=='Sentence-Breaking':        #       统计所有句末空格符号<space>的总数
						totalSentenceBreaking+=1
						if answerWt[1]!=tagWt[1]:       #       统计错误标注句末空格符号<space>的总数
							totalfalseSentenceBreaking+=1
	else:

		for i in range(10):
			print 'len(answerList)!=len(tagList)'

	spaceCorrect    =   round(totalCorrectSpace/float(totalSpace),9)
	falseBreaking  =   round(totalfalseSentenceBreaking/float(totalSpace),9)
	spaceBreakingRecall    =   round((totalSentenceBreaking-totalfalseSentenceBreaking)/float(totalSentenceBreaking),9)
	return [spaceCorrect,falseBreaking,spaceBreakingRecall]

