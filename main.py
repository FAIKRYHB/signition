# -*- coding: utf-8 -*-


import sys

import os,time, ntpath, hashlib,base64

from zipfile import ZipFile
from os.path import basename
from PyQt5.QtWidgets import QApplication, QMainWindow, QStatusBar, QFileDialog
from PyQt5 import QtGui, uic

from rsa import RSA 



qtCreatorFile = "dialog.ui"

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class Signition(QMainWindow, Ui_MainWindow):
    selectedFile = ""
    rsaClass = None
    def loadFileAction(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "", options=options)
        
        info = os.stat(fileName);
        head, tail = ntpath.split(fileName);
        name, ext = tail.split(".")
        self.nazev.setText(name)
        self.typ.setText(ext)
        self.cesta.setText(fileName)
        self.velikost.setText(str(info.st_size)+"B")
        self.datum.setText(str(time.asctime(time.localtime(info.st_mtime))))
        
        self.selectedFile = fileName
        
    def saveFileAction(self):
        hashFunction = hashlib.sha256()
        
        with open(self.selectedFile,"rb") as f:
            for byte_block in iter(lambda: f.read(4096),b""):
                hashFunction.update(byte_block)
            #print(hashFunction.hexdigest())
            
            podpis = self.rsaClass.podepsat(hashFunction.hexdigest())
            tempSign = "rsa.sign"
            sign = open(tempSign,"w")
            encoded = str(base64.b64encode(podpis.encode())).replace("b'","").replace("'","")
            
            
            
            sign.write("RSA_SHA256 " + encoded)
            sign.close()
            
            
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                   "Zip file (*.zip)", options=options)
            print(fileName)
            
            ext = _.split(".")[1].replace(")","")
            
            if(fileName.find(ext) < 0):
                fileName = fileName + "." + ext
            with ZipFile(fileName,"w") as zip:
                zip.write(self.selectedFile,basename(self.selectedFile))
                zip.write(tempSign)
                zip.close()
                
                os.remove(tempSign)
            keyName = basename(fileName).split(".")[0]
            path = fileName.replace(basename(fileName),"")
            
            publicKey = str(base64.b64encode(str("("+ str(self.rsaClass.n)+","+str(self.rsaClass.e)+")").encode())).replace("b'","").replace("'","")
            privateKey = str(base64.b64encode(str("("+ str(self.rsaClass.n)+","+str(self.rsaClass.d)+")").encode())).replace("b'","").replace("'","")
            
            verejny = open(path+keyName+".pub","w")
            verejny.write("RSA "+publicKey)
            verejny.close()
            
            soukromy = open(path+keyName+".priv","w")
            soukromy.write("RSA "+privateKey)
            soukromy.close()
            
            
    def loadPubAction(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Public key file (*.pub)", options=options)
        ext = _.split(".")[1].replace(")","")
            
        if(fileName.find(ext) < 0):
            fileName = fileName + "." + ext
        
        f = open(fileName,"r")
        n,e = base64.b64decode(f.read().split(" ")[1]).decode("utf-8").replace("(","").replace(")","").split(",")
        
        self.rsaClass.n = n
        self.rsaClass.e = e
        
        self.pubKeyState.setText("Veřejný klíč načten")
    def loadZipAction(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "Zip file (*.zip)", options=options)
        ext = _.split(".")[1].replace(")","")
            
        if(fileName.find(ext) < 0):
            fileName = fileName + "." + ext
            
        
    def __init__(self):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.rsaClass = RSA()
        self.loadFileButton.clicked.connect(self.loadFileAction)
        self.saveFileButton.clicked.connect(self.saveFileAction)
        self.loadPubButton.clicked.connect(self.loadPubAction)
        self.loadZipedButton.clicked.connect(self.loadZipAction)
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Signition()
    window.show()
    sys.exit(app.exec_())

