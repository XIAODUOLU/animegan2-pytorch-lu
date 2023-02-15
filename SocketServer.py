"""
使用Socket通信，完成:
手机上传雾图，服务器分析后回传
"""
import cv2
import time
import argparse
import os
import torch

#from deblurgan.model import generator_model, discriminator_model, generator_containing_discriminator_multiple_outputs

from model import Generator

torch.backends.cudnn.enabled = False
torch.backends.cudnn.benchmark = False
torch.backends.cudnn.deterministic = True
    

import numpy as np
import socket
import sys

received_path = './images/cache.jpg'
sent_path = './output/cache.jpg'
def save_file(sock):
    """
    从sock中获取数据，并保存下来
    :param sock:
    :return:
    """
    with open(received_path, 'wb') as f:
        print('file opened')
        while True:
            data = sock.recv(1024)
            # print()
            if not data:
                break
            elif 'EOF' in str(data):
                f.write(data[:-len('EFO')])
                break
            # write data to a file
            f.write(data)
    # sock.close()
    print('pic received finished')

def send_img(sock):
    # 发送处理后的图片
    with open(sent_path, 'rb') as f:
        for data in f:
            sock.send(data)
    print('send finished')
    

def socket_service():
    """
    开启socket服务
    :return:
    """
    # 开启socket服务
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind(('192.168.43.215', 13408))
        s.listen(10)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("Wait")

    

    # 等待连接并处理
    while True:
        
        try:
            sock, _ = s.accept()
            save_file(sock)
            sock.close()
            os.system("python test.py --input_dir ./images --output_dir ./output --checkpoint ./face_paint_512_v2_0.pt --device cpu")
            sock, _ = s.accept()
            send_img(sock)
            sock.close()
        except Exception as reason:
            print(reason)
        

if __name__ == '__main__':
    
    socket_service()
