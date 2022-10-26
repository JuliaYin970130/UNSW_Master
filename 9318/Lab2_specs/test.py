## import modules here
import pandas as pd
import numpy as np

def read_data(filename):
    df = pd.read_csv(filename, sep='\t')
    return (df)

################# Question 1 #################

# helper functions
def project_data(df, d):
    # Return only the d-th column of INPUT
    return df.iloc[:, d]

def select_data(df, d, val):
    # SELECT * FROM INPUT WHERE input.d = val
    col_name = df.columns[d]
    return df[df[col_name] == val]

def remove_first_dim(df):
    # Remove the first dim of the input
    return df.iloc[:, 1:]

def slice_data_dim0(df, v):
    # syntactic sugar to get R_{ALL} in a less verbose way
    df_temp = select_data(df, 0, v)
    return remove_first_dim(df_temp)

def deepcopy(L):
    # copy the elements of L to a
    a = []
    for x in L:
        a.append(x)
    return a

def single_tuple(input_data):
    # binary code: 0000, 0001, 0010, .... , 1111 (dim = 4)
    # or 000, 001, 010, ... , 111 (dim = 3)
    # in which the '1' represents 'ALL'

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
        temp = deepcopy(vals)
        for j in range(len(code)):
            if code[j] == '1':
                temp[j] = 'ALL'
        result.append(temp)
    result = pd.DataFrame(result, columns=list(input_data))
    return result

def buc_rec(df, result, output):
    # Note that input is a DataFrame
    dims = df.shape[1]
    if dims == 1:
        # only the measure dim
        input_sum = sum(project_data(df, 0))
        result.append(input_sum)
        output.loc[len(output)] = result
    else:
        # the general case
        dim0_vals = set(project_data(df, 0).values)
        temp_result = deepcopy(result)
        for dim0_v in dim0_vals:
            result = deepcopy(temp_result)
            sub_data = slice_data_dim0(df, dim0_v)
            result.append(dim0_v)
            buc_rec(sub_data, result, output)
        ## for R_{ALL}
        sub_data = remove_first_dim(df)
        result = deepcopy(temp_result)
        result.append("ALL")
        buc_rec(sub_data, result, output)

def buc_rec_optimized(df):# do not change the heading of the function
    if df.shape[0] == 1:
        output = single_tuple(df)
    else:
        dims = list(df)
        output = pd.DataFrame(columns=dims)
        buc_rec(df, [], output)
    print(output)
    return output

input_data = read_data('./asset/a_.txt')
output = buc_rec_optimized(input_data)