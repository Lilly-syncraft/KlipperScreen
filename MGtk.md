# PyGObject

PyGObject é um pacote python que contém a vinculação com bibliotecas GObjects, como o Gtk, Glib, Gdk, Pango, entre outras.
Com o Gtk, é possivél criar telas interativas, sendo sua estrutura é organizada em linhas e colunas.

O GTK+ usa um modelo de programação orientada a eventos. Quando o usuário não está fazendo nada, ele fica no loop principal e aguarda a entrada. Se o usuário executar alguma ação – digamos, um clique do mouse — o loop principal “acorda” e entrega um evento para o GTK+.

Quando widgets recebem um evento, eles frequentemente emitem um ou mais sinais. Sinais notificam seu programa que “algo interessante aconteceu” invocando funções que você conectou ao sinal. Depois que um retorno de chamada terminar, o GTK+ retornará ao loop principal e aguardará a entrada do usuário.
### Exemplo:
Esse sinal pode ser visualizado por exemplo em um botão:
```python
btn = Gtk.Button()
btn.connect("clicked", self.load_menu)
```
Onde o sinal é o 'clicked' e a função o self.load_menu.

## Gif animado e KlipperScreen
### Criando um gif para que quando o botão de load for precionado ele possa aparecer enquanto a impressora faz a sua rotina.
O código abaixo representa a criação do grid, onde o gif ficará localizado, e a definição de um gif: 
```python 
#--------------------------demais códigos--------------------------------------------------------------------
        self.content.add(self.labels['extrude_menu'])

        # Criar grid do gif
        self.gif_box = Gtk.Grid(orientation=Gtk.Orientation.HORIZONTAL, vexpand=True)

        # Criar o gif
        path_name = Path(__file__).parent / ".." / "t" / "try.gif"
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
        self.gif_box.attach(self.loading_gif, 1, 0, 1, 1)
        # Adiciona o layout principal ao conteúdo
        self.content.add(self.gif_box)
        # Adiciona o layout principal ao painel
        self.gif_box.show_all() 
        #esconde o GIF
        self.loading_gif.hide()

    def enable_buttons(self, enable):
#--------------------------demais códigos--------------------------------------------------------------------
```
### Após cria o gif e definir seu lugar, vamos criar algumas funções para que ele apareça apenas quando for chamado.
```python
#--------------------------demais códigos--------------------------------------------------------------------
    def _operation_gif(self):
        # Pega o status da temperatura
        temp = self._printer.get_stat(self.current_extruder, 'temperature')
        target = self._printer.get_stat(self.current_extruder, 'target')
        
    # Só vai mostrar o gif se a temperatura estiver abaixo do mínimo
        if temp < target or target > 0:
            self._start_loading_gif()
        else:
            self._stop_loading_gif()

    # Chamado o Gif
    def _start_loading_gif(self):
        # Mostra o GIF animado
        def show_gif():
            print("Exibindo GIF animado...")
            # Esconde os botões  
            GLib.idle_add(self.labels['extrude_menu'].hide)
            self.loading_gif.show()
            # Redesenha o layout, como se fosse um refresh
            self.loading_gif.queue_draw()
            self.gif_box.queue_draw()
            return False
        # Adiciona a função de mostrar o GIF à fila de eventos
        GLib.idle_add(show_gif)

    # Para o GIF
    def _stop_loading_gif(self):
        def hide_gif():
            print("Escondendo GIF animado...") 
            # Mostra os botões novamente
            self.labels['extrude_menu'].show()
            self.loading_gif.hide()
            return False
        GLib.idle_add(hide_gif)

```
OBS:. Ele foi chamado na função load_unload.