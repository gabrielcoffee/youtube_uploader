import tkinter as tk
from tkinter import filedialog
from auth import authenticate_youtube
from upload import upload_multiple_videos

client_json_path = ""
video_paths = []

def upload_client_json():
    global client_json_path
    client_json_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if client_json_path:
        client_json_label.config(text="Arquivo recebido")
    else:
        client_json_label.config(text="Nenhum arquivo selecionado")
    print(client_json_path)

def upload_videos():
    global video_paths
    video_paths = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4")])
    if video_paths:
        videos_label.config(text=f"{len(video_paths)} vídeos selecionados")
    else:
        videos_label.config(text="Nenhum vídeo selecionado")
    print(video_paths)

def publish_videos():
    youtube = authenticate_youtube(client_json_path)
    title = title_entry.get()
    description = description_entry.get()
    tags = tags_entry.get().split(',')
    privacy_status = privacy_var.get()
    is_title_filename = title_description.get() == "title_filename"
    upload_multiple_videos(youtube, video_paths, is_title_filename, title, description, tags, privacy_status)

def update_title_entry(*args):
    if title_description.get() == "title_filename":
        title_entry.config(state='disabled')
    else:
        title_entry.config(state='normal')

def create_first_page():
    first_page = tk.Tk()
    first_page.title("Upload de vídeos")
    first_page.geometry("800x800")  # Make the window bigger

    # Add a logo at the top with a larger font
    logo_label = tk.Label(first_page, text="Youtube Auto Uploader", font=("Helvetica", 32))
    logo_label.pack(pady=(20, 40))  # Add space above and below the logo

    # create a button to upload the client.json file
    upload_client_json_button = tk.Button(first_page, text="Upload client.json", command=upload_client_json, width=20, height=2)
    upload_client_json_button.pack(pady=3)
    global client_json_label
    client_json_label = tk.Label(first_page, text="Nenhum arquivo selecionado")
    client_json_label.pack(pady=5)

    # create a button to upload videos
    upload_videos_button = tk.Button(first_page, text="Upload vídeos", command=upload_videos, width=20, height=2)
    upload_videos_button.pack(pady=3)
    global videos_label
    videos_label = tk.Label(first_page, text="Nenhum vídeo selecionado")
    videos_label.pack(pady=5)

    # Add a text above the radio buttons
    options_label = tk.Label(first_page, text="Escolha uma opção para o título dos vídeos")
    options_label.pack(pady=10)

    # create a radio button with the options "Título e descrição padrão" and "Nome do arquivo como título"
    global title_description
    title_description = tk.StringVar()
    title_description.set("title_default")
    title_description.trace('w', update_title_entry)

    radio_button1 = tk.Radiobutton(first_page, text="Título padrão (com numeração)", variable=title_description, value="title_default")
    radio_button1.pack(pady=2)

    radio_button2 = tk.Radiobutton(first_page, text="Nome do arquivo como título", variable=title_description, value="title_filename")
    radio_button2.pack(pady=5)

    # Add entries for title, description, and tags
    global title_entry, description_entry, tags_entry
    title_label = tk.Label(first_page, text="Título padrão:")
    title_label.pack()
    title_entry = tk.Entry(first_page, width=50)
    title_entry.pack(pady=5)

    description_label = tk.Label(first_page, text="Descrição padrão:")
    description_label.pack()
    description_entry = tk.Entry(first_page, width=50)
    description_entry.pack(pady=5)

    tags_label = tk.Label(first_page, text="Tags (separadas por vírgula):")
    tags_label.pack()
    tags_entry = tk.Entry(first_page, width=50)
    tags_entry.pack(pady=5)

    # Add radio buttons for privacy status
    global privacy_var
    privacy_var = tk.StringVar()
    privacy_var.set("private")

    privacy_label = tk.Label(first_page, text="Privacidade:")
    privacy_label.pack(pady=10)
    radio_button_public = tk.Radiobutton(first_page, text="Público", variable=privacy_var, value="public")
    radio_button_public.pack(pady=5)
    radio_button_private = tk.Radiobutton(first_page, text="Privado", variable=privacy_var, value="private")
    radio_button_private.pack(pady=5)

    # Add a text before the last button
    redirect_label = tk.Label(first_page, text="Você será redirecionado a uma página na web para confirmar sua conta do Google/Youtube\nAo confirmar os vídeos serão publicados automaticamente, você pode conferir o terminal para ver o progresso")
    redirect_label.pack(pady=(30, 5))

    # create a button to publish videos
    publish_button = tk.Button(first_page, text="Publicar Vídeos", command=publish_videos, width=20, height=2)
    publish_button.pack(pady=20)

    first_page.mainloop()