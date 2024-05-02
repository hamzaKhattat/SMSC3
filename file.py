from edit import *
from interface import *
import sys
import os
from PySide2 import *
from PySide2 import *
from qt_material import *
from PySide2 import QtCore, QtGui,QtWidgets
from PySide2.QtCore import *
import psutil
#from psutil import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import PySide2extn
import datetime
import shutil
#import pyside2
platforms={
    "linux":"Linux",
    "linux1":"Linux",
    "darwin":"OS x",
    "win32":"Windows",
    "win64":"Windows"
    }
import logging
fname=""
import sys
from mysql.connector import connect
import pandas as pd
import smpplib.gsm
import smpplib.client
import smpplib.consts
import time
import configparser
from threading import Thread
import mysql
from PySide2.QtWidgets import QProgressBar

#from multiThreading import Thread
use_method=0
class sms_generator:
    ip=""
    port=0
    username=""
    passwd=""
    files=[]
    repeat=False
    amount,amount_per_sec="",""
    
    def __init__(self, ip="", port="", user="", password="H@mza123456789", files=[], repeat=False, amount=0, amount_per_sec=0):
        self.ip=ip
        self.port=port
        self.username=user
        self.passwd=password
        self.files=files
        self.repeat=repeat
        self.amount=amount
        self.amount_per_sec=amount_per_sec
    def checked(self,name):
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        self.connection("""CREATE TABLE IF NOT EXISTS generator(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,ip varchar(255),file VARCHAR(255),SMS int,total varchar(255),repeaat varchar(255)) """)
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM {}".format(name))
        count = cursor.fetchone()[0]
        connection.close()
        print("count:",count)
        return count

    def Generator(self):
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        self.connection("""CREATE TABLE IF NOT EXISTS generator(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,ip varchar(255),file VARCHAR(255),SMS int,total varchar(255),repeaat varchar(255)) """)
        print("Amount:",self.amount,"Total:",self.amount_per_sec)
        cursor = connection.cursor()
        s = '''
        CREATE TABLE IF NOT EXISTS generator_''' + (self.files[0].split("/")[-1]).split(".")[0] + '''(
                       id INT PRIMARY KEY AUTO_INCREMENT,
                       ip   VARCHAR(255),
                       port VARCHAR(255),
                       user VARCHAR(255), 
                       password VARCHAR(255), 
                       file VARCHAR(255), 
                       repeaat VARCHAR(255), 
                       amount VARCHAR(255), 
                       amount_per_sec VARCHAR(255)
        );
        '''
        #print(s)
        cursor.execute(s)
        
        # files  = [x, y, z]
        file = ",".join(self.files) # x,y,z
        #print(file)
        s="INSERT INTO generator(ip,file,SMS,total,repeaat) values('{}','{}',0,'{}','{}')".format(str(self.ip)+":"+str(self.port),file,str(self.amount),self.repeat)
        #print(s)
        cursor.execute(s)
        s="""INSERT INTO generator_"""+(self.files[0].split("/")[-1]).split(".")[0]+"""(ip, port, user, password, file, repeaat, amount,
        amount_per_sec) VALUES ('{}', '{}', '{}', '{}', '{}','{}', '{}', '{}')""".format(self.ip,
        self.port, self.username, self.passwd,file,self.repeat,  self.amount, self.amount_per_sec)
        #print(s)
        cursor.execute(s)
        connection.commit()
        connection.close()


    def get_last_id(self):
        try:
            # Establish a connection to the database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="H@mza123456789",
                database="templates"
            )

            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Execute the SQL query to get the last ID
            cursor.execute("SELECT MAX(id) FROM generator;")

            # Fetch the result
            last_id = cursor.fetchone()[0]

            return last_id

        except mysql.connector.Error as error:
            print("Error while connecting to MySQL:", error)
            return None

        finally:
            # Close the cursor and connection
            if 'cursor' in locals():
                cursor.close()
            if 'connection' in locals():
                connection.close()

    def connection(self,query):
        #print("Executing query "+query+".....")
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()
    def get_all_data(self):
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM generator")  # Fixed typo 'sekect' to 'SELECT'
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        #Fprint(df)
        connection.close()
        return rows 
    def get_data(self,table):
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM {}".format(table))  # Fixed typo 'sekect' to 'SELECT'
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[i[0] for i in cursor.description])
        connection.close()
        return df  # Corrected return statement
    
    def get_file_by_id(self, id):
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        cursor = connection.cursor()
        query = "SELECT file FROM generator WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()  # Fetch the row
        connection.close()  # Close the connection before further Threading
        #print("R:",result)
        if result is not None:
            file = result[0]  # Fetch the 'file' column from the first row
            return file
        else:
            print("No matching row found in the database.")
            return None
    def get_data_by_id(self,id):
        files = self.get_file_by_id(id)
        #print("\nfiles:",files)
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        cursor = connection.cursor()
        query = "SELECT ip, port, user, password, file, repeaat, amount, amount_per_sec FROM generator_{}".format(files.split(",")[0].split("/")[-1].split(".")[0])
        #print("\nQuery:",query,"\n")
        cursor.execute(query)
        data = cursor.fetchall()[0]
        connection.close()
        #print("\nData:",data)
        if data:  # Check if data is not None
            ip, port, user, password, file, repeat, total, a = data
            repeat=bool(repeat)
            return ip, port, user, password, file, repeat, total, a
        else:
                return None  # Return None if no data is found for the provided ID
    def send_sms(self, client, src, dst, msg, monitor, total, last_id,username,password,monitor_sec,sec):
        print("Monitor:{}/Monitor Per Sec:{}/Amount Per Sec:{}/Total:{}".format(monitor,monitor_sec,sec, total))
        if int(monitor) == int(total):
            return monitor,monitor_sec
        elif monitor_sec==sec:
            return monitor,monitor_sec
        else:            
            logging.debug('Connected')
            file = open("Logs.txt", "a")
            file.write("\n\nMessage {} is Sending .................. \n\nClient Object:{},\nsrc:{}\ndst:{},\nmsg:{}"
                       .format(monitor, client, src, dst, msg))
            file.close()
            parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u"{}".format(msg))

            for part in parts:
                pdu = client.send_message(
                    source_addr_ton=smpplib.consts.SMPP_TON_ALNUM,
                    source_addr_npi=smpplib.consts.SMPP_NPI_UNK,
                    source_addr=src,
                    dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
                    dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
                    destination_addr=dst,
                    short_message=part,
                    data_coding=encoding_flag,
                    esm_class=msg_type_flag,
                    registered_delivery=True,
                )
                logging.info('submit_sm {}->{} seqno: {}'.format(pdu.source_addr, pdu.destination_addr, pdu.sequence))
            
            # Update last_id in the database
            self.connection("UPDATE generator SET SMS={} WHERE id={}".format(int(monitor), int(last_id)))

            # Increase monitor by 1 for the next message
            monitor= int(monitor)+1
            monitor_sec=int(monitor_sec)+1
            print("\nSending SMS Number:{}\n".format(str(monitor)))
            return monitor,monitor_sec
#(client, file, monitor, total, last_id, username, password, monitor_sec, sec, repeat)
    def sms_per_files(self, client, files, monitor, total, last_id,username,password,monitor_sec,sec,r): 
        if isinstance(files, str):
            files=[files]
        else :
            files=files
        print("before fi :",files,type(files))  
  
        for fi in files:
            monitor,monitor_sec = self.sms_per_file(client, fi, monitor, total, last_id,username,password,monitor_sec,sec,r)
        return monitor,monitor_sec

    # Assuming other methods are defined here

    def sms_per_file(self, client, file, monitor, total, last_id, username, password, monitor_sec, sec, repeat):
        connection = connect(
            host="localhost",
            user="root",
            password="H@mza123456789",
            database="templates"
        )
        cursor = connection.cursor()
        query = "SELECT * FROM {}".format((file.split("/")[-1]).split(".")[0])
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()

        for row in data:
            # Check if we have reached the total count
            if int(monitor) >= int(total):
                return monitor, monitor_sec

            # Check if we need to sleep to respect the amount per second
            if int(monitor_sec) == int(sec) and not monitor_sec == 1:
                print("condition 2")
                monitor_sec = 0
                time.sleep(1)
                if not repeat:
                    self.sms_per_files(client, file, monitor, total, last_id, username, password, monitor_sec, sec, repeat)# Sleep for a second
                return monitor, monitor_sec

            # Send the SMS
            src, dst, msg = row[1], row[2], row[3]
            monitor, monitor_sec = self.send_sms(
                client,
                src,
                dst,
                msg,
                monitor,
                total,
                last_id,
                username,
                password,
                monitor_sec,
                sec
            )

        return monitor, monitor_sec


    def send_per_amount(self, client, files, amount_per_sec, amount, last_id,username,password):
        monitor = 1
        done = False
        monitor_sec=1
        while not done:
            for i in range(int(amount_per_sec)):
                print("Monitor:{},Amount:{}".format(monitor,amount))
                if int(monitor) == int(amount):
                    done = True
                    print("All sms has been sent!!!!!!!!!")
                    break            
                else:
                    print("")
                    print("args:",client, files, monitor, amount, last_id,username,password,monitor_sec,int(amount_per_sec))
                    monitor,monitor_sec = self.sms_per_files(client, files, monitor, amount, last_id,username,password,monitor_sec,int(amount_per_sec),True)
                    print("the monitor is increased:",monitor)
                    print("Sms {} has been sent".format(monitor))
                    print("send_per_amount() monitor_sec=", monitor_sec)
                    print("send_per_amount() amount_per_sec=",amount_per_sec)
                    if int(monitor_sec)==int(amount_per_sec):
                       monitor_sec=0
                       print("Sleeping for 1 sec..................")
                       time.sleep(1)
            if done:
                break
            else:
                monitor_sec=0
                print("Sleeping for 1 sec..................")
                time.sleep(1)

    def copy_template(self,files):
        for file in files:
            self.insert_file_rows(file)
            print()
    def insert_file_rows(self, file):
        if "/" in file:
            name = (file.split("/")[-1]).split(".")[0]
        else:
            name = file.split(".")[0]
        
        df = pd.read_csv(file)
        cols = df.columns
        
        # Create table if not exists
        self.connection("""CREATE TABLE IF NOT EXISTS {} (
                   id INT AUTO_INCREMENT PRIMARY KEY,
                   SID VARCHAR(255),
                   Destination VARCHAR(255),
                   Content  VARCHAR(255)
        )""".format(str(name)))
        
        # Check if the number of columns match
        if len(cols) != 3:
            print("Number of columns in DataFrame doesn't match the expected count.")
            return
        
        src, dst, msg = str(cols[0]), str(cols[1]), str(cols[2])
        print("Df:", df)
        
        for i, row in df.iterrows():
            # Insert values into the table
            self.connection("INSERT INTO {}(SID, Destination, Content) VALUES ('{}', '{}', '{}')".format(name, str(row.iloc[0]), str(row.iloc[1]), str(row.iloc[2])))

    def checked(self,name):
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        self.connection("""CREATE TABLE IF NOT EXISTS generator(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,ip varchar(255),file VARCHAR(255),SMS int,total varchar(255)) """)
        cursor = connection.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM {}".format(name))
        count = cursor.fetchone()[0]
        connection.close()
        print("count:",count)
        return count
    def main(self, ip, port, user, password, files, repeat=False, a=0,total=0,last_id=1):
        total=int(total)
        self.connection("UPDATE generator set SMS={} where ip='{}'".format(0,str(str(ip)+":"+str(port))))
        # Set up logging for debugging
        #logging.basicConfig(level='INFO')

        # Two parts, GSM default / UCS2, SMS with UDH

        client = smpplib.client.Client(str(ip),int(port) )

        # Print when obtain message_id
        client.set_message_sent_handler(
            lambda pdu: logging.info('submit_sm_resp seqno: {} msgid: {}'.format(pdu.sequence, pdu.message_id)))

        # Handle delivery receipts (and any MO SMS)
        def handle_deliver_sm(pdu):
                logging.info('delivered msgid:{}'.format(pdu.receipted_message_id))
                return 0 # cmd status for deliver_sm_resp

        client.set_message_received_handler(lambda pdu: handle_deliver_sm(pdu))
        client.connect()
        client.bind_transceiver(system_id=str(user), password=str(password))

        print("Files:{},length:{}".format(files,len(files)))
        print("main args:",ip, port, user, password, files, repeat, total, a,last_id)
        
        if repeat:
            if isinstance(files, str):
                    if len(list(files.split(",")))==1 :
                        total=total
                    elif len(files)>1:
                        total=int(total/len(list(files.split(","))))
                    else:
                        print("No Files Inputed.......")
                    print("Before sending.........",files)
                    self.send_per_amount(client, files, a, total,last_id,user,password)
            else:
                if len(list(files))==1:
                    #print("compare Achieved!!!!!!")
                    total=total
                elif len(files)>1:
                           total=int(total/len(list(files)))
                else:
                           print("No Files Inputed.......")
                print("Before sending.........",files)
                self.send_per_amount(client, files, a, total,last_id,user,password)            
        else:
                # Otherwise, send SMS per file
                #print("Repeat in main= False")
                file_list=",".join(files)
                name=file_list.split(",")[0].split("/")[-1].split(".")[0]

                rows=self.checked(name)
                if(int(total)>=int(rows)):
                    total=rows
                else:
                    total=total
                if isinstance(files, str):
                    if len(list(files.split(",")))==1 :
                    #print("compare Achieved!!!!!!")
                        total=int(total)+int(a)
                    elif len(list(files.split(",")))>1:
                        total=int(total/len(list(files.split(","))))+int(a)
                    else:
                        print("No Files Inputed.......")
                    print("Before sending.........",total)

                else:

                       if len(list(files))==1 :
                    #print("compare Achieved!!!!!!")
                           total=int(total)+int(a)
                       elif len(files)>1:
                           total=int(total/len(list(files)))+int(a)
                       else:
                           print("No Files Inputed.......")
                       print("Before sending.........",files)
                print("\n\nTotal Before running",total)
                self.sms_per_files(client, files,2,int(total),last_id,user,password,0,a,False)
        
class frontend(sms_generator) :
    

    
    def check(self):
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        self.connection("""CREATE TABLE IF NOT EXISTS generator(id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,file VARCHAR(255),SMS int) """)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM generator")
        count = cursor.fetchone()[0]
        connection.close()
        return count == 0
    def rows_gen(self):
            connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM generator")
            count = cursor.fetchall()
            connection.close()
            count = [item[0] for item in count]

            print(count)
            return count
    def load_config(self,l):
        if sys.platform==platforms["win32"]:
            l=l.replace("\\","\\\\")
        else:
            pass
        print("l value:",l,sys.platform)
        config= configparser.RawConfigParser()   
        configFilePath = r'{}'.format(str(l))
        config.read(configFilePath)
        print(config)        
        # Get values from the config object
        ip = config["config"]["ip"]
        port = config["config"]["port"]
        user = config["config"]["username"]
        password = config["config"]["password"]
        files = config["config"]["files"].split(",")
        repeat = config["config"].getboolean("repeat")  # Assuming repeat is a boolean value in the config
        total = config["config"]["Total"]        # Assuming total is an integer value in the config
        a = config["config"]["SMS/sec"]                      # Assuming a is a string value in the config
        return ip, port, user, password, files, repeat, total, a
    
    def delete_generator(self,file,num):
        self.connection("delete from generator_{} where id={}".format(file.split("/")[-1]))
        self.connection("DELETE FROM generator WHERE id={}".format(int(num)))

   
class MainWindow(QMainWindow,frontend):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        ### Set Main Background to transparent
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ###Shadow effect stylota
        self.shadow=QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0,92,157,550))
        ### Apply Shadow Effect to Central Widget
        self.ui.centralwidget.setGraphicsEffect(self.shadow)
        ### set window Icon
        self.setWindowIcon(QtGui.QIcon(":/icons/icons/mail.svg"))
        ### Set Window Tittle
        self.setWindowTitle("SMPP")
        ### Window Size grip to Resize
#        QSizeGrip(self.ui.size_grip)
        self.ui.close_window.clicked.connect(lambda:self.close())
        self.ui.minimize_window.clicked.connect(lambda:self.showMinimized())
        self.ui.restore_window.clicked.connect(lambda:self.restore_or_maximize_window())
        
        ## To Dashboard
        self.ui.dashboard_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.Dashbord) )
        ## To Setting Page
        self.ui.setting_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.Configuration) )
        ## To Server Page
        self.ui.server_btn.clicked.connect(lambda:self.ui.stackedWidget.setCurrentWidget(self.ui.Server) )
        
        def moveWindow(e):
            ### roundProgressBar(self.cpu_percent)
            ### spiralProgressBar(self.ram_percent)
            if self.isMaximized()==False:### Not Maximized
                if e.buttons()==Qt.LeftButton or e.buttons()==Qt.RightButton:
                    self.move(self.pos()+e.globalPos()-self.clickPosition)
                    #print("Positions:\nPosition:{}\nGlobal Position:{}\nClicked Position:{}".format(self.pos(), e.globalPos(),self.clickPosition))
                    self.clickPosition=e.globalPos()
                    e.accept()
        ### Move Window
        self.ui.header.mouseMoveEvent=moveWindow
        ### Menu Animation
        self.ui.Menu_btn.clicked.connect(lambda: self.slideLeftMenu())
        
        #apply_stylesheet(app,theme='dark_cyan.xml')

        for w in self.ui.menu_frame.findChildren(QPushButton):
            w.clicked.connect(self.applyButtonStyle)
        
        self.ui.configFile_btn.clicked.connect(self.configFile)
        ## Files
        
        self.ui.save_btn.clicked.connect(lambda:self.save(fname))
        ## Dashboard Function
        self.dashboard()
        ## Settings Function
        #self.settings()
        self.show()
    
    def configFile(self):
        global fname
        fname, _ = QFileDialog.getOpenFileName(self.ui.configFile_btn, "Load Configuration File",".", "Configuration File (*.txt,*.cfg);;All Files (*)")
        print("fname:",fname)
        self.ui.config_path.setText(str(fname))
        global use_method
        use_method=1
        
        fname=fname
        
    def save(self,fname):
        #self.checked()
        print("Save Is Clicked !!!!!! with use method ",use_method)
        print("fname:",fname)
        if self.ui.comboBox.currentText()=="Add":
            if use_method==1:
                print("Add Is Clicked !!!!!! with use method 1")
                ip, port, user, password, files, repeat, total, a=self.load_config(fname)
                files=list(files)
                print("Infos:\n",ip, port, user, password, files, repeat, total, a)
                print("Repeat:",repeat)
                gen_obj=sms_generator(ip, port, user, password, files, repeat, total, a)
                gen_obj.Generator()
                gen_obj.copy_template(files)
                last_id=self.get_last_id()
                
                gen_obj.main(ip, port, user, password, files, repeat, a, int(total),last_id)
            else:
                ip=self.ui.ip_line.text()
                port=self.ui.port_line.text()
                user=self.ui.username_line.text()
                password=self.ui.password_line.text()
                files=self.ui.template_2.clicked.connect(self.templates)
                repeat=self.ui.checkBox.checked()
                a=int(self.ui.sms_line.text())
                total=int(self.ui.total_line.text())
                last_id=self.get_last_id()
                gen_obj=sms_generator(ip, port, user, password, files, repeat, int(total), a)
                gen_obj.Generator()
                gen_obj.copy_template(files)
#def main(self, ip, port, user, password, files, repeat=False, a=0,total=0,last_id=1)
#def __init__(self, ip="", port="", user="", password="H@mza123456789", files=[], repeat=False, amount=0, amount_per_sec=0):
                gen_obj.main(ip, port, user, password, files, repeat, a, int(total)-1,last_id)
            self.ui.comboBox.setCurrentIndex(0)
        #if self.ui.comboBox.currentText()=="edit":
        
        if self.ui.comboBox.currentText()=="Remove":
            if use_method==1:
                ip, port, user, password, files, repeat, total, a=self.load_config(fname)
                num=self.get_generator_data(str(str(ip)+":"+str(port)),files)
                
                ip, port, user, password, files, repeat, total, a=self.get_data_by_id(num)
                name=files.split(",")[0].split("/")[-1].split(".")[0]
                self.delete_generator(name,num)
    def get_generator_data(self,ip,file):
        connection = connect(host="localhost", user="root", password="H@mza123456789", database="templates")
        cursor = connection.cursor()
        query = "SELECT id FROM generator where ip='{}' and file='{}'".format(ip,file)
        print("\nQuery:",query,"\n")
        cursor.execute(query)
        data = cursor.fetchall()[0]
        connection.close()
        print("\nData:",data)
        return data
        ######## Menu Button Styling Function
                
    def create_table_widget(self,rowPosition,columnPosition,text,tableName):
        qtable=QTableWidgetItem()
        #USE getattr() Method
        getattr(self.ui,tableName).setItem(rowPosition,columnPosition,qtable)
        qtablei=getattr(self.ui,tableName).item(rowPosition,columnPosition)
        qtablei.setText(text)
    def fetch(self,name,items):
        for i in items:
            if name in i:
                return False
            else:
                pass
        return True
    def findName(self):
        name = self.ui.search_generator.text().lower()
        for row in range(self.ui.generator.rowCount()):
            items = []  # Clear the items list for each row
            for i in range(5):
                item = self.ui.generator.item(row, i)
                print("Item:", item.text().lower())
                if item is not None:  # Check if item exists before accessing its text
                    items.append(str(item.text().lower()))
            try:
                self.ui.generator.setRowHidden(row, self.fetch(name,items))
            except Exception as e:
                print("Error:", e)
    def dashboard(self):
        try:
            # Loop through data and create a row for each item
            for x in self.get_all_data():
                print("\n\n\n",x,"\n\n\n")
                print("x[4]:{},x[3]:{}".format(x[4],x[3]))
                x3=int(float(str(x[3])))
                x4=int(float(str(x[4])))
                rowPosition = self.ui.generator.rowCount()  # Get the current row count
                self.ui.generator.insertRow(rowPosition)  # Insert a new row

                # Create table widgets for each column
                self.create_table_widget(rowPosition, 0, str(x[0]), "generator")
                self.create_table_widget(rowPosition, 1, "Generator " + str(x[0]), "generator")
                self.create_table_widget(rowPosition, 2, str(x[1]), "generator")
                self.create_table_widget(rowPosition, 3, str(x[2]), "generator")
                self.create_table_widget(rowPosition, 4, str(x3), "generator")

                # Create a progress bar and set its value
                progressBar = QProgressBar()
                progressBar.setObjectName("progressBar")
                progressBar.setMaximum(100)  # Set the maximum value to 100
                self.ui.generator.setCellWidget(rowPosition, 5, progressBar)  # Place the progress bar in the table
                self.update_progress_bar(rowPosition, int(x3), int(x4))  # Set the initial progress value
                
                # Create and configure "Run" button
                run_btn = QPushButton("Run")
                run_btn.setStyleSheet("color: orange;")
                self.ui.generator.setCellWidget(rowPosition, 6, run_btn)

                # Create and configure "Edit" button
                edit_btn = QPushButton("EDIT")
                edit_btn.setStyleSheet("color: Red;")
                self.ui.generator.setCellWidget(rowPosition, 7, edit_btn)

                # Connect buttons to their respective slot functions
                edit_btn.clicked.connect(lambda id=x[0], name="Generator " + str(x[0]), ip=x[1], template=x[2]: self.launch_edit(id, name, ip, template))

                # Retrieve generator data for the "Run" button action
                id = int(x[0])
                ip, port, user, password, files, repeat, total, a = self.get_data_by_id(id)
                print("Get Data By Id:",ip, port, user, password, files, repeat, total, a)
                gen_obj = sms_generator(ip, port, user, password, files, repeat, total, a)
                #remove_btn=
                # Connect "Run" button to run the generator's main method
                run_btn.clicked.connect(lambda ip=ip, port=port, user=user, password=password, files=files, repeat=repeat, total=int(total)+1, a=a, last_id=id: gen_obj.main(ip, port, user, password, files, repeat, a, total, id))

                # Schedule progress bar refresh every second
                QTimer.singleShot(1000, lambda row=rowPosition,x3=x3,x4=x4, id=id: self.refresh_progress(row, id,int(x3),int(x4)))  # Refresh every second

            # Connect search box text changed signal to the appropriate slot
            self.ui.search_generator.textChanged.connect(self.findName)

        except Exception as e:
            print(f"An error occurred: {e}")  # Handle exceptions gracefully
    def update_progress_bar(self, row, current_value, total_value):
        progressBar = self.ui.generator.cellWidget(row, 5)
        if progressBar:
            percentage = (current_value / total_value) * 100
            progressBar.setValue(int(percentage))

    def refresh_progress(self, row, id,current_value,total_value):
    # Simulated function to fetch the latest data
        self.update_progress_bar(row, current_value, total_value)
        QTimer.singleShot(1000, lambda: self.refresh_progress(row, id,current_value,total_value))  # Schedule next refresh




        

    def launch_edit(self,idi,gen,ip,temp):
    # Create a QDialog instance for the edit window
        edit_dialog = QtWidgets.QDialog()
        ui_edit = Ui_Form()
        ui_edit.setupUi(edit_dialog)
        ui_edit.id_line.setText(str(idi))
        ui_edit.ip_line.setText(str(ip))
        ui_edit.temp_line.setText(str(temp))
        ui_edit.generator_line.setText(str(gen))
        edit_dialog.exec_()


    def applyButtonStyle(self):
        ## Reset Style For other Buttons
        for w in self.ui.menu_frame.findChildren(QPushButton):
            # If Button name is not equal to clicked button name
            if w.objectName()!=self.sender().objectName():
                ## Default border style
                w.setStyleSheet("border-bottom:none none;")
        self.sender().setStyleSheet("border-bottom:2px solid")
        return
             
    def slideLeftMenu(self):
        width=self.ui.left_frame_count.width()
        if width==40:
            newWidth=200
        else:
            newWidth=40
        self.animation=QPropertyAnimation(self.ui.left_frame_count,b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()
    def mousePressEvent(self,Event):
        self.clickPosition=Event.globalPos()
    
    def restore_or_maximize_window(self):
        if self.isMaximized():
            
            self.showNormal()
            width=self.ui.generator.width()
            newWidth=width-int(width*0.5)
            self.animation=QPropertyAnimation(self.ui.generator,b"minimumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(newWidth)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
        else:
            self.showMaximized()
            width=self.ui.generator.width()
            newWidth=width+int(width*0.5)
            self.animation=QPropertyAnimation(self.ui.generator,b"minimumWidth")
            self.animation.setDuration(250)
            self.animation.setStartValue(width)
            self.animation.setEndValue(newWidth)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
if __name__=="__main__":
    #print("Sys.Argv:",sys.argv)
    app= QApplication(sys.argv)
    window=MainWindow()
    sys.exit(app.exec_())

