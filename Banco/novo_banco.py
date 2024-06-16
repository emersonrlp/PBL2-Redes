from nova_api import *

def main():
    ip = get_local_ip()
    port = 5000  # Porta fixa

    init()

    server_thread = threading.Thread(target=start_server, args=(ip, port))
    server_thread.start()

    monitor_thread = threading.Thread(target=monitor_token)
    monitor_thread.start()

    verifica_token()
    
if __name__ == "__main__":
    main()
