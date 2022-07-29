import pandas as pd, json, re, itertools, varname, dateparser
path = '/Users/virnaliz/Desktop/Garezana/gideon_data/vbd_data_vector.json'
data = pd.read_json(path, orient='index')
df2 = data[["disease", "reservoir_text", "vector_text","incubation", "clinical_hints", "agents", "reservoirs", "vehicles", "vectors"]]

def get_range_data(data_column):
    pattern = "[0-9]+[a-z]+"                                     
    values=[]
    for match in itertools.islice(re.finditer(pattern, data_column), 2):
        values.append(time_in_days(match.group()))
    return pd.Series(values)

def time_in_days(incubation):
    sep = incubation[-1]
    inc_num = int(incubation[:-1])
    if sep == "y":
        x = (inc_num * 365)
    elif sep == "m":
        x = (inc_num * 30)
    elif sep =="w":
        x = (inc_num * 7)
    elif sep =="d":
        x = (inc_num * 1)
    else:  
        x = "Format not recognized"
    return x

def get_range_data1(data_column):
    values=[]
    pattern = "(?<=\<i>)(.*?)(?=\</i>)"
    match_number=re.finditer(pattern, data_column)
    for match in match_number:
        values.append(match.group())
    return values

def data_from_list_of_dics(df, feature_name):
    feature_col = df[f"{feature_name}"]
    if feature_name[-1]== "s":
        s_less_string = feature_name[:-1]
        df[f"{s_less_string}_list"]= feature_col.apply(lambda row: [dic[f"{s_less_string}"] for dic in row])

#Making columns
df2[["min_incubation", "max_incubation"]]= df2["incubation"].apply(lambda x: get_range_data(x))
df2["vector_gen"]= df2["vector_text"].apply(lambda x: get_range_data1(x))
for col in df2:
    if type(df2[col][12460]) == list and type(df2[col][12460][0]) == dict:
        data_from_list_of_dics(df2,col)
df3 = df2[['disease', 'reservoir_text', 'clinical_hints', 'min_incubation', 'max_incubation', 'vector_gen', 'agent_list', 'reservoir_list', 'vehicle_list', 'vector_list']]
df3.to_csv("/Users/virnaliz/Desktop/Garezana/gideon_data/vbd_parsed.csv")
