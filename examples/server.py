import socket
import sys
import examples.pakbus as pakbus
import threading

def FileNetowr(ip, name):
    s = pakbus.open_socket(ip, 6785, 30)
    FileData, RespCode = pakbus.fileupload(s, 1, 2050, FileName='.TDF')

    if FileData:
        tabledef = pakbus.parse_tabledef(FileData)
        # for tableno in range(1, len(tabledef) + 1):
        #     print ('Table %d: %s' % (tableno, tabledef[tableno - 1]['Header']['TableName']))
        #     print ('Table signature: 0x%X' % tabledef[tableno - 1]['Signature'])
        #     print ('Header:', tabledef[tableno - 1]['Header'])
        #     for fieldno in range(1, len(tabledef[tableno - 1]['Fields']) + 1):
        #         print ('Field %d:' % (fieldno), tabledef[tableno - 1]['Fields'][fieldno - 1])
        #     print

    a, b = pakbus.collect_data(s, 1, 2050, tabledef, TableName='Public')
    print(a)

    path = "/home/uxfac/"

    pkt = pakbus.pkt_bye_cmd(1, 2050)
    pakbus.send(s, pkt)

    s.close()

class AsyncTask:
    def __init__(self):
        pass

    def TaskA(self):
        print ('Process A')
        FileNetowr("106.249.253.227", "YangYang")
        threading.Timer(60*10, self.TaskA).start()

    def TaskB(self):
        print ('Process B')
        FileNetowr("210.223.199.221", "Buan")
        threading.Timer(60*10, self.TaskB).start()

    def TaskC(self):
        print ('Process C')
        FileNetowr("147.46.138.187","Seoul")
        threading.Timer(60*10, self.TaskB).start()

    def TaskD(self):
        print ('Process D')
        FileNetowr("1.209.192.61","JeJu")
        threading.Timer(60*10, self.TaskB).start()


def main():
    print 'Async Function'
    at = AsyncTask()
    at.TaskA()

    at.TaskB()
    at.TaskC()
    at.TaskD()


if __name__ == '__main__':
    main()
