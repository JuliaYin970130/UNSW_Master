## import modules here 
import pandas as pd
import numpy as np
import helper

def read_data(filename):
    df = pd.read_csv(filename, sep='\t')
    return (df)

# helper functions
def project_data(df, d):
    # Return only the d-th column of INPUT
    return df.iloc[:, d]

def select_data(df, d, val):
    # SELECT * FROM INPUT WHERE input.d = val
    col_name = df.columns[d]
    #print(df[df[col_name] == val])
    return df[df[col_name] == val]

def remove_first_dim(df):
    # Remove the first dim of the input
    return df.iloc[:, 1:]

def slice_data_dim0(df, v):
    # syntactic sugar to get R_{ALL} in a less verbose way
    df_temp = select_data(df, 0, v)
    return remove_first_dim(df_temp)


################### Question 1 ###################

def buc_rec_optimized(df):# do not change the heading of the function
    df_temp = df.copy()
    #print(df_temp)
    for i in df_temp.columns[:-1].tolist():  # change v_1  v_2 ...  v_d to str
        df_temp[i] = df_temp[i].apply(str)

    df_output = pd.DataFrame(columns=df_temp.columns.to_list())
    #print(df_output)
    #df_temp = df_temp.loc[:,df_temp.columns[:-1]]

    dims = df_temp.columns.shape[0]
    pred_list = []
    #print(df_temp.index)
    #df_output.sort_index(inplace=True)
    if df_temp.index.shape[0] > 1:
        buc(df_temp, dims, pred_list, df_output)
        df_output.sort_values(by=df.columns[:-1].tolist(), inplace=True)
        print(df_output)
    else:
        df_output = single_tuple(df_temp)
        print(df_output)

    return df_output
    #pass # **replace** this line with your code

def buc(data,dimes,pred_list, output):

    # 只剩M的时候
    if dimes == 1:
        # 算总和
        sum = (project_data(data,0).apply(int)).sum()
        #result = pred_list.copy()
        pred_list.append(sum)
        #print(result)
        #print()
        #print(pred_list)
        output.loc[len(output)] = pred_list
        #print('output:')
        #print(output)
        #print()
        return output

    # The single-tuple optimization
    elif data.index.shape[0] == 1:
        single_1(data, pred_list, output)

    else:
        # 去重的dime
        #print(data)
        dimes_list = list(set(project_data(data, 0).to_list()))
        #print(dimes_list)
        #print()
        for dime in dimes_list:
            # 按当前dime切割一下
            slice_data = slice_data_dim0(data, dime)
            #pred_list.append(dime)
            #print(pred_list) -> 会重复叠加
            result = pred_list.copy()
            result.append(dime)
            dimes = slice_data.columns.shape[0]
            buc(slice_data, dimes, result, output)
        # 删第一个dime
        data_ = remove_first_dim(data)
        result = pred_list.copy()
        result.append('ALL')
        #print('removed')
        buc(data_, data_.columns.shape[0], result, output)

def single_(df,df_out):
    value = df.head(1).values.tolist()

    print(value)




def single_1(df,pre_dims,df_out):

    cols = df.shape[1] - 1
    _count = 2 ** (cols)
    #value = df.head(1).values.tolist()
    #print(value)
    for num in range(0, 2 ** (cols)):
        #print(pre_dims)
        concat = [i for i in pre_dims]
        binary = bin(num)[2:]
        #print(binary)
        temp = df.head(1).values.tolist()
        temp = temp[0]
        for i in range(0, len(binary)):
            if binary[i] == '1':
                temp[len(temp) - len(binary) + i - 1] = "ALL"

        #concat.append(i for i in temp[0])
        #print(concat)
        #print()
        concat.extend(temp)
        #print(concat)
        df_out.loc[len(df_out)] = concat


def single_tuple(input_data):
    num_of_dims = input_data.shape[1] - 1
    rows = 2 ** num_of_dims
    vals = list(input_data.loc[0])
    L = []
    for i in range(rows):
        temp = bin(i)
        result = temp[2:]
        L.append(result)
    final = []
    for i in L:
        if len(i) < num_of_dims:
            temp = '0' * (num_of_dims-len(i)) + i
            i = temp
        final.append(i)
    result = []
    for code in final:
        temp = vals.copy()
        for j in range(len(code)):
            if code[j] == '1':
                temp[j] = 'ALL'
        result.append(temp)
    result = pd.DataFrame(result, columns=list(input_data))
    return result
    #output.loc[len(output)] = result


input_data = read_data('./asset/a_.txt')
output = buc_rec_optimized(input_data)
