#-------------------------------------------------------------------------------
# Name:     Xroxy Proxy Grabber/Tester with GUI
# Purpose:      Test to see if proxies work
#
# Author:      DontWorry
#
# Created:     21/08/2011
# Copyright:   (c) DontWorry 2011
# Licence:     Open sourced
#-------------------------------------------------------------------------------
#!/usr/bin/env python

from fltk import *
import re
import urllib
import urllib2
import base64
import thread


def grabIp(r = 0, s = 0):
        rangePages = fl_input("What page do you want to start at?")
        choosePages = fl_input("What page do you want to end at?")
        r = int(rangePages)
        s = int(choosePages)

        while r < s+1:
                proxyInput = 'http://www.xroxy.com/proxylist.php?port=&type=Not_codeen&ssl=&country=&latency=&reliability=&sort=reliability&desc=true&pnum=%s#table' % (r)
                print "Grabbing data from page: ", r
                userAgent = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
                requestData = urllib2.Request(proxyInput, headers={ 'User-Agent': userAgent })
                proxyRead = urllib2.urlopen(requestData)
                readIps = proxyRead.read()
                ipAddress = re.findall(r'host=\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', readIps)
                portNumber = re.findall(r'port=\d{1,5}', readIps)

                for matches in ipAddress:
                        ipList.append(matches)
                for port in portNumber:
                        portList.append(port)

                r +=1


        for ip in ipList:
                ipBroken = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip)
                for ips in ipBroken:
                        ipList2.append(ips)
        for po in portList:
                portBroken = re.findall(r'\d{1,5}', po)
                for ports in portBroken:
                        portList2.append(ports)
        fakeIpList = ipList2[:]
        fakePortList = portList2[:]



        while True:
                try:
                        ipLists.add(fakeIpList[0]+":"+fakePortList[0])
                        fakeIpList.remove(fakeIpList[0])
                        fakePortList.remove(fakePortList[0])
                except:
                        fl_message("Done gathering IP's!")
                        break

def checkIps(x):
        g = 0
        b = 0
        good = int(g)
        bad = int(b)
        timeOut = int(fl_input("Enter a timeout for checking your proxies"))
        while True:
                try:
                        ipPort = ipLists.text(1)
                        proxies = {'http':'http://'+ipPort}
                        print "Trying to connect to: ", ipPort
                        loadProxy = urllib2.ProxyHandler(proxies)
                        proxyOpener = urllib2.build_opener(loadProxy)
                        installOpen = urllib2.install_opener(proxyOpener)
                        filehandle = urllib2.urlopen(base64.decodestring('aHR0cDovL2ljYW5oYXppcC5jb20v'), timeout=timeOut)
                        if filehandle.read()[:-1]+':'+portList2[0] == ipPort:
                                good+=1
                                validIp.add(ipPort)
                                win.redraw()
                                print "Succesfully recieved data from: ", ipPort
                        else:
                                bad+=1
                                invalidIp.add(ipPort)
                                print "Failed to recieve data from: ", ipPort
                                win.redraw()
                        ipLists.remove(1)
                except IOError:
                        ipLists.remove(1)
                        print "Failed to recieve data from: ", ipPort
                        pass
                except:
                        fl_message("Finished validating IP's. Please save to file to prevent data loss.")
                        break



def savingFile(x):
        fname2 = fl_file_chooser('Save File','*.txt',None)
        f = open(fname2,'w')
        try:
                test = validIp.size()
                while True:
                        f.write(validIp.text(test)+'\n')
                        test -= 1
        except:
                fl_message("Done Saving")
                f.close()

win = Fl_Window(200,200,400,450, "Xroxy Proxy Grabber GUI")
ipList = []
portList = []
ipList2 = []
portList2 = []
win.begin()
ipLists = Fl_Browser(50,25,300,150, "IP's")
validIp = Fl_Browser(50,200,150,150, "Working Proxies")
invalidIp = Fl_Browser(200,200,150,150, "Non-Working Proxies")
startSearch = Fl_Button(50,380,100,50, "Start")
startValidate = Fl_Button(250,380,100,50, "Validate")
startSave = Fl_Button(150,380,100,50, "Save")
win.end()

startSearch.callback(grabIp)
startValidate.callback(checkIps)
startSave.callback(savingFile)

Fl.scheme("plastic")
win.show()
Fl.run()
