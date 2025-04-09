import socket
import threading
import sys
import time


LOCAL_IP = '0.0.0.0'
PORT = 8080
TIMEOUT = 15


def receive_messages(sock, peer_ip):
    while True:
        try:
            sock.settimeout(TIMEOUT)
            data, addr = sock.recvfrom(1024)
            print(f"\n接收到消息: {data.decode()}")

            # 回复ACK
            ack_message = "ACK"
            sock.sendto(ack_message.encode(), (peer_ip, PORT))
            print(f"发送确认: {ack_message}")
        except socket.timeout:
            print("接收超时")
        except KeyboardInterrupt:
            print("接收线程关闭")
            break


def send_messages(sock, peer_ip):
    try:
        while True:
            message = input("输入消息: ")
            if message.lower() == 'exit':
                break

            # 发送消息
            sock.sendto(message.encode(), (peer_ip, PORT))
            print(f"发送消息: {message}")

            # 等待ACK
            sock.settimeout(TIMEOUT)
            try:
                data, addr = sock.recvfrom(1024)
                print(f"接收到来自 {addr} 的确认: {data.decode()}")
            except socket.timeout:
                print("未收到确认，重新发送...")
                continue
    except KeyboardInterrupt:
        print("发送线程关闭")


def main():
    if len(sys.argv) != 3 or sys.argv[1] not in ['send', 'receive']:
        print("用法: python link.py <send/receive> <peer_ip>")
        return

    mode, peer_ip = sys.argv[1], sys.argv[2]

    # 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((LOCAL_IP, PORT))

    # 接收
    receiver_thread = threading.Thread(target=receive_messages, args=(sock, peer_ip))
    receiver_thread.daemon = True
    receiver_thread.start()

    if mode == 'send':
        print(f"开始发送模式，对等节点IP: {peer_ip}")
        send_messages(sock, peer_ip)
    else:
        print(f"开始接收模式，对等节点IP: {peer_ip}")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("接收模式关闭")

    sock.close()


if __name__ == "__main__":
    main()