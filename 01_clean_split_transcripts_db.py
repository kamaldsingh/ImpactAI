# Databricks notebook source
# MAGIC %run "/Users/mailkamaldeep@gmail.com/helpers"

# COMMAND ----------

import pyspark.pandas as ps
import re

# COMMAND ----------

# MAGIC %matplotlib inline
# MAGIC pd.options.display.max_columns = 999

# COMMAND ----------

sparkdf = spark.read.table('raw_transcripts_csv')
psdf = ps.DataFrame(sparkdf)

# COMMAND ----------

def count_splits_transcripts(tr):
    qna = [x for x in sent_tokenize(tr) if 'questions and answers' in str.lower(x) or 'questions & answers' in str.lower(x)] 
    
    if(len(qna)>0):
        return 1
    else:
        qnaa = [x for x in sent_tokenize(tr) if 'analyst' in str.lower(x) or 'portfolio manager' in str.lower(x)] 
        if(len(qnaa)>0):
            return 2
        else:
            return 0
        
def split_transcript(row):
    splits = re.split(r'questions and answers|questions & answers', str.lower(row.transcript))
    if(len(splits)>0):
        row['prep_remarks'] = splits[0]
        row['QnA'] = ' '.join(splits[1:None])
    else:
        splits = re.split(r'analyst|portfolio manager', str.lower(row.transcript))
        if(len(splits)>0):
            row['prep_remarks'] = splits[0]
            row['QnA'] = ' '.join(splits[1:None])
        else:
            print('exception')
            row['prep_remarks'] = str.lower(row.transcript)
            row['QnA'] = str.lower(row.transcript)
    return(row)

# COMMAND ----------

tp_splits = psdf.apply(lambda x:split_transcript(x), axis=1)
tp_splits = tp_splits.drop(columns='transcript')

# COMMAND ----------

tp_splits.to_table('tp_splits')

# COMMAND ----------

tp_splits[tp_splits.QnA.isna()].shape

# COMMAND ----------


