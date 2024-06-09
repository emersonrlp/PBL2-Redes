from nova_api import app

def main():
    try:
        # Inicia a aplicação Flask
        app.run(host='0.0.0.0', port=8081, debug=True, threaded=True)

    except Exception as e:
        print('Erro:', e)

if __name__ == "__main__":
    main()
