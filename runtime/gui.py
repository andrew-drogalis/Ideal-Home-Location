import customtkinter
import tkintermapview
import sys, pathlib, webbrowser
from PIL import Image
from tkextrafont import Font
from runtime.data_analysis import IdealHomeDataAnalysis
current_path = str(pathlib.Path(__file__).parent.parent)

"""
    Built with Custom Tkinter: https://github.com/TomSchimansky/CustomTkinter/wiki
"""

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Window Title
        self.title("Ideal Home Location Matcher")

        # Default Window Size
        self.geometry(f"{1100}x{850}")

        # Load Custom Fonts
        Font(file="assets/fonts/Neuton-Regular.ttf")
        Font(file="assets/fonts/Cabin-Regular.ttf")
        Font(file="assets/fonts/Cabin-Bold.ttf")
        
        title_font = customtkinter.CTkFont(family='Neuton', size=24, weight="normal")
        regular_font = customtkinter.CTkFont(family='Cabin', size=16, weight="normal")
        bold_font = customtkinter.CTkFont(family='Cabin', size=16, weight="bold")

        # Configure App Grid Layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        """ 
            Header Frame 
        """
        self.header_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.header_frame.grid_rowconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/assets/images/Ideal_Home_Location_Matcher.png"),size=(403, 86))
        self.bg_image_label = customtkinter.CTkLabel(self.header_frame, text='', image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky='nw')
        self.github_image = customtkinter.CTkImage(light_image=Image.open(current_path + "/assets/images/github-mark.png"),dark_image=Image.open(current_path + "/assets/images/github-mark-white.png"), size=(76, 25))
        self.github_button = customtkinter.CTkButton(self.header_frame, image=self.github_image, width=90, hover_color=('#fff','#000'), text='', compound='right', fg_color='transparent', bg_color='transparent', command=self.github_more_information)
        self.github_button.grid(row=0, column=1, padx=0, pady=(10, 10), sticky='ne')

        """ 
            Sidebar Frame 
        """
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", font=regular_font)
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event, font=regular_font, dropdown_font=regular_font)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", font=regular_font)
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event, font=regular_font, dropdown_font=regular_font)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.end_label = customtkinter.CTkLabel(self.sidebar_frame, text="Finish Line", anchor="n", font=regular_font)
        self.end_label.grid(row=0, column=0, padx=20, pady=(20, 20))

        self.progressbar = customtkinter.CTkProgressBar(self.sidebar_frame, orientation="vertical")
        self.progressbar.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky='ns')
        self.progressbar.set(0)

        self.start_label = customtkinter.CTkLabel(self.sidebar_frame, text="Start Line", font=regular_font)
        self.start_label.grid(row=3, column=0, padx=20, pady=(20, 20), sticky='n')

        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")



        """ 
            Introduction Frame 
        """
        self.intro_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.intro_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.intro_frame.grid_rowconfigure(3, weight=1)
        self.intro_frame.grid_columnconfigure(1, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.intro_frame, text="Introduction", font=title_font)
        self.logo_label.grid(row=1, column=0, padx=25, pady=(10, 5), sticky='e')

        self.textbox = customtkinter.CTkTextbox(self.intro_frame, height=400, font=regular_font)
        self.textbox.grid(row=2, column=0, columnspan=4, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.textbox.insert("0.0", "CTkTextbox")
        self.textbox.configure(state="disabled")

        self.intro_button_1 = customtkinter.CTkButton(master=self.intro_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.intro_button_event)
        self.intro_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")


        # After Introduction Frame Load Data Analysis Class
        self.IdealHomeDataAnalysis = IdealHomeDataAnalysis()

        """ 
            Family Location Frame 1
        """
        self.family_location_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.family_location_frame.grid_rowconfigure(3, weight=1)
        self.family_location_frame.grid_columnconfigure(1, weight=1)
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
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.family_location_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
     
        self.seg_button_1.configure(values=["CTkSegmentedButton", "Value 2", "Value 3"])
        self.seg_button_1.set("Value 2")

        self.family_location_button_1 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_forward_event)
        self.family_location_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_location_button_2 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_backward_event)
        self.family_location_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")
        

        """ 
            Family Details Frame 1b
        """
        self.family_details_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.family_details_frame.grid_rowconfigure(3, weight=1)
        self.family_details_frame.grid_columnconfigure(1, weight=1)



        self.family_details_button_1 = customtkinter.CTkButton(master=self.family_details_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1b_forward_event)
        self.family_details_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_details_button_2 = customtkinter.CTkButton(master=self.family_details_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1b_backward_event)
        self.family_details_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")
        

        """ 
            Work Location Frame 2
        """
        self.work_location_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.work_location_frame.grid_rowconfigure(3, weight=1)
        self.work_location_frame.grid_columnconfigure(1, weight=1)


        self.work_location_button_1 = customtkinter.CTkButton(master=self.work_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_2_forward_event)
        self.work_location_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.work_location_button_2 = customtkinter.CTkButton(master=self.work_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_2_backward_event)
        self.work_location_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        
        """ 
            Work Details Frame 2b
        """
        self.work_details_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.work_details_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.work_details_frame.grid_rowconfigure(3, weight=1)
        self.work_details_frame.grid_columnconfigure(1, weight=1)


        self.family_location_button_1 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_forward_event)
        self.family_location_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_location_button_2 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_backward_event)
        self.family_location_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        
        """ 
            Income Metrics Frame 3
        """
        self.income_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.income_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.income_frame.grid_rowconfigure(3, weight=1)
        self.income_frame.grid_columnconfigure(1, weight=1)



        self.family_location_button_1 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_forward_event)
        self.family_location_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_location_button_2 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_backward_event)
        self.family_location_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        
        """ 
            Area Classification Frame 4
        """
        self.area_classification_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.area_classification_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.area_classification_frame.grid_rowconfigure(3, weight=1)
        self.area_classification_frame.grid_columnconfigure(1, weight=1)


        self.family_location_button_1 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_forward_event)
        self.family_location_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_location_button_2 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_backward_event)
        self.family_location_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        """ 
            Weather Metrics Frame 5
        """
        self.weather_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.weather_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.weather_frame.grid_rowconfigure(3, weight=1)
        self.weather_frame.grid_columnconfigure(1, weight=1)



        self.family_location_button_1 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_forward_event)
        self.family_location_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_location_button_2 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_backward_event)
        self.family_location_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")
        
        """ 
            Natural Disaster Risk Frame 6
        """
        self.natural_disaster_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.natural_disaster_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.natural_disaster_frame.grid_rowconfigure(3, weight=1)
        self.natural_disaster_frame.grid_columnconfigure(1, weight=1)



        self.family_location_button_1 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_forward_event)
        self.family_location_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_location_button_2 = customtkinter.CTkButton(master=self.family_location_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_backward_event)
        self.family_location_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        """ 
            Results Frame 7
        """
        self.results_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.natural_disaster_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.results_frame.grid_rowconfigure(3, weight=1)
        self.results_frame.grid_columnconfigure(1, weight=1)


        self.results_button_1 = customtkinter.CTkButton(master=self.results_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_7_backward_event)
        self.results_button_1.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")


    def intro_button_event(self):
        self.intro_frame.grid_forget()
        self.family_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.11)

    # FRAME 1
    def frame_1_forward_event(self):
        self.family_location_frame.grid_forget()
        if 1 == 1:
            self.family_details_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.22)
        else:
            self.work_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.33)

    def frame_1_backward_event(self):
        self.family_location_frame.grid_forget()
        self.intro_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(0)

    # FRAME 1b
    def frame_1b_forward_event(self):
        self.family_details_frame.grid_forget()
        self.work_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.33)

    def frame_1b_backward_event(self):
        self.family_details_frame.grid_forget()
        self.family_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.11)

    # FRAME 2
    def frame_2_forward_event(self):
        self.work_location_frame.grid_forget()
        if 1 == 1:
            self.work_details_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.44)
        else:
            self.income_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.55)

    def frame_2_backward_event(self):
        self.work_location_frame.grid_forget()
        if 1 == 1:
            self.family_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.11)
        else:
            self.family_details_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.22)

    # FRAME 2b
    def frame_2b_forward_event(self):
        self.work_details_frame.grid_forget()
        self.income_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.55)

    def frame_2b_backward_event(self):
        self.work_details_frame.grid_forget()
        self.work_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.33)

    # FRAME 3
    def frame_3_forward_event(self):
        self.income_frame.grid_forget()
        self.area_classification_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.66)

    def frame_3_backward_event(self):
        self.income_frame.grid_forget()
        if 1 == 1:
            self.work_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.33)
        else:
            self.work_details_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.44)

    # FRAME 4
    def frame_4_forward_event(self):
        self.area_classification_frame.grid_forget()
        self.weather_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.77)

    def frame_4_backward_event(self):
        self.area_classification_frame.grid_forget()
        self.income_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.55)

    # FRAME 5
    def frame_5_forward_event(self):
        self.weather_frame.grid_forget()
        self.natural_disaster_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.88)

    def frame_5_backward_event(self):
        self.weather_frame.grid_forget()
        self.area_classification_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.66)

    # FRAME 6
    def frame_6_forward_event(self):
        self.natural_disaster_frame.grid_forget()
        self.results_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(1)

    def frame_6_backward_event(self):
        self.natural_disaster_frame.grid_forget()
        self.weather_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.77)

    # FRAME 7
    def frame_7_backward_event(self):
        self.results_frame.grid_forget()
        self.natural_disaster_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.88)

    # UTILITIES
    def github_more_information(self):
        webbrowser.open_new('https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
