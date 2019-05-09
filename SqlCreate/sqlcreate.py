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
        fileType = csvname.split(".")[1]
        fileType=basic_conf["type"]
        data = ""
        if fileType == "csv":
            data = open(csvname)
        else:  
            data = xlrd.open_workbook(csvname)
        sheet = 0
        if "sheets" in basic_conf:
            sheet = int(basic_conf["sheets"])
        col  = 0
        if "col" in basic_conf:
            col = int(basic_conf["col"])

        #open file 
        self.tableInfoItems = []
        for Sec in self.cfg.getSections():
            if Sec == "basic_conf":
                continue
            else:
                cfg = {}
                for key, value in self.cfg.getSectItems(Sec):
                    cfg[key] = value
                if "savename" not in cfg:
					print("savename file name must not null..")
					continue
                if os.path.exists(cfg["savename"]):
                    os.remove(cfg["savename"])
                cfg["fileHandle"] = open(cfg["savename"],"w")
                self.tableInfoItems.append(cfg)
        table=""
        if fileType != "csv":
            table = data.sheets()[sheet]
        index = 0
        self.keyname = ""
        if fileType != "csv":
            for key in table.col_values(col):
                index = self.writeTofile(index, value)
        else:
            for key in data.readlines():
                value = key.split(",")[col-1]
                value = value.replace('\r\n','')
                value = value.replace('\n','')
                index = self.writeTofile(index, value)
                
        for item in self.tableInfoItems:
            if "fileHandle" in item:
                item["fileHandle"].close()

    def writeTofile(self, index, key):
        if 0 == index:
            self.keyname = key
        else:
            #create sql 
            for item in self.tableInfoItems:
                sql = "err basicsql, please check conf.ini"
                if "basicsql" in item:
                    sql = item["basicsql"].replace("{--keyname--}", self.keyname).replace("{--key--}", key)
                elif index > 1:
                    continue
                if "fileHandle" in item:
                    item["fileHandle"].write(sql)
                    item["fileHandle"].write('\n')
        index += 1
        return index

if __name__ == "__main__":
    print("start sql create ...")
    config_file_path="./conf.ini"
    if len(sys.argv) == 2:
        config_file_path = sys.argv[1]
    sql = sqlCreate(config_file_path)
    sql.run()