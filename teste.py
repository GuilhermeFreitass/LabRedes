#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import os

def get_dns_service():
    # Realiza uma consulta DNS para determinar o endereço IP do serviço de nome
    dns_ip = socket.gethostbyname('192.0.2.100')
    return dns_ip

def get_web_service():
    # Conecta-se ao serviço web para determinar o endereço IP e a porta
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(('192.0.2.100', 80))
        web_ip, web_port = s.getpeername()
        return web_ip, web_port
    except socket.error:
        return None, None
    finally:
        s.close()

def capture_traffic():
    # Captura o tráfego gerado ao testar se os serviços estão funcionando corretamente
    filename = "traffic_capture.pcap"
    os.system("sudo tcpdump -i any -w {0} host 192.0.2.100".format(filename))
    print "Captura de tráfego concluída."

def test_host_online():
    # Testa se o host está online
    response = os.system("ping -c 1 192.0.2.100 > /dev/null")
    if response == 0:
        print "O host está online."
    else:
        print "O host está offline."

def test_web_service(ip, port):
    # Testa se o serviço web está respondendo corretamente
    response = os.system("curl -s {0}:{1} > /dev/null".format(ip, port))
    if response == 0:
        print "O serviço web está respondendo corretamente."
    else:
        print "O serviço web não está respondendo corretamente."

def main():
    # Obter IPs e portas dos serviços de nome e web
    dns_ip = get_dns_service()
    web_ip, web_port = get_web_service()

    print "Serviço de Nome:"
    print "IP:", dns_ip

    if web_ip:
        print "\nServiço Web:"
        print "IP:", web_ip
        print "Porta:", web_port
    else:
        print "\nServiço Web indisponível."

    # Capturar tráfego
    capture_traffic()

    # Testar se o host está online
    test_host_online()

    if web_ip:
        # Testar se o serviço web está respondendo corretamente
        test_web_service(web_ip, web_port)

if __name__ == "__main__":
    main()
