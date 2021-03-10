## Slack-Bot

##### Bot feito em python para automatizar o check-in feito no slack da Kenzie Academy Brazil
##### Check-in automático tanto para as 09:00 como para as 14:00
##### No caso do dev ser coach, o check-in é feito de forma automatica tanto no início do horário de coach quanto no check-in normal da turma

## ## Instalação

##### 1. ```pip install selenium```
##### 2. Baixar o [Geckodriver](https://github.com/mozilla/geckodriver/releases) e colocar o que extraiu na pasta usr/bin
##### 3. Configurar o core/main.py de acordo com suas preferências:
#####  Alterar o COACH_Q2 com o link da página do check-in de coach, caso seja coach
#####  Alterar o ALUNO_Q3 com o link da página do check-in de dev
#####  Alterar o FIREFOX_PROFILE com o local de onde seu perfil do firefox esta (o firefox deve estar logado no slack)
#####  No Firefox digite about:profiles para verificar o local do perfil

#### Only for Linux
