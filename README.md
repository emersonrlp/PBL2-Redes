<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body> 
  <h1>Internet das Coisas</h1>
    <p>Devido aos avanços tecnológicos nas áreas de sitemas embarcados, microeletrônica, comunicação e sensoriamento, o termo Internet das Coisas (<em>Internet of things</em>, IoT) criado por Kevin Ashton, vem sendo muito discutido nos dias atuais frente as possíveis aplicações as mais diversas áreas como saúde, energia, cidades inteligentes, etc.</p>
    <p></p>
    <p>Mediante a isso, esse projeto tem o intuito de realizar a conexão de dispositivos simulados via script em python com uma interface cliente por meio de um sistema de mensageria chamado de broker, sendo utilizados para isso os protocolos de comunicação TCP e UDP para a comunicação dispositivo-broker e uma API em python para realizar a comunicação broker-cliente.</p>
    <h2>Arquiterura do Projeto</h2>
    O projeto funciona da seguinte forma:
        <ol>
            <li>O broker inicializa o servidor TCP, o servidor UDP e a API para poder trocar mensagens com os dispositivos e com os clientes.</li>
            <li>O dispositivo tenta se conectar ao servidor para poder receber mensagens TCP e envia dados UDP periodicamente ao broker.</li>
            <li>O cliente comunica com a API as solicitações que ele deseja fazer ao broker.</li>
            <br>
            <div align="center">
                <figure>
                    <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-04-24%20210107.png" alt="Descrição da Imagem">
                    <br>
                    <figcaption>Arquitetura do Projeto</figcaption>
                </figure>
            </div>
        </ol>
    <h3>Comunicação Cliente-Broker</h3>
    Para a comunicação entre o cliente e o broker foi utilizada uma API RESTful que possui uma rota para os sensores <strong>http://localhost:8081/sensores</strong> e uma rota para as solicitações <strong>http://localhost:8081/solicitacoes</strong>, cada uma delas possui um método <strong>POST</strong>, <strong>GET</strong>, <strong>PUT</strong> e <strong>DELETE</strong> para fazer possíveis alterações.
    <h4>Sobre os Métodos</h4>
        <ul>
            <p>-<strong>POST</strong>, método responsável por criar um item na rota expecíficada.</p>
            <p>-<strong>GET</strong>, método responsável por pegar um item na rota expecíficada.</p>
            <p>-<strong>PUT</strong>, método responsável por atualizar um item na rota expecíficada.</p>
            <p>-<strong>DELETE</strong>, método responsável por deletar um item na rota expecíficada.</p>
        </ul>
    <p><strong>Obs.:</strong> para testar se as rotas estavam funcionando foi utilizado o software Insomnia.</p>
    <br>
    <p>Os dados salvos nessas rotas são guardados no formato parecido com o de um dicionário, possuindo chave:valor.</p>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-03%20165615.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Exemplo do Formato</figcaption>
            </figure>
        </div>
    <br>
    <p>Basicamente o que é feito quando chega um dado novo ao broker pelo dispositivo é que o dado é atualizado de acordo com o endereço IP do dispositivo no dicionário, para que o cliente possua o dado mais atualizado caso solicite esse dado por solicitação pela rota <strong>http://localhost:8081/solicitacoes</strong>, já quando o cliente manda uma solicitação para a rota <strong>http://localhost:8081/solicitacoes</strong>, ela é verificada pelo broker e então repassada para o dispositivo solicitado.</p>
    <p>Segue uma figura ilustrativa sobre essa troca de mensagens.</p>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-03%20210254.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Comunicação Cliente-Broker</figcaption>
            </figure>
        </div>
    <br>
    <h3>Comunicação Dispositivo-Broker</h3>
        <p>Para a comunicação entre o dispositivo e o broker foi utilizados dois protocolos, o TCP para envio de comandos/solicitações do broker para o dispositivo e o UDP para envio de dados do dispositivo para o broker.</p>
        <p>Mas, para que utilizar dois protocolos diferentes?</p>
        <p><strong>TCP</strong>, o protocolo de comunicação TCP foi utilizado no projeto para o envio de comandos/solicitações para os dispositivos porque é necessário garantir que aqueles dados foram entregues com sucesso, o que não é garantido pelo protocolo UDP.</p>
        <p><strong>UDP</strong>, o protocolo de comunicação UDP foi utilizado no projeto porque é preciso mandar dados do dispositivo para o broker de maneira rápida e periódica sem se importar tanto se o dado chegou inteiro, já que será enviado novamente em seguida.</p>
    <p>Segue uma figura ilustrativa sobre essa troca de mensagens.</p>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-03%20210608.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Comunicação Dispositivo-Broker</figcaption>
            </figure>
        </div>
    <br>
    <h2>Interface do Dispositivo</h2>
    Antes de falar da interface, vale ressaltar que o dispositivo mensionado é um sensor de temperatura que faz médições periódicas de temperatura em graus célsius e manda para o broker caso o dispositivo esteje ligado.
    <p>A figuras as seguir mostram a interface CLI do dispositivo ligado e desligado que permite ao usuário ligar ou desligar o dispositivo.</p>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-03%20232415.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Interface do Dispositivo ligado</figcaption>
            </figure>
        </div>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-03%20230711.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Interface do Dispositivo desligado</figcaption>
            </figure>
        </div>
    <br>
    <h2>Interface do Cliente</h2>
    <p>Como permitido, a interface para a comunicação entre o cliente e o broker foi feita via interface de linha de comando (CLI).</p>
    <p>A principio, ao iniciar o cliente irá aparecer uma tela com um menu com o que pode ser solicitado ao broker, o usuário deve escolher primeiro o comando e depois o número do sensor que ele deseja fazer a solicitação.</p>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-04%20122426.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Menu da Interface</figcaption>
            </figure>
        </div>
    <br>
    <p>A seguir, temos as imagens de quando é solicitado ver todos os dispositivos já conectados, a temperatura de um determinado sensor, a temperatura de um sensor sendo que ele está desligado e quando há uma falha na comunicação entre cliente e broker, respectivamente.</p>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-04%20122617.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Solicitação para ver todos os dispositivos já conectados</figcaption>
            </figure>
        </div>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-04%20122501.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Solicitação de temperatura com o dispositivo ligado</figcaption>
            </figure>
        </div>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-04%20122818.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Solicitação de temperatura com o dispositivo desligado</figcaption>
            </figure>
        </div>
    <br>
        <div align="center">
            <figure>
                <img src="https://github.com/emersonrlp/MI-de-Redes/blob/main/IMG/Captura%20de%20tela%202024-05-04%20122647.png" alt="Descrição da Imagem">
                <br>
                <figcaption>Falha ao se comunicar com o broker</figcaption>
            </figure>
        </div>
    <br>
    <p>Lembrando que qualquer uma das solicitações escolhidas passará os dados em formato de dicionário para a API.</p>
    <h2>Sobre o Desempenho</h2>
    <p>Para melhorar o tempo de resposta foi-se utilizado Threads, Filas e também uma função expecífica do python chamada de timeout().</p>
    <p>Sobre o uso de fila, ela foi de crucial importância sobretudo para guardar os dados da API e para sempre pegar a primeira solicitação da rota <strong>http://localhost:8081/solicitacoes</strong>, já que não exite prioridade entre as solicitações feitas pelos clientes.</p>
    <p>Já sobre o uso de Threads, é mais complicado, visto que são utilizados threads tanto no dispositivo quanto no broker.</p>
    <ul>
        <p>-Dispositivo, nele é utilizado Threads para receber mensagens TCP, enviar dados UDP e esperar por uma entrada do usuário no dispositivo para caso ele deseje desligar ou ligar manualmente o sensor simultaneamente.</p>
        <p>-Broker, é utilizado Threads nele para garantir todo dado que chegar da API e do Dispositivo será encaminhado para seu respectivo destino, não havendo perda de dados.</p>    
    </ul>
    <p>Por fim, o uso da função timeout() foi utilizada somente no cliente, visto que quando o broker desconectava e o cliente tentava fazer uma solicitação havia uma demora para saber se o broker estava desconectado e a função garante que se o broker demorar mais de 1s para responder é porque ele está desconectado.</p>
    <h2>Tratamento de Conexões Simultâneas</h2>
    <p>Embora foi feito o uso de Threads para melhorar o desempenho do código, não foi possível verificar problemas decorrentes ao uso de Threads no sistema com os testes feitos em laboratório, o que não significa que não possa ocorrer futuros problemas quando a adição de um número bem maior de dispositivos ligados. Caso aconteça, seria necessário implementar novas medidas para que ambos os dispositivos sejam capazes de se comunicar de maneira adequada com o broker.</p>
    <h2>Confiabilidade da Solução</h2>
    <p>Durante o desenvolvimento do projeto foi discutido sobre a importância dos dispositivos e clientes conectados ao broker não pararem de funcionar completamente após o fim da sua execução ou quando por algum motivo a conexão internet da máquina que esteje rodando o broker caia, pois se o broker está ou não conectado não deveria afetar a execução nem dos Clientes e nem dos Dispositivos. Para isso, foi-se utilizado uma verificação tanto nos Dispositivos quanto nos clientes para saber se o broker está funcionando, para que caso não esteja os Dispositivos continuem tentando estabelecer a conexão e o Cliente informe que não é possível realizar uma solicitação ao broker.</p>
    <p>Além disso, foi importante fazer um tratamento de erro para as trocas de mensagens entre o Dispositivo-Broker e Cliente-Broker para que mesmo se um deles pare de funcionar, não afete o funcionamento do resto, ou seja, mesmo se um deles parar de funcionar o resto vai continuar rodando  para caso a conexão seja restabelecida</p>
    <h2>Sobre o Projeto</h2>
    <h3>Cliente</h3>
    <p>Segue as funções contidas no <strong>'cliente.py'</strong></p></p>
    <ul>
        <li><strong>obter_lista_de_sensores()</strong>, responsável por consumir a rota da API que guarda dados sobre os dispositivos conectados.</li>
        <li><strong>limpar_terminal()</strong>, responsável por limpar o terminal da interface CLI do cliente.</li>
        <li><strong>menu()</strong>, responsável por mostrar as opções ao usuário e repassar os comandos realizados por ele ao broker.</li>
        <li><strong>main()</strong>, responsável por chamar tudo que vai ser realizado na execução.</li>
    </ul>
    <h3>Dispositivo</h3>
    <p>Segue as funções contidas no <strong>'dispositivo.py'</strong></p>
    <ul>
        <li><strong>gerar_temperatura()</strong>, responsável por gerar temperaturas aleatórias entre 20° e 30°.</li>
        <li><strong>receber_mensagem_tcp()</strong>, responsável por fazer a conexão do dispositivo com o broker para que ele possa receber as mensagens TCP.</li>
        <li><strong>enviar_mensagem_udp()</strong>, responsável por enviar os dados ao broker em UDP.</li>
        <li><strong>entrada()</strong>, responsável por esperar por uma solicitação do usuário via CLI no dispositivo.</li>
        <li><strong>limpar_terminal()</strong>, responsável por limpar a interface CLI do dispositivo.</li>
        <li><strong>main()</strong>, responsável por criar threads para que o dispositivo consiga receber mensagens TCP, enviar mensagens UDP e esperar uma solicitação do usuário via CLI constantemente.</li>
    </ul>
    <h3>Broker</h3>
    <p>Diferente dos demais, o <strong>'broker.py'</strong> guarda a parte referente ao Servidor para lidar com a comunicação com os dispositivos e a parte da API para poder pegar requisições dos clientes e subir dados para que o cliente possa acessá-los</p>
    <ul>
    <h3>Servidor</h3>
            <p>Segue as funções referentes a parte do servidor no <strong>'broker.py'</strong></p>
            <ul>
                <li><strong>broker()</strong>, responsável por iniciar o servidor TCP e aceitar conexões dos dispositivos.</li>
                <li><strong>receber_udp()</strong>, responsável por receber os dados dos dispositivos.</li>
                <li><strong>atualizar_dados()</strong>, responsável por manter os dados atualizados no dicionário da API</li>
                <li><strong>data_atual()</strong>, responsável por pegar a data atual para passar ao dado atual</li>
                <li><strong>tratamento_mensagens()</strong>, responsável por verificar se tem alguma solicitação pendente de um cliente para um dispositivo para repassá-lo ao dispositivo.</li>
                <li><strong>remover_solicitação()</strong>, responsável por remover uma solicitação no dicionário da API.</li>
                <li><strong>obter_lista_solicitações()</strong>, responsável por pegar a lista de dicionários da API.</li>
                <li><strong>enviar_tcp()</strong>, responsável por enviar a mensagem tcp ao dispositivo escolhido.</li>
                <li><strong>delete_cliente()</strong>, responsável por deletar um cliente da lista de clientes.</li>
            </ul>
    <h3>API</h3>
        <p>Segue as funções referentes a parte da API no <strong>'api.py'</strong></p>
        <ul>
            <li><strong>get_sensores()</strong>, responsável por retornar os dados e todos os sensores registrados na sua aplicação.</li>
            <li><strong>get_sensor()</strong>, responsável por retornar os dados de um sensor expecífico registrado na aplicação.</li>
            <li><strong>criar_sensor()</strong>, responsável por criar e registrar um sensor na aplicação.</li>
            <li><strong>atualizar_sensor()</strong>, responsável por atualizar dados de um sensor na aplicação.</li>
            <li><strong>excluir_sensor()</strong>, responsável por remover um sensor da aplicação.</li>
            <li><strong>get_solicitacoes()</strong>, responsável por retornar os dados e todas as solicitações registradas na sua aplicação.</li>
            <li><strong>get_solicitacao()</strong>, responsável por retornar os dados de uma solicitação expecífica registrada na aplicação.</li>
            <li><strong>criar_solicitacao()</strong>, responsável por criar e registrar uma solicitação na aplicação.</li>
            <li><strong>atualizar_solicitacao()</strong>, responsável por atualizar dados de uma solicitação na aplicação.</li>
            <li><strong>excluir_solicitacao()</strong>, responsável por remover uma solicitação da aplicação.</li>
        </ul>
    </ul>
    <h2>Conclusão</h2>
    <p>Enfim, conclui-se que o projeto entregue abrange todos os requisitos solicitados no problema, abordando o uso de threads, criação de um broker para troca de mensagens, criação de uma dispositivo/atuador, uso de uma API RESTful , uso de docker para facilitar a execução do sistema por terceiros, o uso do software Insomnia para testes nas rotas e por fim o uso dos protocolos TCP e UDP para troca de mensagens.</p>
    <p>Ademais, vale mencionar possíveis alterações para uma melhor usabilidade da interface do cliente como o uso de React para o front-end, adição de outros tipos de dispositivos ou até mesmo fazer uso de dispositivos reais.</p>
  <h2>Como Executar o Projeto</h2> 
    <p>Siga os seguintes passos para a execução do projeto:</p>
    <ul>
      <li>baixe o repositório: 
          <a href="https://github.com/emersonrlp/MI-de-Redes.git">https://github.com/emersonrlp/MI-de-Redes.git</a>
      </li>
      <li>execute o seguinte comando com o terminal nas pastas Cliente, Dispositivo e Broker: <strong>'docker build -t nome_do_arquivo .'</strong></li>
      <li>digite <strong>'docker images'</strong> para ver se as imagens docker foram criadas com sucesso.</li>
      <li>por fim, execute o programa usando o comando <strong>'docker run --network='host' -it -e IP_ADDRESS=ip_do_broker nome_da_imagem'</strong> para executar as imagens do dispositivo e do cliente criadas e <strong>'docker run --network='host' -it nome_da_imagem'</strong> para executar a imagem do broker.</li>
   </ul>
  <p>tendo feito isso, é possível fazer solicitações por meio do cliente via CLI pedindo para que forneça a temperatura, desligue ou ligue um determinado dispositivo.</p>    
    <p><strong>Obs.:</strong> é necessário ter o docker instalado na máquina que deseja executar o código.</p>
</body>
</html>
