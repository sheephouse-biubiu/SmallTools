import sys,os
import xlrd
import os, sys
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)
from conf import config

class sqlCreate:
    def __init__(self, config_file_path):
        self.cfg = config.Config(config_file_path)

    def run(self):
        print("run sql createt")
        #get base config, name "basic_conf"
        basic_conf = {}
        for key, value in self.cfg.getSectItems("basic_conf"):
            basic_conf[key] = value
        csvname = ""
        if "filename" in basic_conf:
            csvname = basic_conf["filename"]
        if csvname == "":
            print("csv file name must not null")
            return     
        data = xlrd.open_workbook(csvname)
        sheet = 0
        if "sheets" in basic_conf:
            sheet = int(basic_conf["sheets"])
        col  = 0
        if "col" in basic_conf:
            col = int(basic_conf["col"])

        #open file 
        tableInfoItems = []
        for Sec in self.cfg.getSections():
            if Sec == "basic_conf":
                continue
            else:
                cfg = {}
                for key, value in self.cfg.getSectItems(Sec):
                    cfg[key] = value
                cfg["fileHandle"] = open(cfg["savename"],"w")
                tableInfoItems.append(cfg)

        table = data.sheets()[sheet]
        index = 0
        keyname = ""
        for key in table.col_values(0):
            if 0 == index:
                keyname = key
            else:
                #create sql 
                for item in tableInfoItems:
                    sql = item["basicsql"].replace("{--table--}", item["tablename"]).replace("{--keyname--}", keyname).replace("{--key--}", key)
                    item["fileHandle"].write(sql)
                    item["fileHandle"].write('\n')
            index += 1
        for item in tableInfoItems:
            item["fileHandle"].close()        

if __name__ == "__main__":
    print("start sql create ...")
    config_file_path="./conf.ini"
    if len(sys.argv) == 2:
        config_file_path = sys.argv[1]
    sql = sqlCreate(config_file_path)
    sql.run()