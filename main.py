import vlc
import tkinter as tk
from tkinter import filedialog
import time
import threading


class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecteur Vidéo MP4")
        self.root.geometry("800x650")
        self.root.configure(bg='black')

        # Créer une instance du lecteur VLC
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Créer un canevas pour afficher la vidéo
        self.canvas = tk.Canvas(root, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=1)

        # Ajouter une barre de progression
        self.progress_scale = tk.Scale(
            root,
            orient='horizontal',
            length=600,
            from_=0,
            to=100,
            sliderlength=10,
            bg='black',
            fg='white',
            troughcolor='gray',
            highlightthickness=0,
        )
        self.progress_scale.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

        # Ajouter des boutons pour contrôler la vidéo
        control_frame = tk.Frame(root, bg='black')
        control_frame.pack(side=tk.BOTTOM)

        self.play_button = tk.Button(
            control_frame, text="Play", command=self.play_video
        )
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(
            control_frame, text="Pause", command=self.pause_video
        )
        self.pause_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(
            control_frame, text="Stop", command=self.stop_video
        )
        self.stop_button.pack(side=tk.LEFT, padx=10)

        self.load_button = tk.Button(
            control_frame, text="Load", command=self.load_video
        )
        self.load_button.pack(side=tk.LEFT, padx=10)

        # Ajouter une barre de volume
        self.volume_scale = tk.Scale(
            control_frame,
            orient='horizontal',
            length=200,
            from_=0,
            to=100,
            sliderlength=10,
            bg='black',
            fg='white',
            troughcolor='gray',
            highlightthickness=0,
            label='Volume',
            command=self.set_volume,
        )
        self.volume_scale.set(50)  # Volume par défaut à 50%
        self.volume_scale.pack(side=tk.RIGHT, padx=10)

        # Variable pour garder le statut de mise à jour de la progression
        self.update_progress = False

    def load_video(self):
        # Charger le fichier vidéo MP4
        video_path = filedialog.askopenfilename(
            filetypes=[("Fichiers MP4", "*.mp4")]
        )
        if video_path:
            media = self.instance.media_new(video_path)
            self.player.set_media(media)

            # Définir le canevas comme output vidéo
            self.player.set_hwnd(self.canvas.winfo_id())

            # Reset la barre de progression
            self.progress_scale.set(0)
            self.update_progress = False

    def play_video(self):
        # Lire la vidéo
        self.player.play()

        # Démarrer le thread pour mettre à jour la barre de progression
        self.update_progress = True
        threading.Thread(target=self.update_progress_bar, daemon=True).start()

    def pause_video(self):
        # Mettre la vidéo en pause
        self.player.pause()

    def stop_video(self):
        # Arrêter la vidéo
        self.player.stop()
        self.update_progress = False
        self.progress_scale.set(0)

    def update_progress_bar(self):
        while self.update_progress:
            time.sleep(1)  # Mettre à jour toutes les secondes

            # Obtenir la durée actuelle et totale de la vidéo
            total_duration = self.player.get_length() / 1000  # en secondes
            current_time = self.player.get_time() / 1000  # en secondes

            if total_duration > 0:
                # Calculer la position actuelle de la vidéo en pourcentage
                progress = (current_time / total_duration) * 100
                self.progress_scale.set(progress)

            if self.player.get_state() == vlc.State.Ended:
                self.update_progress = False

    def set_video_position(self, event):
        # Modifier la position de la vidéo lorsque l'utilisateur change la barre de progression
        new_position = self.progress_scale.get() / 100.0  # Convertir en fraction
        self.player.set_position(new_position)

    def set_volume(self, volume):
        # Régler le volume du lecteur VLC
        self.player.audio_set_volume(int(volume))


# Création de la fenêtre principale
root = tk.Tk()
player = VideoPlayer(root)

# Connecter la barre de progression à la fonction de changement de position
player.progress_scale.bind("<ButtonRelease-1>", player.set_video_position)

root.mainloop()
