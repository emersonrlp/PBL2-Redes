<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body> 
  <h1>Transações Bancárias Distribuídas</h1>
    <p>
Devido aos avanços dos bancos brasileiros nos atendimentos móveis, que visam facilitar a maneira com que os usuários realizam transações e operações no dia a dia, como checar saldo, extrato, limite de crédito, entre outros, houve um aumento substancial na adesão de seus clientes a essas plataformas. Além disso, outro fator culminante que influenciou esse desenvolvimento foi o surgimento da ferramenta Pix, cujo principal objetivo é garantir a rapidez dos pagamentos 24 horas por dia.</p>
    <p></p>
    <p>Mediante a isso, um país onde não existe um sistema bancário centralizado decidiu implementar a ferramenta Pix. No entanto, existem algumas diferenças na sua implementação devido ao seu sistema distinto. Para isso, é necessário utilizar uma abordagem que garanta a não concorrência nas operações entre os bancos e assegure a atomicidade das transações, evitando problemas como duplicação de dinheiro, perca de dinheiro, etc.</p>
    <h2>Arquiterura do Projeto</h2>
    <p>Antes de explicar como é a arquitetura do projeto em si, vamos dar uma olhada e entender o que é um sistema que possui um Banco Central.</p>
    <br>
    <div align="center">
                <figure>
                    <img src="IMG/Captura de tela 2024-07-01 121301.png" alt="Descrição da Imagem">
                    <br>
                    <figcaption>Arquitetura do Banco Central</figcaption>
                </figure>
            </div>
    <br>
    <p>Como mostra a imagem, o banco central é responsável por encaminhar todas as operações feitas entre os bancos e garantir a confiabilidade dessas operações, evitando gastos indevidos de dinheiro. Isso é possível porque todas as operações passam pelo banco central antes de serem concluídas. Caso haja conflito entre as transações, não haverá problema, pois existe uma ordem definida para cada uma.</p>
    <p>Tendo mostrado um pouco de como funciona um sistema com o Banco Central, vamos ver como é a Arquitetura do sistema sem a presença de um Banco Central.</p>
    <br>
    <div align="center">
        <figure>
            <img src="IMG/Captura de tela 2024-07-01 125117.png" alt="Descrição da Imagem">
            <br>
            <figcaption>Arquitetura do Projeto</figcaption>
        </figure>
    </div>
    <br>
    <p>No sistema mencionado, diferente do que tínhamos com o Banco Central, não há um ente responsável por receber todas as transações ou garantir sua confiabilidade. Em vez disso, cada banco segue uma regra pré-definida para evitar possíveis erros. Nesse caso, foi utilizada uma topologia de rede de computadores chamada Token Ring para garantir que somente um banco por vez possa efetuar uma transação, pois apenas um banco por vez terá acesso ao token, que é a entidade que permite a realização de uma transferência.</p>
    <p>Segue um fluxo da execução do sistema:</p>
    <ol>
        <li>Todos os bancos são inicializados, inclusive o escolhido para iniciar com o token.</li>
        <li>Qualquer cliente pode inserir uma transação a ser feita no seu banco.</li>
        <li>Caso exista alguma operação a ser feita pelo banco detentor do token, apenas uma é feita e o token é passado para o proximo da lista.</li>
        <li>Caso não exista nenhuma operação a ser feita pelo banco detentor do token, o token é passado para o proximo da lista.</li>
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
    <h2>Conclusão</h2>
    <p>Enfim, conclui-se que o projeto entregue abrange todos os requisitos solicitados no problema, abordando o uso de threads, criação de um broker para troca de mensagens, criação de uma dispositivo/atuador, uso de uma API RESTful , uso de docker para facilitar a execução do sistema por terceiros, o uso do software Insomnia para testes nas rotas e por fim o uso dos protocolos TCP e UDP para troca de mensagens.</p>
    <p>Ademais, vale mencionar possíveis alterações para uma melhor usabilidade da interface do cliente como o uso de React para o front-end, adição de outros tipos de dispositivos ou até mesmo fazer uso de dispositivos reais.</p>
  <h2>Como Executar o Projeto</h2> 
    <p>Siga os seguintes passos para a execução do projeto:</p>
    <ul>
      <li>baixe o repositório: 
          <a href="https://github.com/emersonrlp/PBL2-Redes">https://github.com/emersonrlp/PBL2-Redes.git</a>
      </li>
      <li>execute o seguinte comando com o terminal nas pastas Cliente e Banco: <strong>'docker build -t nome_do_arquivo .'</strong></li>
      <li>digite <strong>'docker images'</strong> para ver se as imagens docker foram criadas com sucesso.</li>
      <li>por fim, execute o programa usando o comando <strong>'docker run --network='host' -it -e IP_ADDRESS=ip_do_banco nome_da_imagem'</strong> para executar as imagens dos bancos e dos clientes.</li>
   </ul>
  <p>tendo feito isso, é possível criar contas, consultar saldo, realizar depositos, saques, transferências de todas as contas finculadas a um cliente expecífico.</p>    
    <p><strong>Obs.:</strong> é necessário ter o docker instalado na máquina que deseja executar o código.</p>
</body>
</html>
