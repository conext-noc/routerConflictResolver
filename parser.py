import pandas as pd
import re
import os

def fileToDict(fileName, fileType):
  file = pd.read_excel(fileName) if fileType == "E" else pd.read_csv(
    fileName, encoding='latin1')
  data = file.to_dict("records")
  return data

def dataToDict(header, data):
  value = re.sub(" +", " ", data).replace(" ", ",")
  res = header + value
  print(res[:-1], file=open("data.csv", "w",encoding="utf-8"))
  result = fileToDict("data.csv","C")
  os.remove("data.csv")
  return result
