from pathlib import Path
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="hiiiii")

        self.set_border_width(10)
        self.box = Gtk.Box(spacing=6, orientation=Gtk.Orientation.VERTICAL)
        self.add(self.box)

        # Botão
        button = Gtk.Button(label="Abrir diálogo")
        button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(button, True, True, 0)

    def on_button_clicked(self, widget):
        dialog = PopUp(self)
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("Você clicou em OK")
        elif response == Gtk.ResponseType.CANCEL:
            print("Você clicou em Cancelar")

        dialog.destroy()

class PopUp(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Diálogo", transient_for=parent, flags=Gtk.DialogFlags.MODAL)
        self.set_default_size(300, 200)
        self.set_border_width(20)

        # Adiciona botões
        self.add_buttons(
            "Cancelar", Gtk.ResponseType.CANCEL,
            "OK", Gtk.ResponseType.OK
        )

        # Corpo do diálogo
        content_area = self.get_content_area()
        label = Gtk.Label(label="Este é um diálogo simples.")
        content_area.add(label)

        # Caminho da imagem
        path_name = Path(__file__).parent / "t" / "try.gif"
        self.im = Gtk.Image()
        self.im.set_from_file(str(path_name))
        content_area.add(self.im)

        self.show_all()

# Inicialização da janela
if __name__ == "__main__":
    window = MainWindow()
    window.set_size_request(300, 200)
    window.connect('destroy', Gtk.main_quit)
    window.show_all()
    Gtk.main()


