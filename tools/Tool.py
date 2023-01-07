# encoding: utf-8
# @Time: 2023/1/7 9:05 
# @Author: 侯真杰

from config import configObject
from common.writerExcel import toxls



class Tool:
    @staticmethod
    def create_writer_excel(table_id, row, enviroment='PRE'):
        """设置环境"""
        configObject.set_enviroment(enviroment)

        toxls(table_id, row)




if __name__ == '__main__':
    Tool.create_writer_excel("2100000032625980", 10)


