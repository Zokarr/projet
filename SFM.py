import customtkinter
from tkinter import filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image


class SupplyFlowMonitoringApp:
    def __init__(self, root, animated_panel):
        self.root = root
        self.animated_panel=animated_panel
        self.initialize_ui()

    def initialize_ui(self):
        self.root.geometry("800x500")
        self.root.title("Supply Flow Monitoring")
        self.create_widgets()

    def create_widgets(self):
        self.create_images()
        self.create_labels()
        self.create_dropdowns()
        self.create_buttons()
        self.create_entries()
        
    def create_images(self):
        self.new_img= customtkinter.CTkImage(light_image = Image.open(".\\assets\Orano.png"),
                                             size=(90,90),
                                             dark_image=Image.open(".\\assets\Orano.png"))

        self.opt = customtkinter.CTkImage(light_image = Image.open(".\\assets\opt-modified.png"),

                                            dark_image = Image.open(".\\assets\opt-modified.png"))

        self.opt1 = customtkinter.CTkImage(light_image = Image.open(".\\assets\coeur.png"),

                                            dark_image = Image.open(".\\assets\coeur.png"))
            
            
    def create_labels(self):
        self.material_label = customtkinter.CTkLabel(self.root, text="Matériau")
        self.material_label.place(x=20, y=100)

        self.data_label = customtkinter.CTkLabel(self.root, text="Donnée à tester")
        self.data_label.place(x=20, y=150)

        self.int_conf_label = customtkinter.CTkLabel(self.root, text="Intervalle de ""\n""confiance")
        self.int_conf_label.place(x=20, y=200)

        self.rebus_rate_label = customtkinter.CTkLabel(self.root, text="Taux de rebut:")
        self.rebus_rate_label.place(x=500, y=450)

        self.image_label = customtkinter.CTkLabel(self.root,text="", image=self.new_img)
        self.image_label.place(x=10,y=10)


        self.celine = customtkinter.CTkLabel(self.animated_panel,image = self.opt1, text ="CELINE JE T'AIME", width = 120, height = 120 , compound="right" ) 
        self.celine.pack()
        
    def create_dropdowns(self):
        material_options = ["Pierre", "Emma", "Sam-muelle"]
        self.material_dropdown = customtkinter.CTkOptionMenu(self.root,fg_color="gray28",button_hover_color="dark goldenrod", button_color="goldenrod" ,values=material_options,dropdown_hover_color="gray25",dropdown_fg_color="gray28")
        self.material_dropdown.place(x=120, y=100)

        data_options = ["Pierre", "Emma", "Sam-muelle"]
        self.data_dropdown = customtkinter.CTkOptionMenu(self.root,fg_color="gray28",button_color="goldenrod",button_hover_color="dark goldenrod", values=data_options,dropdown_hover_color="gray25",dropdown_fg_color="gray28")
        self.data_dropdown.place(x=120, y=150)

    def create_buttons(self):
        self.open_button = customtkinter.CTkButton(
            self.root, text="Ouvrir un fichier Excel",
            compound="left", command=self.open_csv_file,
            hover_color="gray28", border_color="gold",
            fg_color="transparent", border_width=2
        )
        self.open_button.place(x=120, y=100)

        # Créez le bouton Analyser sans l'ajouter à la SlidePanel
        self.analyze_button = customtkinter.CTkButton(
            self.root, text="Analyser",
            hover_color="gray28", border_color="gold",
            border_width=2, fg_color="transparent"
        )

        self.animated_panel = customtkinter.CTkButton(self.root, image= self.opt, text="" ,command = animated_panel.animate,
            fg_color="transparent", hover_color = "black",
            width=30

             )

        self.animated_panel.place(x=0, y= 400)


   # def animate_analyze_button(self, start_pos, end_pos):
        # Cette méthode gérera l'animation du bouton Analyser
       # delta = 3 if end_pos > start_pos else -3
    #    if (delta > 0 and start_pos < end_pos) or (delta < 0 and start_pos > end_pos):
     #       start_pos += delta
     #       self.analyze_button.place_configure(x=start_pos, y=350)
           # self.root.after(10, lambda: self.animate_analyze_button(start_pos, end_pos))
        #else:
      #      # Mettez à jour la commande du bouton une fois l'animation terminée
      #      self.analyze_button.configure(command= lambda : self.analyze_data(self.data))
            
            
            
            
    def create_entries(self):
        self.alpha_entry = customtkinter.CTkEntry(self.root, placeholder_text="valeur en %",border_color="gold", border_width=2)
        self.alpha_entry.place(x=120, y=200)

    def open_csv_file(self):
        
        excel_file = filedialog.askopenfilename(filetypes=[("Fichiers Excel", "*.xlsx")])
        if excel_file:  # Vérifiez si un fichier a été sélectionné
            self.data = pd.read_excel(excel_file, sheet_name="Jeu1")
        # Mettre à jour la commande du bouton après avoir chargé les données
            self.analyze_button.place(x=120,y=250)
            self.analyze_button.configure(command= lambda : self.analyze_data(self.data))



    def analyze_data(self, data=None):
      if data is not None:
        
        Nom_donnees_x = data.columns[1] # On récupère le nom de la colonne 1
        x_data = data[Nom_donnees_x]  # On récupère les données de la colonne 1
        mean, std = np.mean(x_data), np.std(x_data)

    
        x_data2 = np.linspace(min(x_data), max(x_data), len(x_data))  
        y_normale = (1 / (std * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_data2 - mean) / std) ** 2)

        pdf = stats.norm.pdf(x_data, mean, std)
        
        ks_statistic, ks_p_value = stats.kstest(x_data, 'norm', args=(mean, std))

    # Créez une figure
        fig, ax1 = plt.subplots(figsize=(4,4))

    
    # Créez un histogramme 1D sur le premier axe
        ax1.hist(x_data, bins=20, rwidth=0.85, color="gray")
        ax1.set_xlabel(Nom_donnees_x)
        ax1.set_ylabel('Fréquence')
        ax1.set_title('Histogramme 1D')


    # Créez un deuxième axe des ordonnées partageant le même axe des abscisses
        ax2 = ax1.twinx()

    
    # Ajoutez une légende
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper right')
        pdf = stats.norm.pdf(x_data2, mean, std)
        y_normale=pdf * len(x_data) * (max(x_data) - min(x_data)) / 20
        ax2.set_ylim(0, max(y_normale))
        ax2.fill_between(x_data2, y_normale, 0, where=(x_data2 >= min(x_data2)) & (x_data2 <=11 ), color='lightblue', alpha=0.5, label='Rebut')

        if ks_p_value < 0.05:
            ks_result = "Les données ne suivent probablement pas une distribution gaussienne (p-value < 0.05)"
            # Ajuster la gaussienne aux données et afficher en rouge pointillé
            self.label_ks1=customtkinter.CTkLabel(self.root)
            
            self.label_ks1.place(x=340,y=350)
            ax2.plot(x_data2,y_normale, 'y--', linewidth=2, label='Gaussian Fit (Rejected)')
        else:
                 ks_result = "Les données suivent probablement une distribution gaussienne (p-value >= 0.05)"
         # Ajuster la gaussienne aux données et afficher en trait plein noir
                 self.label_ks2=customtkinter.CTkLabel(self.root, text=ks_result)

                 self.label_ks2.place(x=340,y=350)
                 ax2.plot(x_data2,y_normale, 'yellow', linewidth=2, label='Gaussian Fit (Accepted)')
    # Créez un canevas tkinter pour afficher la figure
        ax2.legend(loc="upper right")
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.get_tk_widget().place(x=500, y=10)
        canvas.draw()
      


# Slide Panel ----------------------------------------------

class SlidePanel(customtkinter.CTkFrame):
    def __init__(self, parent, start_pos, end_pos):
        super().__init__(master = parent)
        # general attributes 
        self.start_pos = start_pos + 0.04
        self.end_pos = end_pos - 0.03
        self.width = abs(start_pos - end_pos)

        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True

        # layout
        self.place(relx = self.start_pos, rely = 0.05, relwidth = 0.3, relheight = 0.2)

    def animate(self):
        if self.in_start_pos:
            self.animate_forward()
        else:
            self.animate_backwards()

    def animate_forward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.008
            self.place(relx = self.pos, rely = 0.05, relwidth = 0.3, relheight = 0.2)
            self.after(10, self.animate_forward)
        else:
            self.in_start_pos = False

    def animate_backwards(self):
        if self.pos < self.start_pos:
            self.pos += 0.008
            self.place(relx = self.pos, rely = 0.05, relwidth = self.width, relheight = 0.9)
            self.after(10, self.animate_backwards)
        else:
            self.in_start_pos = True



if __name__ == "__main__":
    plt.style.use('dark_background')

    root = customtkinter.CTk()
    root.configure(fg_color=["#121522", "#000000"])
    animated_panel = SlidePanel(root, 1.0, 0.7)

    app = SupplyFlowMonitoringApp(root,animated_panel)
    customtkinter.set_appearance_mode("dark")
    root.iconbitmap('.\\assets\icone.ico')
    
    root.mainloop()
