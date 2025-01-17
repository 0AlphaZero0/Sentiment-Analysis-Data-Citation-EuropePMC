#!/usr/bin/env python
#-*- coding: utf-8 -*-
# THOUVENIN Arthur athouvenin@outlook.fr
# 01/04/2019
########################
#
# revoir la façon de calculer l'accuracy
#
#
#
#
######

import codecs
import numpy as np
import pandas as pd
import time

from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras import layers
from keras import models
from keras import backend

from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split,StratifiedKFold
from sklearn import metrics

import warnings
warnings.filterwarnings('ignore')

##################################################    Variables     ###################################################
# files
dataset="Dataset23.csv"
result_output="ResultCNN.csv"
# parameters
average="macro"
class_weight={
	0 : .9,
	1 : .8,
	2 : .3}
epochs=2
k_cross_val=5
ngram_range=(1,3)
random_state=42
vocab_size=1000
# instances
skf=StratifiedKFold(
	n_splits=k_cross_val,
	random_state=random_state)
lemmatizer=WordNetLemmatizer()
stemmer=SnowballStemmer(
	'english',
	ignore_stopwords=True)
# other variables
Section_num_str,SubType_num_str,Figure_num_str="Section_num","SubType_num","Figure_num"
PreCitation_str,Citation_str,PostCitation_str,completeCitation="PreCitation","Citation","PostCitation","CompleteCitation",
featuresList=[
	Section_num_str,
	SubType_num_str,
	Figure_num_str,
	completeCitation]
	# 'Categories_num']
target_names=[
	"Background",
	"Creation",
	"Use"]
################################################    Functions     #################################################
#
def lemma_word(word):
	"""This function take as args word and return its lemma
	
	Args : 
		- word : (str) a word that could lemmatize by the WordNetLemmatizer from nltk.stem
	
	Return : 
		- word : (str) a lemma of the word gives in args
	"""
	return lemmatizer.lemmatize(word)
#
def lemma_tokenizer(doc):
	""" This function take as args a doc that could be lemmatize.

	Args : 
		- doc : (str) a string that can be tokenize by the word_tokenize of nltk library
	
	Return : 
		- tokens : (list) a list of tokens where each token corresponds to a lemmatized word 
	"""
	tokens=word_tokenize(doc)
	tokens=[lemma_word(t) for t in tokens]
	return tokens
#
def stem_word(word):
	"""This function take as args word and return its stem
	
	Args : 
		- word : (str) a word that could be stemmed by the SnowballStemmer from nltk.stem.snowball
	
	Return : 
		- word : (str) a stem of the word gives in args
	"""
	return stemmer.stem(word)
#
def stem_tokenizer(doc):
	""" This function take as args a doc that could be stemmed.

	Args : 
		- doc : (str) a string that can be tokenize by the word_tokenize of nltk library
	
	Return : 
		- tokens : (list) a list of tokens where each token corresponds to a stemmed word 
	"""
	tokens=word_tokenize(doc)
	tokens=[stem_word(t) for t in tokens]
	return tokens
#
def tokenizer(doc):
	""" This function take as args a doc that could be tokenize.

	Args :
		- doc : (str) a string that can be tokenize by the word_tokenize of nltk library
	
	Return : 
		- tokens : (list) a list of tokens where each token corresponds to a word
	"""
	tokens=word_tokenize(doc)
	return tokens
#
def calc_score(vectorizer,approach,dimension):
	fold=0
	f1_score_mean,precision_mean,recall_mean,accuracy_mean=0,0,0,0
	val_acc_mean,val_loss_mean=0,0
	while fold < len(f1_score_list):
		f1_score_mean+=f1_score_list[fold]
		precision_mean+=precision_list[fold]
		recall_mean+=recall_list[fold]
		accuracy_mean+=accuracy_list[fold]
		val_acc_mean+=val_acc_list[fold]
		val_loss_mean+=val_loss_list[fold]
		fold+=1
	f1_score_mean=round(f1_score_mean/len(f1_score_list),3)
	precision_mean=round(precision_mean/len(precision_list),3)
	recall_mean=round(recall_mean/len(recall_list),3)
	accuracy_mean=round(accuracy_mean/len(accuracy_list),3)
	val_acc_mean=round(val_acc_mean/len(val_acc_list),3)
	val_loss_mean=round(val_loss_mean/len(val_loss_list),3)
	val_loss,val_acc=model.evaluate(X_val_dtm,y_val)
	result=model.predict(X_val_dtm)
	y_pred_class_val=[]
	for sample in result:
		y_pred_class_val.append(np.argmax(sample))
	f1_score=round(metrics.f1_score(y_val,y_pred_class_val,average=average)*100,3)
	precision=round(metrics.precision_score(y_val,y_pred_class_val,average=average)*100,3)
	recall=round(metrics.recall_score(y_val,y_pred_class_val,average=average)*100,3)
	# accuracy=round(metrics.accuracy_score(y_val,y_pred_class_val)*100,3)
	if vectorizer=="Tfidf":
		appr=approach[1]+" "+approach[2]
	else:
		appr=approach.name
	print(
		"\nVALIDATION SET : \n",
		metrics.classification_report(y_val,y_pred_class_val,target_names=target_names),
		"Method : "+str(appr),
		"\nF1_score : "+str(f1_score),
		"\tPrecision : "+str(precision),
		"\tRecall : "+str(recall),
		"\tVal_acc : "+str(round(val_acc*100,3)),
		"\tVal_loss : "+str(round(val_loss,3)),
		"\tTime : "+str(round(end-start,3))+" sec",
		"\n#######################################################")
	print(
		metrics.classification_report(y_test,y_pred_class,target_names=target_names),
		"Method : "+str(appr),
		"\nF1_score : "+str(f1_score_mean),
		"\tPrecision : "+str(precision_mean),
		"\tRecall : "+str(recall_mean),
		"\tVal_acc : "+str(val_acc_mean),
		"\tVal_loss : "+str(val_loss_mean),
		"\tTime : "+str(round(end-start,3))+" sec",
		"\n#######################################################")
	output_file=codecs.open(
		filename=result_output,
		mode='a',
		encoding='utf8')
	output_file.write(str(f1_score))
	output_file.write("\t")
	output_file.write(str(precision))
	output_file.write("\t")
	output_file.write(str(recall))
	output_file.write("\t")
	output_file.write(str(round(val_acc*100,3)))
	output_file.write("\t")
	output_file.write(str(round(val_loss,3)))
	output_file.write("\t")
	output_file.write(str(f1_score_mean))
	output_file.write("\t")
	output_file.write(str(precision_mean))
	output_file.write("\t")
	output_file.write(str(recall_mean))
	output_file.write("\t")
	output_file.write(str(val_acc_mean*100))
	output_file.write("\t")
	output_file.write(str(val_loss_mean))
	output_file.write("\t")
	if vectorizer=="Tfidf":
		if approach[2]=="Token":
			output_file.write("True")#Token
			output_file.write("\t")
			output_file.write("False")#Ngram
		else:
			output_file.write("False")#Token
			output_file.write("\t")
			output_file.write("True")#Ngram
		output_file.write("\t")
		if approach[1]=="Raw":
			output_file.write("True")#Raw
			output_file.write("\t")
			output_file.write("False")#Lemma
			output_file.write("\t")
			output_file.write("False")#Stem
		elif approach[1]=="Lemma":
			output_file.write("False")#Raw
			output_file.write("\t")
			output_file.write("True")#Lemma
			output_file.write("\t")
			output_file.write("False")#Stem
		else:#STEM
			output_file.write("False")#Raw
			output_file.write("\t")
			output_file.write("False")#Lemma
			output_file.write("\t")
			output_file.write("True")#Stem
		output_file.write("\t")
		output_file.write("True")#Tfidf
		output_file.write("\t")
		output_file.write("False")#Embedding
	else:
		output_file.write("True")#Token
		output_file.write("\t")
		output_file.write("False")#Ngram
		output_file.write("\t")
		if completeCitation in str(approach.name):
			output_file.write("True")#Raw
			output_file.write("\t")
			output_file.write("False")#Lemma
			output_file.write("\t")
			output_file.write("False")#Stem
		elif "lemma" in str(approach.name):
			output_file.write("False")#Raw
			output_file.write("\t")
			output_file.write("True")#Lemma
			output_file.write("\t")
			output_file.write("False")#Stem
		else:
			output_file.write("False")#Raw
			output_file.write("\t")
			output_file.write("False")#Lemma
			output_file.write("\t")
			output_file.write("True")#Stem
		output_file.write("\t")
		output_file.write("False")#Tfidf
		output_file.write("\t")
		output_file.write("True")#Embedding
	output_file.write("\t")
	output_file.write(str(dimension))#dimension
	output_file.write("\t")
	output_file.write(str(round(end-start,3)))#time
	output_file.write("\n")
	output_file.close()
	
###################################################    Main     ###################################################
#
data=pd.read_csv(#read dataset
	filepath_or_buffer=dataset,
	header=0,
	sep="\t")
#
data[completeCitation]=data[[PreCitation_str,Citation_str,PostCitation_str]].apply(lambda x : '{}{}'.format(x[0],x[1]), axis=1)# concatenate in 1 column (PreCitation+Citation+PostCitation)
#
data["Categories_num"]=data.Categories.map({#Categories to numerical values
	"Background":0,
	"Creation":1,
	"Use":2})
#
data[Figure_num_str]=data.Figure.map({# Figure feature to numerical values
	True:1,
	False:0})
## Section feature to numerical values
sectionDict={}
index=1
for section in data.Section:
	if section not in sectionDict:
		sectionDict[section]=index
		index+=1
data[Section_num_str]=data.Section.map(sectionDict)
## Subtype feature to numerical values
subTypeDict={}
index=1
for subType in data.SubType:
	if subType not in subTypeDict:
		subTypeDict[subType]=index
		index+=1
data[SubType_num_str]=data.SubType.map(subTypeDict)
# Creation of two pandas column one with stem words and the other with lemma from completeCitation
lemma_citation=[]
stem_citation=[]
for citation in data[completeCitation]:
	lemma_citation.append(" ".join(lemma_tokenizer(citation)))
	stem_citation.append(" ".join(stem_tokenizer(citation)))
data["lemma_citation"]=lemma_citation
data["stem_citation"]=stem_citation
# List of approach for embedding
approaches=[
	data[completeCitation],
	data["lemma_citation"],
	data["stem_citation"]]
# List of Approach for Tfidf
combinations_tfidf=[
	[TfidfVectorizer(tokenizer=tokenizer),"Raw","Token"],
	[TfidfVectorizer(tokenizer=tokenizer),"Stem","Token"],
	[TfidfVectorizer(tokenizer=tokenizer),"Lemma","Token"],
	[TfidfVectorizer(tokenizer=tokenizer,ngram_range=ngram_range),"Raw","Ngram"],
	[TfidfVectorizer(tokenizer=tokenizer,ngram_range=ngram_range),"Stem","Ngram"],
	[TfidfVectorizer(tokenizer=tokenizer,ngram_range=ngram_range),"Lemma","Ngram"]]
# Creation of result file
output_file=codecs.open(
	filename=result_output,
	mode='w',
	encoding='utf8')
output_file.write("f1-score\tPrecision\tRecall\tAccuracy\tLoss\tf1-scoreCV\tPrecisionCV\tRecallCV\tAccuracyCV\tLossCV\tToken\tNgram\tRaw\tLemma\tStem\tTfidf\tEmbedding\tDimension\tTime\n")
output_file.close()
for vectorizer in ["Tfidf","Embedding"]:# Loop between Tfidf and Embedding vectorizer
	if vectorizer=="Tfidf": # Tfidf Vectorizer
		for approach in combinations_tfidf: # for each combination of approaches Raw+Tokenization, Stem+Tokenization,..., Lemma+Ngram
			f1_score_list,precision_list,recall_list,accuracy_list=[],[],[],[]
			val_acc_list,val_loss_list=[],[]
			featuresList.pop(-1)
			if approach[1]=="Raw": # Use the 'raw' column completecitation 
				featuresList.append(completeCitation)
			elif approach[1]=="Stem": # Use the 'stemmed' column
				featuresList.append("stem_citation")
			else: # Use the lemma column
				featuresList.append("lemma_citation")
				print(vectorizer)
				print("Approach : "+approach[1]+" + "+approach[2])
			X=data[featuresList]#.drop(['Categories_num'],axis=1)
			print(X)
			y=data.Categories_num
			X_to_train,X_val,y_to_train,y_val=train_test_split(X,y,random_state=random_state) # 25% for validation and 75% for cross-validation
			start=time.time()
			for train_index,test_index in skf.split(X_to_train,y_to_train):# cross validation
				backend.clear_session() # Allow to clean tensors previously created in the loop
				X_train,X_test=X_to_train.iloc[train_index,],X_to_train.iloc[test_index,]
				y_train,y_test=y_to_train.iloc[train_index],y_to_train.iloc[test_index,]
				vect_X_train=[approach[0].fit_transform(X_train[featuresList[-1]].fillna('').values.reshape(-1)).todense()]# transform and fit the  on completecitation from training to a list of token
				vect_X_test=[approach[0].transform(X_test[featuresList[-1]].fillna('').values.reshape(-1)).todense()]# transform complete citation of test to a list of token thanks to the previous tokenizer
				vect_X_train.extend((# adding several features to the training dataframe
					X_train[[Section_num_str]].values,
					X_train[[SubType_num_str]].values,
					X_train[[Figure_num_str]].values))
				vect_X_test.extend((# adding several features to the testing dataframe
					X_test[[Section_num_str]].values,
					X_test[[SubType_num_str]].values,
					X_test[[Figure_num_str]].values))
				X,y=None,None
				X_train_dtm=np.concatenate(vect_X_train,axis=1) # final dataframe for training fold of cross validation
				X_test_dtm=np.concatenate(vect_X_test,axis=1)# final dataframe for testing fold of cross validation
				X_train_dtm=np.expand_dims(X_train_dtm,axis=2)# add 1 dimension to fit to the convolutionnal layer
				X_test_dtm=np.expand_dims(X_test_dtm,axis=2)# add 1 dimension to fit to the convolutionnal layer
				###   MODEL   ###
				model=models.Sequential()
				model.add(layers.Conv1D(
					filters=128,
					kernel_size=(4),
					activation='relu',
					input_shape=X_train_dtm[0].shape))
				model.add(layers.GlobalMaxPooling1D())
				model.add(layers.Dropout(
					rate=.4))
				model.add(layers.Dense(
					units=len(target_names),
					activation='softmax'))
				model.compile(
					optimizer="adam",
					loss="sparse_categorical_crossentropy",
					metrics=['accuracy'])
				model.fit(
					X_train_dtm,
					y_train,
					epochs=epochs,
					batch_size=20,
					class_weight=class_weight,
					validation_data=(X_test_dtm,y_test))
				###   SCORES   ###
				val_loss,val_acc=model.evaluate(X_test_dtm,y_test)
				val_loss_list.append(val_loss)
				val_acc_list.append(val_acc)
				result=model.predict(X_test_dtm)
				y_pred_class=[]
				for sample in result:#select the highest probibility to be 0(Creation), 1(Background) or 2(Use) and assign the the corresponding number in a list [0,1,2,1,1,2,2,0,etc.]
					y_pred_class.append(np.argmax(sample))
				print("True : \n\tBackground\t: "+str(y_test.tolist().count(0))+"\n\tCreation\t: "+str(y_test.tolist().count(1))+"\n\tUse\t\t: "+str(y_test.tolist().count(2)))#print the frequency of each categories for the training set
				print("Predict : \n\tBackground\t: "+str(y_pred_class.count(0))+"\n\tCreation\t: "+str(y_pred_class.count(1))+"\n\tUse\t\t: "+str(y_pred_class.count(2)))#print the frequency of each categories for the testing set
				f1_score=metrics.f1_score(y_test,y_pred_class,average=average)*100
				f1_score_list.append(f1_score)
				precision=metrics.precision_score(y_test,y_pred_class,average=average)*100
				precision_list.append(precision)
				recall=metrics.recall_score(y_test,y_pred_class,average=average)*100
				recall_list.append(recall)
				accuracy=metrics.accuracy_score(y_test,y_pred_class)*100
				accuracy_list.append(accuracy)
			# Preparing validation set
			vect_X_val=[approach[0].transform(X_val[featuresList[-1]].fillna('').values.reshape(-1)).todense()]
			vect_X_val.extend((
				X_val[[Section_num_str]].values,
				X_val[[SubType_num_str]].values,
				X_val[[Figure_num_str]].values))
			X_val_dtm=np.concatenate(vect_X_val,axis=1)
			X_val_dtm=np.expand_dims(X_val_dtm,axis=2)
			end=time.time()
			featuresList.pop(-1)
			featuresList.append(completeCitation)
			calc_score("Tfidf",approach," ")
	else:
		for dimension in [50,100,200,300]: # loop of embedding dimension proposed by GloVe
			embedding_file='glove.6B.'+str(dimension)+'d.txt' # file from GloVe (https://nlp.stanford.edu/projects/glove/ - Wikipedia 2014 + Gigaword 5)
			for approach in approaches:
				print(vectorizer)
				print("Approach : "+approach.name+"Token")
				featuresList.pop(-1)
				if "Complete" in approach.name: # Use the 'raw' column completecitation 
					featuresList.append(completeCitation)
				elif "stem" in approach.name: # Use the 'stemmed' column
					featuresList.append("stem_citation")
				else: # Use the lemma column
					featuresList.append("lemma_citation")
				f1_score_list,precision_list,recall_list,accuracy_list=[],[],[],[]
				val_acc_list,val_loss_list=[],[]
				tokenizer=Tokenizer(num_words=vocab_size)
				tokenizer.fit_on_texts(approach)
				tmp=tokenizer.texts_to_sequences(approach)
				word_index=tokenizer.word_index
				tmp=pd.DataFrame(pad_sequences(
					sequences=tmp,
					maxlen=len(max(tmp, key=len)), 
					padding='post'))
				data=pd.concat(
					objs=[data[featuresList],tmp],
					axis=1)
				tmp=None
				X=data[featuresList]
				y=data.Categories_num
				X_to_train,X_val,y_to_train,y_val=train_test_split(X,y,random_state=random_state)
				X_val=[X_val.iloc[:, 3:],X_val.iloc[:, :3]]#seq_features,other_features
				start=time.time()
				for train_index,test_index in skf.split(X_to_train,y_to_train):#cross validation
					backend.clear_session()
					X_train, X_test=[X_to_train.iloc[train_index,], X_to_train.iloc[test_index,]] 
					y_train, y_test=[y_to_train.iloc[train_index,], y_to_train.iloc[test_index,]]
					X_train=[X_train.iloc[:, 3:],X_train.iloc[:, :3]] #seq_features,other_features
					X_test=[X_test.iloc[:, 3:], X_test.iloc[:, :3]] #seq_features,other_features
					###  Load Pre-trained embedding   ###
					embeddings_index={}
					f=codecs.open(
						filename=embedding_file,
						mode='r',
						encoding='utf-8')
					for line in f:
						values=line.split()
						word=values[0]
						coefs=np.asarray(
							a=values[1:],
							dtype='float32')
						embeddings_index[word]=coefs
					f.close()
					###   Creation of embedding matrix   ###
					not_in_embedding=0
					embedding_matrix=np.random.uniform(-0.5,0.5,(len(word_index),dimension))
					for word,i in word_index.items():
						embedding_vector=embeddings_index.get(word)
						if embedding_vector is not None:
							embedding_matrix[i]=embedding_vector
						else:
							not_in_embedding+=1
					print(not_in_embedding,"/",len(word_index))
					###   MODEL   ###
					input_layer=layers.Input(
						shape=(X_train[0].shape[1],))
					embedding=layers.Embedding(
						input_dim=len(word_index),
						output_dim=dimension,
						weights=[embedding_matrix],
						input_length=X_train[0].shape[1],
						trainable=False)(input_layer)
					conv=layers.Conv1D(
						filters=128,
						kernel_size=(4),
						activation='relu')(embedding)
					seq_features=layers.GlobalMaxPooling1D()(conv)
					other_features=layers.Input(
						shape=(3,))
					model=layers.np.concatenate(
						axis=1)([seq_features,other_features])
					model=layers.Dropout(
						rate=.4)(model)
					model=layers.Dense(
						units=len(target_names),
						activation='softmax')(model)
					model=models.Model([input_layer,other_features],model)
					model.compile(
						optimizer="adam",
						loss="sparse_categorical_crossentropy",
						metrics=['accuracy'])
					model.fit(
						X_train,
						y_train,
						epochs=epochs,
						batch_size=20,
						class_weight=class_weight,
						validation_data=(X_test,y_test))
					###   SCORES   ###
					val_loss,val_acc=model.evaluate(X_test,y_test)
					val_loss_list.append(val_loss)
					val_acc_list.append(val_acc)
					result=model.predict(X_test)
					y_pred_class=[]
					for sample in result:
						y_pred_class.append(np.argmax(sample))
					f1_score=metrics.f1_score(y_test,y_pred_class,average=average)*100
					f1_score_list.append(f1_score)
					precision=metrics.precision_score(y_test,y_pred_class,average=average)*100
					precision_list.append(precision)
					recall=metrics.recall_score(y_test,y_pred_class,average=average)*100
					recall_list.append(recall)
					accuracy=metrics.accuracy_score(y_test,y_pred_class)*100
					accuracy_list.append(accuracy)
				end=time.time()
				featuresList.pop(-1)
				featuresList.append(completeCitation)
				calc_score("Embedding",approach,dimension)
output_file.close()