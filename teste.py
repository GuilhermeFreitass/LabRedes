import socket
import subprocess
import os

def get_dns_service():
    # Realiza uma consulta DNS para determinar o endereço IP do serviço de nome
    dns_ip = socket.gethostbyname('exemplo.psi.br')
    return dns_ip

def get_web_service():
    # Conecta-se ao serviço web para determinar o endereço IP e a porta
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(('exemplo.psi.br', 80))
            web_ip, web_port = s.getpeername()
            return web_ip, web_port
        except ConnectionRefusedError:
            return None, None

def capture_traffic():
    # Captura o tráfego gerado ao testar se os serviços estão funcionando corretamente
    filename = "traffic_capture.pcap"
    proc = subprocess.Popen(["sudo", "tcpdump", "-i", "any", "-w", filename, "host", "exemplo.psi.br"])

    # Aguarda até que o processo de captura seja concluído
    proc.communicate()

    print(f"Captura de tráfego concluída. Arquivo: {filename}")

def test_host_online():
    # Testa se o host está online
    response = subprocess.run(["ping", "-c", "1", "exemplo.psi.br"], stdout=subprocess.PIPE)
    if response.returncode == 0:
        print("O host está online.")
    else:
        print("O host está offline.")

def test_web_service(ip, port):
    # Testa se o serviço web está respondendo corretamente
    response = subprocess.run(["curl", "-s", f"{ip}:{port}"], stdout=subprocess.PIPE)
    if response.returncode == 0:
        print("O serviço web está respondendo corretamente.")
    else:
        print("O serviço web não está respondendo corretamente.")

def main():
    # Obter IPs e portas dos serviços de nome e web
    dns_ip = get_dns_service()
    web_ip, web_port = get_web_service()

    print("Serviço de Nome:")
    print("IP:", dns_ip)

    if web_ip:
        print("\nServiço Web:")
        print("IP:", web_ip)
        print("Porta:", web_port)
    else:
        print("\nServiço Web indisponível.")

    # Capturar tráfego
    capture_traffic()

    # Testar se o host está online
    test_host_online()

    if web_ip:
        # Testar se o serviço web está respondendo corretamente
        test_web_service(web_ip, web_port)

if __name__ == "__main__":
    main()
