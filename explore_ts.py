# -*- coding: utf-8 -*-
import warnings
warnings.filterwarnings("ignore")
import sys
sys.setrecursionlimit(1000000)
import os
from os import listdir,makedirs
from os.path import join,dirname
import json

import pandas as pd
import numpy as np
from matplotlib.pyplot import cm
import matplotlib.pyplot as plt
from visualize.plot_ts import plot_hist
from settings import Config_json,get_user_data_dir
from utils import savePNG,millisec_to_str
import os


N_color = 10

DAY_SECONDS = 1440 * 60

FIGURE_SIZE = (16, 7)



def run():
    root_dir = get_user_data_dir()

    original_path = join(root_dir, "706_dnm_tmp_3ZFwT#sum_iUserNum_300#20190620_16Days_valid6D_pipeline_test_input_node_train_data.csv")
    df = pd.read_csv(original_path)
    # print(df.head())
    df["timestamp"] = df["timestamp"].map(millisec_to_str)
    #
    pic_path = join("/Users/xumiaochun/jiawei", "tmp/pic_valid/")

    line_id_list = np.unique(df.line_id)

    for l_id in line_id_list:
        l_id_list = l_id.split("valid")
        VALID_DAY = l_id_list[-1].replace("D", "")
        print VALID_DAY
        if int(VALID_DAY) <10:
            continue
        df_slice = df[df.line_id == l_id].copy()
        print(df_slice.shape)
        plt = plot_hist(df_slice, detect_days = 2, plot_day_index=[1,7], anom_col = "label" , value_col = "point", freq = 300)
        savePNG(plt, targetDir=join(pic_path, "%s.png" % l_id))

def extract_selected_id_name():
    root_dir = get_user_data_dir()
    original_path = join(root_dir, "706_dnm_tmp_3ZFwT#sum_iUserNum_300#20190620_16Days_valid6D_pipeline_test_input_node_train_data.csv")
    df = pd.read_csv(original_path)
    # print(df.head(2))
    # print df.columns.tolist()
    df["timestamp"] = df["timestamp"].map(millisec_to_str)
    #
    pic_path = join("/Users/xumiaochun/jiawei", "tmp/pic_valid_select/")

    file_dir = pic_path
    i = 1
    a = os.walk(file_dir)
    b = None
    for root, dirs, files in os.walk(file_dir):
        print(i)
        i += 1
        # print(root) #当前目录路径
    #     print(dirs) #当前路径下所有子目录
    #     print(files) #当前路径下所有非目录子文件
    # print(b)
    selected_data_name = []
    for l_id in files:
        # l_id_list = l_id.split("valid")
        VALID_DAY = files[-1].replace(".png", "")
        selected_data_name.append(VALID_DAY)
    selected_data_name = pd.DataFrame(selected_data_name)
    selected_data_name.to_csv("tmp/selected_name_list.csv",index = False)
    return  selected_data_name

def select_data():
    selected_id = pd.read_csv('/Users/xumiaochun/jiawei/tmp/selected_name_list2.csv')
    selected_id.columns = {'selected_id'}
    root_dir = get_user_data_dir()
    original_path = join(root_dir, "706_dnm_tmp_3ZFwT#sum_iUserNum_300#20190620_16Days_valid6D_pipeline_test_input_node_train_data.csv")
    origin_dataset = pd.read_csv(original_path)    # selected_id = pd.read_csv('/Users/xumiaochun/jiawei/tmp/selected_name_list2.csv')
    a0 = origin_dataset[origin_dataset['line_id'] == selected_id.selected_id[0]]
    t = a0
    for j in range(1,len(selected_id)):
        id_name = selected_id.selected_id[j]
        a1 = origin_dataset[origin_dataset['line_id'] == id_name]
        t = pd.concat([t,a1],axis=0)
    t.to_csv("/Users/xumiaochun/jiawei/tmp/selected_data.csv",index = False)

if __name__ == "__main__":
    select_data()