# Notas estudos KlipperScreen
Para iniciar clone o repositório do KlipperScreen

Logo após será necessário fazer o donlowd das dependências:
```bash
sudo apt-get install libgtk-3-dev python3-gi gir1.2-gtk-3.0 = erro de não reconhecer o Gtk
sudo apt install python3-websocket 

apt install python3.12-venv
sudo apt install python3-gi

pip install vext
pip install vext.gi

sudo apt install pkg-config libcairo2-dev gcc python3-dev libgirepository1.0-dev

pip install PyGObject
``` 
## Mudar tamanho da tela do KlipperScreen
Vá até /config/defaults.conf, em '[main]' adicione o seguinte comando:
```python
[main]
width = 500 #A largura desejada
height = 300 #Altura desejada
```
## Ter uma tela secundária ou principal diretamente no PC
Vá até /config/defaults.conf, adicione o seguinte comando:
```python
[printer MyPrinter]
moonraker_host: 172.16.0.74 #ip da sua impressora
moonraker_port: 7125 #porta
```
### Entendendo o basico da estrutura do KlipperScreen
```
\config
	\defaults.conf # configuraçõpes principais
	\main_menu.conf # da para adicionar novos tipos de paineis no menu principal
\docs #documentação
\ks_includes 
\panels # localização dos paineis 
\scripts
\styles
screen.py # principal, para gerar a tela geral
```
# NOTA SOBRE O GIF

A função que vai executar uma ação, chama a função _send_action. Assim que chamada ela usa a função 'isinstance' para checar se widget é um botão e se for vai chamar o Button_busy e o send_method (que verefica a conecção com o web socket e caso haver uma conecção ele vai enviar informações/comandos em formato json), além de chamar o enable_widget (sendo ele um call-back, assim que o send_method enviar uma resposta a ação, ele é executado e o spinner para), que esta responsavel por um condição de parada, onde
o spinner esta sendo chamado repetidamente até a função retornar falso ou g_source_remove.

enable_widget, ESTÁ LOCALIZADO NO SCREEN