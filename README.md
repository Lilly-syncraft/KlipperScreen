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

A função que vai executar uma ação, chama a função _send_action. Assim que chamada ela usa a função 'isinstance' para checar se widget é um botão e se for vai executar o Button_busy (chama o spinner) e o send_method (que vai vereficar a conexão com o web socket e caso haver uma conexão ele vai enviar informações/comandos em formato json), além de chamar o enable_widget (sendo ele um call-back, assim que o send_method enviar uma resposta a ação, ele é executado e o spinner), que esta responsável por um condição de parada, onde
o spinner esta sendo chamado repetidamente até a função retornar falso ou g_source_remove.
```python
    def _send_action(self, widget, method, params):
        logging.info(f"{method}: {params}")
        if isinstance(widget, Gtk.Button):
            self.gtk.Button_busy(widget, True)
            self._ws.send_method(method, params, self.enable_widget, widget)
        else:
            self._ws.send_method(method, params)
```
enable_widget, ESTÁ LOCALIZADO NO SCREEN
### Gif rodando
Par modificar o gif para que cada botão que chame o spinner mostre o gif, adicione o seginte parâmetro:
```python
gif = "nome_do_gif"
```
Exemplo no botão load:

```python
'load': self._gtk.Button("arrow-down", _("Load"), "color3", gif = "try")
```
OS GIFS DEVEM ESTAR NA PASTA styles/t, CASO QUEIRA REDIRECIONAR MUDE A SEGUINTE LINHA (está localizada no painel "klippyGtk.py" -> na função def Button_busy)
```python
gif_path = Path(__file__).parent / ".." / "t" / f"{gif_name}.gif"
```
### Obs:.
DETALHE IMPORTANTE!!!
CASO NÃO HAVER NENHUM GIF DEFINIDO PARA UM BOTÃO QUE CONTENHA A FUNÇÃO 'BUSY', ELE NÃO VAI EXECUTAR A AÇÃO QUE DEVERIA. 