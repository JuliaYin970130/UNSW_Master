## import modules here 
import pandas as pd
import numpy as np
import helper



def read_data(filename):
    df = pd.read_csv(filename, sep='\t')
    return (df)


################### Question 1 ###################

def buc_rec_optimized(df):# do not change the heading of the function
    df_temp = df.copy()
    #print(df_temp)
    df_output = pd.DataFrame(columns=df_temp.columns.to_list())

#    if df_temp.index.shape[0] > 1:
    dims = df_temp.columns.shape[0]
    pred_list = []
    count = 0
    buc(df_temp, dims, pred_list, df_output,count)
    print(count)

    #print(df_output)

    return df_output
    #pass # **replace** this line with your code

def buc(data,dimes,pred_list, output,count):

    if dimes == 1:
        # sum
        sum = (helper.project_data(data,0).apply(int)).sum()
        pred_list.append(sum)
        output.loc[len(output)] = pred_list
        return output

    # The single-tuple optimization
    elif data.index.shape[0] == 1:
        count += 1
        single_(data,pred_list,output)
        return output

    else:
        # 去重的dime
        #print(data)
        dimes_list = list(set(helper.project_data(data, 0).to_list()))
        #print(dimes_list)
        #print()
        for dime in dimes_list:
            # 按当前dime切割一下
            slice_data = helper.slice_data_dim0(data, dime)
            #pred_list.append(dime)
            #print(pred_list) -> 会重复叠加
            result = pred_list.copy()
            result.append(dime)
            dimes = slice_data.columns.shape[0]
            buc(slice_data, dimes, result, output, count)
        # 删第一个dime
        data_ = helper.remove_first_dim(data)
        result = pred_list.copy()
        result.append('ALL')
        #print('removed')
        buc(data_, data_.columns.shape[0], result, output,count)

def single_(df,pred_list,df_out):

    cols = df.columns.shape[0] - 1
    _count = 2 ** (cols)
    #print()
    #print(_count)
    #value = df.head(1).values.tolist()
    #print(value)
    #concat = []
    for num in range(0, 2 ** (cols)):
        concat = pred_list.copy()
        #print(pre_dims)
        #concat = pred_list.copy()
        binary = bin(num)[2:]
        binary = binary[::-1]
        if len(binary) != cols:
            rest = cols - len(binary)
            binary = binary + rest * '0'
        #print(binary)
        #binary = binary[::-1]
        temp = df.head(1).values.tolist()
        temp = temp[0]
        temp = [str(i) for i in temp]
        #print(temp)
        i = 0
        while i < len(binary):
            if binary[i] == '1':
                #index = i
                #print(index)
                #temp[cols - len(binary) + i] = "ALL"
                temp[i] = "ALL"
            i += 1
        concat.extend(temp)
        #print(concat)
        #print()
        df_out.loc[len(df_out)] = concat

        #print(df_out)
        #print()

input_data = read_data('./asset/a_.txt')
output = buc_rec_optimized(input_data)
print(output)