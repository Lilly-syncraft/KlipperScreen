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
# Código de exemplo para criar um painel com gif
```python
import gi
import time
import threading
from pathlib import Path

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, GdkPixbuf
from ks_includes.screen_panel import ScreenPanel

class Panel(ScreenPanel):
    def __init__(self, screen, title):
        title = title or _("Update")
        screen = screen or "update"
        super().__init__(screen, title)

        # Botão
        self.labels["restart_btn"] = self._gtk.Button(
            "refresh", _("System Restart"), "color1"
        )
        self.labels["restart_btn"].connect("clicked", self.on_button_clicked)

        # Layout principal, vai manter o botão e o GIF
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, vexpand=True)
        self.main_box.pack_start(self.labels["restart_btn"], False, False, 0)

        # === GIF ANIMADO ===
        path_name = Path(__file__).parent / ".." / "styles" / "pato.gif"
        if path_name.exists():
            try:
                # Carregar o GIF animado
                animation = GdkPixbuf.PixbufAnimation.new_from_file(str(path_name))
                self.loading_gif = Gtk.Image.new_from_animation(animation)
                
            except Exception as e:
                print("Erro ao carregar GIF:", e)
                self.loading_gif = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.DIALOG)
        else:
            print("GIF não encontrado:", path_name)
            self.loading_gif = Gtk.Image.new_from_icon_name("image-missing", Gtk.IconSize.DIALOG)

        #não mostrar o GIF até que seja necessário
        self.loading_gif.set_no_show_all(True)
        #alinhar o GIF no centro
        self.loading_gif.set_halign(Gtk.Align.CENTER)
        self.loading_gif.set_valign(Gtk.Align.CENTER)

        # Adiciona o GIF ao layout principal
        self.main_box.pack_start(self.loading_gif, True, True, 0)
        # Adiciona o layout principal ao conteúdo
        self.content.add(self.main_box)
        # Adiciona o layout principal ao painel
        self.main_box.show_all() 
        #esconde o GIF
        self.loading_gif.hide()

    # Método chamado quando o botão é pressionado
    def on_button_clicked(self, widget):
        print("Botão pressionado: iniciando operação...")
        # Esconde o botão
        GLib.idle_add(self.labels["restart_btn"].hide)
        # Mostra o GIF
        self._start_loading_gif()
        # Inicia a tarefa longa em uma thread separada
        threading.Thread(target=self._simulate_long_task).start()

    # Chamado o Gif
    def _start_loading_gif(self):
        # Mostra o GIF animado
        def show_gif():
            print("Exibindo GIF animado...")  
            self.loading_gif.show()
            # Redesenha o layout, como se fosse um refresh
            self.loading_gif.queue_draw()
            self.main_box.queue_draw()
            return False
        # Adiciona a função de mostrar o GIF à fila de eventos
        GLib.idle_add(show_gif)

    # Para o GIF
    def _stop_loading_gif(self):
        def hide_gif():
            print("Escondendo GIF animado...") 
            self.loading_gif.hide()
            # Mostra o botão novamente
            self.labels["restart_btn"].show()
            return False
        GLib.idle_add(hide_gif)

    # Simula uma tarefa longa
    def _simulate_long_task(self):
        time.sleep(3)
        print("Tarefa concluída!")
        # Para o GIF
        self._stop_loading_gif()
```