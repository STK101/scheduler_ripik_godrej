import pandas as pd
import numpy as np
def calc(row):
  rd = row['Red Days']
  rtb = row['Red to Black']
  if (rd == 0):
    return 0 ## to be discussed 
  else :
    return (float(rtb))/rd

def update_transition_probabilities(source_file):
  counts_df = pd.read_csv('hist_data.csv', index_col=0)
  xls = pd.ExcelFile(source_file)
  df1 = pd.read_excel(xls, xls.sheet_names[0] )
  out_name = (df1.loc[1, "Unnamed: 1"])
  df1 = df1.iloc[8:]
  df1.columns = df1.iloc[0]
  df1 = df1.iloc[1:]
  df1.reset_index(inplace= True, drop = True)
  df1_reg_norm =  df1[df1['Norm Category'] != "Ecom"] #316
  df1_reg_norm.drop([df1_reg_norm.columns[0]], axis = 1,inplace = True)
  df1_reg_norm.reset_index(inplace= True, drop = True)
  df1_reg_norm.set_index("Item Code", inplace = True)
  sum = 0
  for x in (df1_reg_norm.index):
    if x not in counts_df.index:
      sum +=1
      c_row = df1_reg_norm.loc[x, df1_reg_norm.columns]
      cs = c_row["Colour Status"][0]
      cs1 = c_row["Colour Status"][1]
      pcs = "_"
      pcs1 = "_"
      if (cs == 'Red'):
          rd = 1
      else:
        rd = 0
      rtb = 0
      counts_df.loc[x] = [cs,cs1,pcs,pcs1,rd,rtb]
    else:
      c_row = df1_reg_norm.loc[x, df1_reg_norm.columns]
      count_row = (counts_df.loc[x, counts_df.columns])
      '''
      (counts_df.loc[x])["Prev Colour Status"] = count_row["Colour Status"]
      (counts_df.loc[x])["Prev Colour Status.1"] = count_row["Colour Status.1"]
      (counts_df.loc[x])["Colour Status"] = c_row["Colour Status"][0]
      (counts_df.loc[x])["Colour Status.1"] = c_row["Colour Status"][1]
      '''
      (count_row)["Prev Colour Status"] = count_row["Colour Status"]
      (count_row)["Prev Colour Status.1"] = count_row["Colour Status.1"]
      (count_row)["Colour Status"] = c_row["Colour Status"][0]
      (count_row)["Colour Status.1"] = c_row["Colour Status"][1]
      '''
      if (c_row["Colour Status"][1] == 'Red'):
        (counts_df.loc[x]['Red Days']) += 1
      if (c_row["Colour Status"][1] == 'Black' and (counts_df.loc[x])["Prev Colour Status.1"] == 'Red'):
        (counts_df.loc[x]['Red to Black']) += 1
      '''
      if (c_row["Colour Status"][1] == 'Red'):
        ((count_row)['Red Days']) += 1
      if (c_row["Colour Status"][1] == 'Black' and (count_row)["Prev Colour Status.1"] == 'Red'):
        ((count_row)['Red to Black']) += 1
      counts_df.loc[x, counts_df.columns] = count_row
      if ((count_row != counts_df.loc[x, counts_df.columns]).all()):
        print("fuck")
  transition_probabilities = counts_df.apply(lambda row: calc(row), axis=1)
  transition_probabilities.to_csv('transition_prob.csv')
  print(sum)
  return counts_df;
