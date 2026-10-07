\-Pré-requisitos técnicos:



Linguagem de programação: utilize Java na versão 17 ou 21.

Banco de dados: utilize Oracle.

Obrigatório o uso da instância Oracle da FIAP durante o desenvolvimento e entrega da atividade.

Modelagem do banco de dados: baseie-se na modelagem previamente criada.

Manipulação de tipos de dados no Java: familiarize-se com a manipulação de dados em Java.



\-Atividade:



fazer a classe DAO acessar o banco de dados, de fato. Crie um método getAll(), que deve acessar o banco de dados, realize um SELECT e receba a consulta, armazenando-a em uma coleção de dados como vimos no capítulo 2.



Crie, também, um método insert() na classe do tipo DAO que realize um INSERT e registre uma nova informação. Como você precisa testar o getAll() solicitado acima, utilize o comando insert() para cadastrar pelo menos cinco novos registros. Use a própria classe Teste, método main(), para inserir os registros e chamar a consulta.



Como os vários passos do acesso ao banco de dados podem ter problemas, tais como o banco estar fora do ar, a tabela ter sido apagada, entre outros, é indispensável realizar o tratamento de exceções. Utilize try-catch para tratar as possíveis exceções.

-Requisitos do sistema:



Classe DAO: criar a classe DAO responsável por acessar o banco de dados Oracle para a continuação do sistema FINTECH.

Consulta de dados: implementar o método getAll na classe DAO. Esse método deverá recuperar todos os dados no banco através de um comando SELECT e retornar uma lista de objetos (resultados do SELECT).

Tratamento de exceções: implementar tratamento de exceções para lidar com possíveis problemas durante o acesso ao banco de dados, como indisponibilidade do banco ou tabela inexistente.

Cadastrar dados: adicionar o método insert na classe DAO que permita registrar informações no banco de dados.

-Instruções para testes:



Criar uma classe para testes, com método para iniciar os testes.

Teste de cadastro: utilizar o método insert para cadastrar pelo menos 5 (cinco) novos registros no banco de dados.

Teste de consulta: testar o método getAll após a inserção dos registros, garantindo que ele recupere e apresente corretamente as informações recuperadas.


\-Adaptação para outras entidades: replique o desenvolvimento realizado para outras entidades da sua modelagem, implementando no mínimo 3 (três) entidades. 



As entidades escolhidas devem fazer parte da modelagem desenvolvida pelo grupo e representar conceitos relacionados ao sistema FINTECH, como, por exemplo, Conta, Receita, Despesa, Investimento ou outros conceitos equivalentes presentes no projeto.



Os nomes e a estrutura das entidades podem variar de acordo com a solução desenvolvida pelo grupo.



&#x20;

\-Após concluir a integração de uma entidade com o banco de dados, aplique o mesmo processo às demais entidades escolhidas para a atividade, garantindo a implementação de pelo menos 3 (três) entidades

