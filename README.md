# Projeto ABAPRJ - Desenvolvimento em Django

Nosso projeto para a ONG Projeto **ABAPRJ** foi desenvolvido utilizando o framework 
**Django**, com duas equipes front-end e back-end.


# Front-End

**Wikten:**

- **Tarefas:** Criação e estilização da página inicial de administração e da página home, 
estilização da tabela em listagens e da listagem de voluntários, além da criação do rodapé
e cabeçalho.

- **Detalhes Técnicos:** Utilização de HTML, CSS e JavaScript para construir uma interface 
amigável e responsiva. Implementação de CSS para estilizar consistente e adaptável em cada 
etapa do designer detalhado previamente com uso de Ferramenta de design colaborativa e 
online como Figma.

**Laíze:**

- **Tarefas:** Criação e estilização da página de ações sociais e da página de resultados de 
buscas, estilização dos botões de todas as páginas, além de alterações no rodapé e cabeçalho.

- **Detalhes Técnicos:** Utilização de HTML, CSS e JavaScript para construir uma página 
amigável e responsiva. Implementação de CSS para estilizar consistente e adaptável em cada 
etapa do designer detalhado. 

**João:**

- **Tarefas:** Criação e estilização das páginas de login e candidatura, documentação, documentação final, edição
de vídeo do final.

- **Detalhes Técnicos:** Utilização de HTML, CSS para construir uma interface amigável

# Back-End

**Página View**

**Pedro:** Em "cadastrosAdmin," Pedro criou as seguintes class-based views:

```
● Gerenrecia
● CadAdmin
● AdminCadCreate
● AdminUpdateView
● FuncUpdareView
● AdminCadUpdate
● AdminlistView
● CadastroEspelhoLista
● CadDeleteView
● FuncDeleteView
● AdminDeleteView
```
Em "cadastros",Pedro concluiu:

```
● CadCreateView
● CadUpdateView
● CadListView
● CadCompleteView
● ValidarFuncionário
```
**Stefany:** Em "cadastrosAdmin,"Stefany criou as seguintes class-based views:

```
● AdminHome
● FuncListView
● DadosCadastroCriancas
● DadosCasdastroVoluntarios
● DadosCadastrosAdmin
● ProcurarCriança
● ProcurarVoluntario
● ProcurarAdmin
```
Em "cadastros,"Stefany concluiu:

```
● Chamalogin
● ChamaHome
● ChamaApoie
● CadVoluntario
● DadosCadastros
● Procurar
```
**Trabalho  Conjunto:** Juntos, concluímos:

```
● Esqueci_senha
● GerarPayload
```
# Página Model

**Pedro:** Pedro criou as seguintes tabelas:

```
● Admin
● Login
```
**Stefany:** Stefany criou:

```
● Cadastro Voluntario
```
**Trabalho Conjunto:** Juntos,concluímos:


```
● EsqueciSenha
● MembroFamilia
● Cadastro
```
# Páginas HTML

**Pedro:** Pedro desenvolveu todas as partes relacionadas às tabelas, incluindo as
funções de editar, excluir e concluir nos seguintes HTMLs do aplicativo 
"cadastrosAdmin":


```
● AdminEspelho_confirm_delete.html
● AdminEspelho_list.html
● CadastroEspelho_confirm_delete.html
● CadastroEspelho_list.html
● CadastroVoluntarioEspelho_confirm_delete.html
● CadastroVoluntarioEspelho_list.html
```
No aplicativo "cadastros", ele trabalhou em:

```
● Cadastro_list.html
● Cadastro_form.html
● base.html
```
Além disso, Pedro criou alguns formulários, como:

```
● AdminEspelho_form.html
● CadastroEspelho_form.html
● Cadastro_form.html(noaplicativo"cadastros")
```
**Stefany:** Stefany desenvolveu todas as páginas relacionadas à pesquisa e filtros,
 incluindo:

No aplicativo "cadastrosAdmin":

```
● Dados_cadastroAdmin.html
● ProcurarAdmin.html
● Resultados_procurarAdmin.html
● Dados_cadastroCrianca.html
● ProcurarCrianca.html
● Resultados_procurarCrianca.html
● Dados_cadastroVoluntario.html
● ProcurarVoluntarios.html
● Resultados_procurarVoluntario.html
```
No aplicativo "cadastros":

```
● Dados_cadastro.html
● Procurar.html
● Resultados_procurar.html
```
Ela também criou EsqueciSenha_form.html no aplicativo "cadastros".


**Detalhes Específicos:**

```
● A paginação de conteúdo foi feita por Stefany.
● Ela também criou listas com os nomes dos voluntários e admins, presentes
em apoie.html, Index.html, e admin.html.
```
**Trabalho Conjunto:** Pedro e Stefany desenvolveram a lógica do payload e pix, 
adicionando-os no index.html, além de integrarem imagens estáticas e CSS no Django.

# Outros Contribuintes:

**João:**  Desenvolveu login.html e CadastroVoluntario_form.html, com adição do
formulário crispy feita por Pedro Cezar.

**Front-End Team:** Responsável por todo o CSS. João especificamente cuidou do CSS 
das páginas de login e cadastro de voluntário. Wikten fez a responsividade de algumas
paginas para telas de celular e tablets, e Laize fez a da pagina apoie.html.

# Página URLs

**Pedro:**  Pedro adicionou máscaras hash em cada URL.

# Lógica do Sistema

A lógica de cadastro e edição é gerenciada através das "Generic Views" do Django, 
facilitando operações de CRUD (Create, Read, Update, Delete). Essas class-based views 
são utilizadas para tarefas como cadastro de novos itens, leitura de itens cadastrados, 
atualização e deleção de itens.

# Tecnologias Utilizadas

```
● Django: Framework principal utilizado para desenvolvimento backend, gerenciamento 
de lógica de negócios e manipulação de dados.
● HTML/CSS/JavaScript:Tecnologias básicas para desenvolvimento front-end, garantindo 
interfaces interativas e responsivas.
● APIsExternas: Integração para processamento de pagamentos e envio de e-mails.
● BibliotecasDjango: Importação de bibliotecas adicionais para facilitar a navegação e 
manipulação de dados.
```
# Implementação

```
● ViewsPersonalizadas: Criação de funções personalizadas nas views para coleta e alteração
de campos via métodos HTTP (GET, POST).
● Deploy: Preparação de campos necessários para deploy, com pendência apenas da hospedagem 
do banco de dados para finalização.
● Organização do Código:  Uso de requisitos e indentação adequada com explicações detalhadas 
para melhor compreensão do código.
● UtilizaçãodeFunçõesNativasdoDjango: Para maior organização, como nomenclatura form, list, 
template, entre outros específicos, evitando a criação de novos campos para manipulação.
```
# Histórico de Commits

Todas essas informações podem ser comprovadas pelo histórico de commits, que contém todos os 
commits feitos até aqui e as respectivas pessoas que os fizeram.

Cada integrante detalhou suas contribuições e as colocou nesta documentação.

**Documento convertido para Markdown por João Pedro Guimarães Fernandes**

