import customtkinter
import tkintermapview
import sys, pathlib, webbrowser
from PIL import Image
from tkextrafont import Font
from runtime.data_analysis import IdealHomeDataAnalysis
current_path = str(pathlib.Path(__file__).parent.parent)

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Window Title
        self.title("Ideal Home Location Matcher")

        # Default Window Size
        self.geometry(f"{1280}x{850}")

        # Load Custom Fonts
        Font(file="assets/fonts/Neuton-Regular.ttf")
        Font(file="assets/fonts/Cabin-Regular.ttf")
        Font(file="assets/fonts/Cabin-Bold.ttf")
        
        regular_font = customtkinter.CTkFont(family='Cabin', size=16, weight="normal")
        bold_font = customtkinter.CTkFont(family='Cabin', size=16, weight="bold")

        # Configure App Grid Layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        """ 
            Main Frame 
        """
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.main_frame.grid_rowconfigure(4, weight=0)
        self.main_frame.grid_columnconfigure(3, weight=0)
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/assets/images/Ideal_Home_Location_Matcher.png"),size=(620, 128))
        self.bg_image_label = customtkinter.CTkLabel(self.main_frame, text='', image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(10, 10), sticky='n')
        # self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),dark_image=Image.open(os.path.join(image_path, "home_light.png")), size=(20, 20))

        # Intro
        self.introduction_frame = customtkinter.CTkFrame(self.main_frame, corner_radius=0)
        self.introduction_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.introduction_frame.grid_rowconfigure(3, weight=0)
        self.introduction_frame.grid_columnconfigure(3, weight=0)
        self.logo_label = customtkinter.CTkLabel(self.introduction_frame, text="Introduction", font=customtkinter.CTkFont(family='Neuton', size=24, weight="normal"))
        self.logo_label.grid(row=0, column=0, columnspan=1, padx=20, pady=(10, 10), sticky='n')

        self.textbox = customtkinter.CTkTextbox(self.introduction_frame, width=250)
        self.textbox.grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.textbox.insert("0.0", "CTkTextbox")
        self.textbox.configure(state="disabled")

        self.main_button_1 = customtkinter.CTkButton(master=self.main_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"))
        self.main_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="nsew")

        
        """ 
            Sidebar Frame 
        """
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", font=regular_font)
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event, font=regular_font, dropdown_font=regular_font)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", font=regular_font)
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event, font=regular_font, dropdown_font=regular_font)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.end_label = customtkinter.CTkLabel(self.sidebar_frame, text="End", anchor="n", font=regular_font)
        self.end_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        self.progressbar_3 = customtkinter.CTkProgressBar(self.sidebar_frame, height=500, orientation="vertical")
        self.progressbar_3.grid(row=1, column=0, rowspan=2, padx=(10, 10), pady=(10, 10), sticky='ns')

        self.start_label = customtkinter.CTkLabel(self.sidebar_frame, text="Start", font=regular_font)
        self.start_label.grid(row=4, column=0, padx=20, pady=(20, 20), sticky='n')

        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

        # After Main Frame and Sidebar Frame Load Data Analysis Class
        self.IdealHomeDataAnalysis = IdealHomeDataAnalysis()

        """ Family Location Frame 1"""
        self.family_location_frame1 = customtkinter.CTkFrame(self)
        # # create checkbox and switch frame
        # self.checkbox_slider_frame = customtkinter.CTkFrame(self, corner_radius=0)
        # self.checkbox_slider_frame.grid(row=2, column=2, padx=(20, 20), pady=(20, 0), sticky="nsew")
        # self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_1.grid(row=1, column=0, pady=(20, 10), padx=20, sticky="n")
        # self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame)
        # self.checkbox_2.grid(row=2, column=0, pady=10, padx=20, sticky="n")
        # self.switch_1 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame, command=lambda: print("switch 1 toggle"))
        # self.switch_1.grid(row=3, column=0, pady=10, padx=20, sticky="n")
        # self.switch_2 = customtkinter.CTkSwitch(master=self.checkbox_slider_frame)
        # self.switch_2.grid(row=4, column=0, pady=(10, 20), padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        #self.slider_progressbar_frame.grid(row=1, column=1, columnspan=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        #self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
     
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")
     
        



    def login_event(self):
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())

        self.login_frame.grid_forget()  # remove login frame
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=100)  # show main frame

    def back_event(self):
        self.main_frame.grid_forget()  # remove main frame
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def github_more_information():
        webbrowser.open_new('https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
