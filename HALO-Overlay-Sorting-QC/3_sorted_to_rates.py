import os
import re
import pandas as pd

pos_path = ".../2_sort_pos/"
neg_path = ".../2_sort_neg/"
save_csv_to_path = ".../QC_folder/"
csv_name = "output"

def extract_UWA(text):
    pattern = r'UWA_\d{1,4}LAYER_\d{1}'
    matches = re.findall(pattern, text)
    return matches[0]


positive_names = []
negative_names = []

false_positive_names = []
false_negative_names = []

pos_file_names = os.listdir(pos_path)
neg_file_names = os.listdir(neg_path)

all_file_names = []

for file_name in pos_file_names:
    file_name = "human_pos_" + file_name
    all_file_names.append(file_name)
for file_name in neg_file_names:
    file_name = "human_neg_" + file_name
    all_file_names.append(file_name)

unique_UWAs = []
score_keeper = {}
for file_name in all_file_names:
    file_name=file_name.upper()
    UWA = extract_UWA(file_name)

    #make a list of unique UWAs
    if UWA not in unique_UWAs:
        unique_UWAs.append(UWA)
for UWA in unique_UWAs:
    score_keeper[UWA + "_false_pos"] = []
    score_keeper[UWA + "_true_pos"] = []
    score_keeper[UWA + "_false_neg"] = []
    score_keeper[UWA + "_true_neg"] = []

for file_name in all_file_names:
    file_name = file_name.upper()
    UWA = extract_UWA(file_name)
    if "HUMAN_POS" in file_name:
        if "MARKED_POS" in file_name:
            score_keeper[UWA + "_true_pos"].append(file_name)
        if "MARKED_NEG" in file_name:
            score_keeper[UWA + "_false_neg"].append(file_name)
    if "HUMAN_NEG" in file_name:
        if "MARKED_NEG" in file_name:
            score_keeper[UWA + "_true_neg"].append(file_name)
        if "MARKED_POS" in file_name:
            score_keeper[UWA + "_false_pos"].append(file_name)
# create dictionary to store data to later be turned into a dataframe
pre_dataframe = {"UWA_layer": [],
                 "false_positive_images": [],
                 "true_positive_images": [],
                 "false_negative_images": [],
                 "true_negative_images": [],
                 "false_positive_rate": [],
                 "false_negative_rate": [],
                 }

for UWA in unique_UWAs:
    false_pos_list = score_keeper[UWA+"_false_pos"]
    true_pos_list = score_keeper[UWA + "_true_pos"]
    false_neg_list = score_keeper[UWA + "_false_neg"]
    true_neg_list = score_keeper[UWA + "_true_neg"]

    pre_dataframe["UWA_layer"].append(UWA)
    pre_dataframe["false_positive_images"].append(false_pos_list)
    pre_dataframe["true_positive_images"].append(true_pos_list)
    pre_dataframe["false_negative_images"].append(false_neg_list)
    pre_dataframe["true_negative_images"].append(true_neg_list)



    if len(false_pos_list)>0:
        false_pos_rate = 100*len(false_pos_list)/(len(false_pos_list)+len(true_pos_list))
        print(f"{UWA} false +: {round(false_pos_rate, 1)}%")
        pre_dataframe["false_positive_rate"].append(round(false_pos_rate,1))
    if len(false_pos_list)==0:
        print(f"{UWA} false +: 0%")
        pre_dataframe["false_positive_rate"].append(0)
    if len(false_neg_list)>0:
        false_neg_rate = 100*len(false_neg_list)/(len(false_neg_list)+len(true_neg_list))
        print(f"{UWA} false -: {round(false_neg_rate, 1)}%")
        pre_dataframe["false_negative_rate"].append(round(false_neg_rate, 1))
    if len(false_neg_list) == 0:
        print(f"{UWA} false -: 0%")
        pre_dataframe["false_negative_rate"].append(0)

df = pd.DataFrame(pre_dataframe, index=None)
df.to_csv(save_csv_to_path+csv_name+".csv", index=False)