# coding=utf-8
__author__ = 'qiangzi'
import codecs

# class fileIOprocessing:
'''
	文件读取
	&&
	文件写入
'''

def fileInput(path='',encode='utf-8',segtag=''):
	'''
	path:打开文件路径
	encode:文件编码格式
	segtag:文件分割标识符
	@:rtype List
	:param path:
	:param encode:
	:param segtag:
	'''
	inputFile=codecs.open(path,'r',encode)
	inputReader=inputFile.read()
	inputText=inputReader.split(segtag)
	inputFile.close()
	return inputText
def fileOutput(path='', encode='utf-8', writingcontent=None):
	'''
	path：文件存储路径
	encode：文件编码格式
	writingcontent：文件写入内容
					文件写入格式——list
					['单元行写入内容',......]
	@:rtype void
	:param path:
	:param encode:
	:param writingcontent:
	'''
	if writingcontent is None:
		writingcontent = []
	inputFile=codecs.open(path,'w',encode)
	for w in writingcontent:
		inputFile.write(w)
	inputFile.close()
	return
