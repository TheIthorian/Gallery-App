import xml.etree.cElementTree as ET
import traceback
import datetime
import os, time
import pymysql
from config import mysql

"""
Todo:
 - Return description of cached values instead of enum
 - Add method to raiseError > UserErrorInsert
"""

class Server ():

    def __init__(self, root, serverConfigFile):
        
        root = ET.parse(serverConfigFile).getroot()
        for child in root:
            if (child.tag == 'Server'):
                self.servername = child.attrib['servername']
                self.username = child.attrib['username']
                self.password = child.attrib['password']
                self.dbname = child.attrib['dbname']
                self.directoryRoot = child.attrib['directoryroot']

            if (child.tag == 'AppInfo'):
                self.siteversion = child.attrib['siteversion']


    def runQuery(self, file, queryName, inputs):
        conn = mysql.connect()
        query = GetQuery(file, queryName)

        # Query debugging
        if False:
            print("\nQuery: ", queryName, query)
            for i in inputs:
                value = inputs[i]
                print("Key: ", i, "\tValue: ", value, type(value))

        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(query, inputs)
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result


    def runInsertQuery(self, file, queryName, inputs):
        conn = mysql.connect()
        query = GetQuery(file, queryName)
        cursor = conn.cursor(pymysql.cursors.DictCursor)

        if False:
            print("\nQuery: ", queryName, query)
            for i in inputs:
                value = inputs[i]
                print("Key: ", i, "\tValue: ", value, type(value))

        cursor.execute(query, inputs)
        result = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        
        return result
       

    def dataAuthorisation(self, authName, parentId, childId):

        inputs = {'ParentId':parentId, 'ChildId':childId}
        try:
            result = self.runQuery("UserAuthorisation", authName, inputs)
        except Exception as e:
            print("\nData auth error: ", e)
            print('Parameters: {Auth: ', authName, ', ParentId: ', parentId, ', ChildId: ', childId, '}\n')
            return False

        #print(result)
        if len(result) > 0: return True 
        else: return False
 

def GetQuery (file, queryName):

    root = ET.parse('./data/' + file + '.xml').getroot()
    for child in root:
        if child.attrib['Name'] == queryName:
            return child.find('SQL').text
    raise Exception("Unable to locate query: " + file + ">" + queryName)
    


global serverConnection
serverConnection = Server('./', './config/ServerConfig.xml') 


