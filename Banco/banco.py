from api import *

def main():
    global tem_token, ip
    porta = 8081  # Porta fixa

    iniciar()

    thread_servidor = threading.Thread(target=iniciar_servidor, args=(ip, porta))
    thread_servidor.start()

    thread_monitor = threading.Thread(target=monitorar_token)
    thread_monitor.start()

    thread_process = threading.Thread(target=processamento)
    thread_process.start()
    
if __name__ == "__main__":
    main()
