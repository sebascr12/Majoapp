import tkinter as tk
from tkinter import Label, Button, messagebox
import cv2
import PIL.Image, PIL.ImageTk
import random
import pygame  # Para reproducir la canción en la vista final
from ffpyplayer.player import MediaPlayer

class VideoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MajoApp")
        self.root.geometry("850x650")
        self.root.configure(bg="#F5E6E8")  # Fondo en tonos pastel
        self.root.resizable(False, False)
        self.centrar_ventana()

        # Inicializar pygame para la música
        pygame.mixer.init()

        # Videos y Cartas
        self.videos = ["video1.mp4", "video2.mp4", "video3.mp4"]
        self.cartas = [
            "Yo sé que peco por impaciente y muy intenso,"  
            "\n Hace poco descubrí que la paciencia y la intensidad van de la mano (al menos conmigo)"
            "\n Te explico..."
            "\n Yo soy paciente porque sé que te esperaría por toda una vida,"
            "\n pero te amo con tanta intensidad que necesito demostrarte que realmente soy lo que alguna vez dejé de ser, haciéndote estas cosas.",

            "Ese video significa todo lo que llega a mi mente cuando me preguntan"
            "\n '¿Por qué Majo?'"
            "\n Sin querer, en este montón de rato que llevamos juntos he descubierto que no estoy solo en esta vida"
            "\n Me di cuenta que existe alguien capaz de sostenerme y apoyarme, incluso cuando no soy capaz de dar lo mejor de mí."
            "\n"
            "\n Te admiro tanto y me siento tan orgulloso de quien sos."
            "\n Que toda mi vida, si es mi elección, esa va a ser tenerte a mi lado."
            "\n No solo físicamente, sino mental y espiritualmente."
            "\n Yo sé que puedo ser feliz y extraordinario solo, pero con vos tengo paz y además tengo con quién compartir esos momentos"
            "\n en los que soy extraordinario, para que lo que tenemos forme algo excepcional.",

            "Flaca, yo no voy a parar de decirlo, usted se merece el mundo entero."
            "\n He mejorado muchísimo y con la decisión por el resto de mi vida con vos."
            "\n Solo por tenerte aquí, yo decido mejorar. Por la mejor mujer"
            "\n que hay en esta vida."
        ]
        self.video_index = 0
        self.playing_video = False
        self.video_paused = False

        # Estilos
        self.fuente = ("Georgia", 14, "italic")

        # Reproductor de Video
        self.video_label = Label(self.root, bg="#F5E6E8")
        self.video_label.pack()

        # Botón Play
        self.btn_play_video = Button(self.root, text="Play", command=self.reproducir_video, 
                                     font=self.fuente, fg="white", bg="#4CAF50", relief="flat", padx=12, pady=5, width=10)
        self.btn_play_video.pack(pady=10)

        # Botón Pausa
        self.btn_pause = Button(self.root, text="Pausa", command=self.toggle_pausa, 
                                font=self.fuente, fg="white", bg="#6D6875", relief="flat", padx=12, pady=5, width=10)

        # Botón "Click después del video"
        self.btn_click_carta = Button(self.root, text="Dale click", command=self.mostrar_carta, 
                                      font=self.fuente, fg="#4A4A4A", bg="#D8A7B1", relief="flat", padx=12, pady=5, width=20)

        # Botón "Next" para avanzar al siguiente video desde la carta
        self.btn_next_video = Button(self.root, text="Next", command=self.siguiente_video, 
                                     font=self.fuente, fg="white", bg="#B5838D", relief="flat", padx=12, pady=5, width=10)

        # Botón "Sí"
        self.btn_si = Button(self.root, text="SI", command=lambda: messagebox.showinfo("Mensaje", 
            "Favor confirmar disponibilidad por un sticker al 7293-0105 para recibir itinerario."
            "\n Pero en serio, si la respuesta es no por X o Y también avisarme por favor."
            "\n\n Me tosté la jupa haciendo esto, espero que te guste mucho."),
            font=self.fuente, fg="#4A4A4A", bg="#A2836E", relief="flat", padx=12, pady=5, width=10)

        # Botón "No"
        self.btn_no = Button(self.root, text="NO", command=self.mover_boton_no,
                             font=self.fuente, fg="white", bg="#E74C3C", relief="flat", padx=12, pady=5, width=10)

        # Carta
        self.carta_label = Label(self.root, text="", font=self.fuente, wraplength=500, justify="center",
                                 bg="#F3D8D5", fg="#4A4A4A", padx=20, pady=20, borderwidth=2, relief="solid")

    def centrar_ventana(self):
        self.root.update_idletasks()
        ancho = self.root.winfo_width()
        alto = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.root.winfo_screenheight() // 2) - (alto // 2)
        self.root.geometry(f"+{x}+{y}")

    def reproducir_video(self):
        if self.video_index < len(self.videos):
            video_path = self.videos[self.video_index]
            self.cap = cv2.VideoCapture(video_path)
            self.player = MediaPlayer(video_path)
            self.playing_video = True
            self.video_paused = False
            self.actualizar_frame()

            self.btn_play_video.pack_forget()
            self.btn_pause.pack(pady=10)
        else:
            self.mostrar_vista_final()

    def actualizar_frame(self):
        if self.cap.isOpened() and not self.video_paused:
            ret, frame = self.cap.read()
            audio_frame, val = self.player.get_frame()

            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (800, 450))
                img = PIL.Image.fromarray(frame)
                imgtk = PIL.ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                self.root.after(30, self.actualizar_frame)

            if val == 'eof':  
                self.cap.release()
                self.player.close_player()
                self.playing_video = False
                self.btn_pause.pack_forget()
                self.btn_click_carta.pack(pady=20)

    def toggle_pausa(self):
        if self.playing_video:
            if self.video_paused:
                self.video_paused = False
                self.player.set_pause(0)
                self.btn_pause.config(text="Pausa")
                self.actualizar_frame()
            else:
                self.video_paused = True
                self.player.set_pause(1)
                self.btn_pause.config(text="Reanudar")

    def mostrar_carta(self):
        self.btn_click_carta.pack_forget()
        self.video_label.pack_forget()
        self.carta_label.config(text=self.cartas[self.video_index])
        self.carta_label.pack(pady=30)

        if self.video_index == 2:
            self.mostrar_vista_final()
        else:
            self.btn_next_video.pack(pady=20)

    def siguiente_video(self):
        self.carta_label.pack_forget()
        self.btn_next_video.pack_forget()
        self.video_label.pack()
        self.video_index += 1
        self.btn_play_video.pack(pady=20)

    def mostrar_vista_final(self):
        pygame.mixer.music.load("cancion.mp3")
        pygame.mixer.music.play()

        self.video_label.pack_forget()
        self.btn_pause.pack_forget()
        self.btn_play_video.pack_forget()

        self.carta_label.pack(pady=20)
        self.btn_si.place(relx=0.35, rely=0.8, anchor="center")
        self.btn_no.place(relx=0.65, rely=0.8, anchor="center")

    def mover_boton_no(self):
        new_x = random.uniform(0.2, 0.8)
        new_y = random.uniform(0.7, 0.9)
        self.btn_no.place(relx=new_x, rely=new_y, anchor="center")

root = tk.Tk()
app = VideoApp(root)
root.mainloop()
