from tkinter import messagebox, StringVar
import customtkinter
from tkintermapview import TkinterMapView
import os, sys, pathlib, webbrowser
from PIL import Image
from runtime.data_analysis import IdealHomeDataAnalysis
from runtime.utilities.instructions import instructions_text
from version import current_version
current_path = str(pathlib.Path(__file__).parent.parent)

"""
    Built with Custom Tkinter: https://github.com/TomSchimansky/CustomTkinter/wiki
"""

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.after(1, self.load_data_analysis)

        # Window Title
        self.title(" Ideal Home Location Matcher")

        # Add Ideal Home Icon
        self.iconbitmap(self.resource_path("assets/icon/Ideal_Home.ico"))
        self._windows_set_titlebar_color('dark')
        self.update()

        # Default Window Size
        self.geometry(f"{1200}x{1000}")

        # Load Custom Fonts
        font_manager = customtkinter.FontManager()
        font_manager.windows_load_font(font_path=self.resource_path("assets/fonts/Telex-Regular.ttf"))
        
        bold_font = customtkinter.CTkFont(family='Telex', size=16, weight="bold")
        self.title_font = customtkinter.CTkFont(family='Telex', size=28, weight="bold")
        self.regular_font = customtkinter.CTkFont(family='Telex', size=16, weight="normal")
        self.large_font = customtkinter.CTkFont(family='Telex', size=19, weight="normal")
        self.large_bold = customtkinter.CTkFont(family='Telex', size=19, weight="bold")

        # Component Label Colors
        self.label_color = ('#fff','#111')
        self.seg_button_unselected = ('#8da4b7','gray23') 
        self.seg_button_unselected_hover = ('#a1b5c4',"gray33")

        # Configure App Grid Layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # Initalize Class Variables
        self.family_location_frame = None
        self.family_location_valid1 = False
        self.family_location_valid2 = False
        self.family_details_frame = None
        self.work_frame = None
        self.work_valid1 = False
        self.income_frame = None
        self.income_entry1_valid = False
        self.income_entry2_valid = False
        self.area_classification_frame = None
        self.weather_frame = None
        self.natural_disaster_frame = None
        self.results_frame = None
        self.map_marker = None
        self.map_marker_region = None
        self.results_polygon = None
        self.radius_index = 0

        """ 
            Header Frame 
        """
        self.header_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e5f1fc','#32485c'))
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.header_frame.grid_rowconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        # Logo Image
        bg_image = customtkinter.CTkImage(Image.open(current_path + "/assets/images/Ideal_Home_Location_Matcher.png"),size=(358, 87))
        bg_image_label = customtkinter.CTkLabel(self.header_frame, text='', image=bg_image)
        bg_image_label.grid(row=0, column=0, padx=20, pady=10, sticky='nw')
        # Github Link
        github_image = customtkinter.CTkImage(light_image=Image.open(current_path + "/assets/images/github-mark.png"),dark_image=Image.open(current_path + "/assets/images/github-mark-white.png"), size=(81, 20))
        github_button = customtkinter.CTkButton(self.header_frame, image=github_image, width=90, hover_color=('#fff','#000'), text='', compound='right', fg_color='transparent', bg_color='transparent', command=self.github_more_information)
        github_button.grid(row=0, column=1, padx=15, pady=10, sticky='e')
        # Version label
        version_label = customtkinter.CTkLabel(self.header_frame, text=f'Version: {current_version}', font=customtkinter.CTkFont(family='Telex', size=12, weight="normal"))
        version_label.grid(row=0, column=1, padx=19, pady=10, sticky='se')

        """ 
            Sidebar Frame 
        """
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0, fg_color=('#e5f1fc','#32485c'))
        self.sidebar_frame.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        # Finish Label
        finish_label = customtkinter.CTkLabel(self.sidebar_frame, text="Finish Line", anchor="center", font=bold_font, fg_color=self.label_color)
        finish_label.grid(row=0, column=0, ipadx=10, padx=10, pady=(40, 20))
        # Progres Bar 
        self.progressbar = customtkinter.CTkProgressBar(self.sidebar_frame, width=10, orientation="vertical", border_width=1, fg_color='#fff')
        self.progressbar.grid(row=1, column=0, padx=10, pady=10, sticky='ns')
        self.progressbar.set(0)
        # Start Label
        start_label = customtkinter.CTkLabel(self.sidebar_frame, text="Start Line", font=bold_font, fg_color=self.label_color)
        start_label.grid(row=3, column=0, ipadx=10, padx=10, pady=20, sticky='')
        # Settings Label
        settings_label = customtkinter.CTkLabel(self.sidebar_frame, text="Settings", font=bold_font, fg_color=self.label_color)
        settings_label.grid(row=5, column=0, ipadx=18, padx=10, pady=(10, 10))
        # Appearance Mode
        color_mode_image = customtkinter.CTkImage(light_image=Image.open(current_path + "/assets/images/color_mode_black.png"),dark_image=Image.open(current_path + "/assets/images/color_mode_white.png"), size=(20, 20))
        color_mode_label = customtkinter.CTkLabel(self.sidebar_frame, image=color_mode_image, text="")
        color_mode_label.grid(row=6, column=0, padx=(5,0), pady=0, sticky='w')
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, width=100, values=["Light", "Dark", "System"], anchor='center', command=self.change_appearance_mode_event, font=self.regular_font, dropdown_font=self.regular_font)
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=(40,10), pady=10)
        self.appearance_mode_optionmenu.set("System")
        # Zoom %
        zoom_image = customtkinter.CTkImage(light_image=Image.open(current_path + "/assets/images/zoom_black.png"),dark_image=Image.open(current_path + "/assets/images/zoom_white.png"), size=(20, 20))
        zoom_label = customtkinter.CTkLabel(self.sidebar_frame, image=zoom_image, text="")
        zoom_label.grid(row=8, column=0, padx=(5,0), pady=(0, 5), sticky='w')
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, width=100, values=["80%", "90%", "100%", "110%", "120%"], anchor='center', command=self.change_scaling_event, font=self.regular_font, dropdown_font=self.regular_font)
        self.scaling_optionemenu.grid(row=8, column=0, padx=(40,10), pady=(10, 20))
        self.scaling_optionemenu.set("100%")

        """ 
            Instructions Frame 
        """
        self.intro_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.intro_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.intro_frame.grid_rowconfigure(3, weight=1)
        self.intro_frame.grid_columnconfigure(0, weight=1)
        # Page Title
        instructions_title = customtkinter.CTkLabel(self.intro_frame, text="Instructions", font=self.title_font, fg_color=self.label_color)
        instructions_title.grid(row=0, column=0, columnspan=3, ipady=1, ipadx=20, padx=20, pady=15, sticky='')
        # App Instructions
        instructions_textbox = customtkinter.CTkTextbox(self.intro_frame, border_width=1, fg_color=self.label_color, height=650, font=self.regular_font, wrap='word')
        instructions_textbox.grid(row=1, column=0, columnspan=3, padx=20, pady=15, sticky="nsew")
        instructions_textbox.insert("0.0", instructions_text)
        instructions_textbox.configure(state="disabled")
        # Navigation Button
        instruction_get_started_button = customtkinter.CTkButton(master=self.intro_frame, width=120, height=30, border_width=1, text='Get Started', text_color="#DCE4EE", font=self.regular_font, command=self.instruction_button_event)
        instruction_get_started_button.grid(row=3, column=2, padx=20, pady=20, sticky="s")


    def build_family_location_frame_1(self):
        self.family_location_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.family_location_frame.grid_rowconfigure((3,5,8,10,13), weight=1)
        self.family_location_frame.grid_columnconfigure(0, weight=1)

        # Initalize Work Frame
        if not self.work_frame:
            self.build_work_frame_2()
    
        family_location_title = customtkinter.CTkLabel(self.family_location_frame, text="Ideal Family Preferences", font=self.title_font, fg_color=self.label_color)
        family_location_title.grid(row=0, column=0, columnspan=3, padx=20, ipady=1, ipadx=20, pady=15, sticky='')
        
        # Family Location Question #1
        family_location_label_1 = customtkinter.CTkLabel(self.family_location_frame, text="Do you want to be nearby family members?", font=self.large_font, fg_color=self.label_color)
        family_location_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
        
        self.family_location_seg_button_1 = customtkinter.CTkSegmentedButton(self.family_location_frame, font=self.regular_font, command=self.seg_button_family_location, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.family_location_seg_button_1.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.family_location_seg_button_1.configure(values=["Yes", "No"])
        self.family_location_seg_button_1.set("No")

        # Family Location Entry Frame #1
        self.family_location_entry_frame1 = customtkinter.CTkFrame(self.family_location_frame, corner_radius=0, fg_color=('#d1d7e1',"gray22"))
        self.family_location_entry_frame1.grid_rowconfigure(10, weight=1)
        self.family_location_entry_frame1.grid_columnconfigure((0, 1, 2, 3), weight=1)

        family_location_entry_label_1 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="Please enter the first location:", font=self.large_font, fg_color=self.label_color)
        family_location_entry_label_1.grid(row=0, column=0, columnspan=4, padx=40, pady=(10,5), sticky='')

        family_location_city_label_1 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="City:", font=self.large_font, fg_color=self.label_color)
        family_location_city_label_1.grid(row=1, column=0, padx=60, pady=5, sticky='n')

        family_location_state_label_1 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="State:", font=self.large_font, fg_color=self.label_color)
        family_location_state_label_1.grid(row=1, column=1, padx=40, pady=5, sticky='n')

        family_location_zipcode_label_1 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="Zipcode:", font=self.large_font, fg_color=self.label_color)
        family_location_zipcode_label_1.grid(row=1, column=2, padx=40, pady=5, sticky='n')

        self.family_location_entry1 = customtkinter.CTkEntry(self.family_location_entry_frame1, width=250, placeholder_text='City', font=self.large_font)
        self.family_location_entry1.grid(row=2, column=0, padx=40, pady=5, sticky='n')
        self.family_location_entry1.bind("<Return>", self.family_location_button1_verify)

        self.family_location_entry2 = customtkinter.CTkEntry(self.family_location_entry_frame1, placeholder_text='State', font=self.large_font)
        self.family_location_entry2.grid(row=2, column=1, padx=40, pady=5, sticky='n')
        self.family_location_entry2.bind("<Return>", self.family_location_button1_verify)

        self.family_location_entry3 = customtkinter.CTkEntry(self.family_location_entry_frame1, placeholder_text='Zipcode', font=self.large_font)
        self.family_location_entry3.grid(row=2, column=2, padx=40, pady=5, sticky='n')
        self.family_location_entry3.bind("<Return>", self.family_location_button1_verify)

        # Verify Submission #1
        self.family_location_verify_button_1 = customtkinter.CTkButton(master=self.family_location_entry_frame1, text='Verify', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.family_location_button1_verify)
        self.family_location_verify_button_1.grid(row=2, column=3, padx=(20, 30), pady=(5,10), sticky="n")

        self.family_location_confirmation_output_1 = customtkinter.CTkEntry(self.family_location_entry_frame1, width=450, font=self.large_font, state='disabled')

        self.family_location_confirm_button_1 = customtkinter.CTkButton(master=self.family_location_entry_frame1, text='Confirm', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.family_location_button1_confirm)

        # Family Location Question #2
        self.family_location_label2 = customtkinter.CTkLabel(self.family_location_frame, text="Additional Location?", font=self.large_font, fg_color=self.label_color)

        self.family_location_seg_button_2 = customtkinter.CTkSegmentedButton(self.family_location_frame, font=self.regular_font, command=self.seg_button_family_location_2, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.family_location_seg_button_2.configure(values=["Yes", "No"])
        self.family_location_seg_button_2.set("No")

        # Family Location Entry Frame #2
        self.family_location_entry_frame2 = customtkinter.CTkFrame(self.family_location_frame, corner_radius=0, fg_color=('#d1d7e1',"gray22"))
        self.family_location_entry_frame2.grid_rowconfigure(10, weight=1)
        self.family_location_entry_frame2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        family_location_entry_label_2 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="Please enter the second location:", font=self.large_font, fg_color=self.label_color)
        family_location_entry_label_2.grid(row=0, column=0, columnspan=4, padx=40, pady=(10,5), sticky='')

        family_location_city_label_2 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="City:", font=self.large_font, fg_color=self.label_color)
        family_location_city_label_2.grid(row=1, column=0, padx=60, pady=5, sticky='n')

        family_location_state_label_2 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="State:", font=self.large_font, fg_color=self.label_color)
        family_location_state_label_2.grid(row=1, column=1, padx=40, pady=5, sticky='n')

        family_location_zipcode_label_2 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="Zipcode:", font=self.large_font, fg_color=self.label_color)
        family_location_zipcode_label_2.grid(row=1, column=2, padx=40, pady=5, sticky='n')

        self.family_location_entry4 = customtkinter.CTkEntry(self.family_location_entry_frame2, width=250, placeholder_text='City', font=self.large_font)
        self.family_location_entry4.grid(row=2, column=0, padx=40, pady=5, sticky='n')
        self.family_location_entry4.bind("<Return>", self.family_location_button2_verify)

        self.family_location_entry5 = customtkinter.CTkEntry(self.family_location_entry_frame2, placeholder_text='State', font=self.large_font)
        self.family_location_entry5.grid(row=2, column=1, padx=40, pady=5, sticky='n')
        self.family_location_entry5.bind("<Return>", self.family_location_button2_verify)

        self.family_location_entry6 = customtkinter.CTkEntry(self.family_location_entry_frame2, placeholder_text='Zipcode', font=self.large_font)
        self.family_location_entry6.grid(row=2, column=2, padx=40, pady=5, sticky='n')
        self.family_location_entry6.bind("<Return>", self.family_location_button2_verify)

        # Verify Submission #2
        self.family_location_verify_button_2 = customtkinter.CTkButton(master=self.family_location_entry_frame2, text='Verify', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.family_location_button2_verify)
        self.family_location_verify_button_2.grid(row=2, column=3, padx=(20, 30), pady=(5,10), sticky="n")

        self.family_location_confirmation_output_2 = customtkinter.CTkEntry(self.family_location_entry_frame2, width=450, font=self.large_font, state='disabled')

        self.family_location_confirm_button_2 = customtkinter.CTkButton(master=self.family_location_entry_frame2, text='Confirm', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.family_location_button2_confirm)
    
        # Family Location Question #3
        self.family_location_label3 = customtkinter.CTkLabel(self.family_location_frame, text="What is the maximum preferable travel distance from the location(s)?", font=self.large_font, fg_color=self.label_color)

        self.family_location_seg_button_3 = customtkinter.CTkSegmentedButton(self.family_location_frame, font=self.regular_font, command=self.seg_button_family_location3, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.family_location_seg_button_3.configure(values=["10 Miles", "20 Miles", "40 Miles", "60 Miles", "100 Miles", "200 Miles"])
        self.family_location_seg_button_3.set("40 Miles")

        # Initalize Family Location Seg Button #1 Command
        self.seg_button_family_location(param=self.family_location_seg_button_1.get())

        # Navigation Buttons
        family_location_next_button = customtkinter.CTkButton(master=self.family_location_frame, width=120, height=30, border_width=1, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_1_forward_event)
        family_location_next_button.grid(row=14, column=2, padx=20, pady=20, sticky="s")
        #  ------------------
        family_location_previous_button = customtkinter.CTkButton(master=self.family_location_frame, width=120, height=30, border_width=1, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_1_backward_event)
        family_location_previous_button.grid(row=14, column=0, padx=20, pady=20, sticky="sw")


    def build_family_details_frame_1b(self):
        self.family_details_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.family_details_frame.grid_rowconfigure((3,6,9,12,15), weight=1)
        self.family_details_frame.grid_columnconfigure(0, weight=1)

        family_details_title = customtkinter.CTkLabel(self.family_details_frame, text="Ideal Family Preferences", font=self.title_font, fg_color=self.label_color)
        family_details_title.grid(row=0, column=0, padx=20, columnspan=4, ipady=1, ipadx=20, pady=15, sticky='')

        # Family Details Question #1
        family_details_label1 = customtkinter.CTkLabel(self.family_details_frame, text="Are you married?", font=self.large_font, fg_color=self.label_color)
        family_details_label1.grid(row=1, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_1 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.family_details_seg_button_1.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.family_details_seg_button_1.configure(values=["Yes", "No"])
        self.family_details_seg_button_1.set("No")

        # Family Details Question #2
        family_details_label2 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to be nearby people with the same marital status as you?", font=self.large_font, fg_color=self.label_color)
        family_details_label2.grid(row=4, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_2 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.family_details_seg_button_2.grid(row=5, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.family_details_seg_button_2.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_2.set("3")

        # Family Details Question #3
        family_details_label3 = customtkinter.CTkLabel(self.family_details_frame, text="Do you have children?", font=self.large_font, fg_color=self.label_color)
        family_details_label3.grid(row=7, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_3 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.family_details_seg_button_3.grid(row=8, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.family_details_seg_button_3.configure(values=["Yes", "No"])
        self.family_details_seg_button_3.set("No")

        # Family Details Question #4
        family_details_label4 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to be nearby people with the same children status as you?", font=self.large_font, fg_color=self.label_color)
        family_details_label4.grid(row=10, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_4 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.family_details_seg_button_4.grid(row=11, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.family_details_seg_button_4.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_4.set("3")

        # Family Details Question #5
        family_details_label5 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to be in a high ranking school district?", font=self.large_font, fg_color=self.label_color)
        family_details_label5.grid(row=13, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_5 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.family_details_seg_button_5.grid(row=14, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.family_details_seg_button_5.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_5.set("3")

        # Navigation Buttons
        family_details_next_button = customtkinter.CTkButton(master=self.family_details_frame, width=120, height=30, border_width=1, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_1b_forward_event)
        family_details_next_button.grid(row=16, column=2, padx=20, pady=20, sticky="s")
        #  ------------------
        family_details_previous_button = customtkinter.CTkButton(master=self.family_details_frame, width=120, height=30, border_width=1, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_1b_backward_event)
        family_details_previous_button.grid(row=16, column=0, padx=20, pady=20, sticky="sw")
        

    def build_work_frame_2(self):
        self.work_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.work_frame.grid_rowconfigure((3,6,9,12), weight=1)
        self.work_frame.grid_columnconfigure(0, weight=1)

        work_title = customtkinter.CTkLabel(self.work_frame, text="Ideal Work Preferences", font=self.title_font, fg_color=self.label_color)
        work_title.grid(row=0, column=0, padx=20, columnspan=4, ipady=1, ipadx=20, pady=15, sticky='')

        # Work Question #1
        work_label_1 = customtkinter.CTkLabel(self.work_frame, text="Are you employed?", font=self.large_font, fg_color=self.label_color)
        work_label_1.grid(row=1, column=0, columnspan=3, pady=10, padx=20, sticky="")

        self.work_seg_button_1 = customtkinter.CTkSegmentedButton(self.work_frame, font=self.regular_font, command=self.seg_button_work_1, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.work_seg_button_1.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.work_seg_button_1.configure(values=["Yes", "No"])
        self.work_seg_button_1.set("No")

        # Work Question #2
        self.work_label2 = customtkinter.CTkLabel(self.work_frame, text="Do you want to be nearby your office?", font=self.large_font, fg_color=self.label_color)
        
        self.work_seg_button_2 = customtkinter.CTkSegmentedButton(self.work_frame, font=self.regular_font, command=self.seg_button_work_2, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.work_seg_button_2.configure(values=["Yes", "No"])
        self.work_seg_button_2.set("No")

        # Work Question #3
        self.work_label3 = customtkinter.CTkLabel(self.work_frame, text="How important is it to have nearby employment opportunities?", font=self.large_font, fg_color=self.label_color)

        self.work_seg_button_3 = customtkinter.CTkSegmentedButton(self.work_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.work_seg_button_3.configure(values=["1", "2", "3", "4", "5"])
        self.work_seg_button_3.set("3")

        # Work Location Entry Frame 1
        self.work_location_entry_frame1 = customtkinter.CTkFrame(self.work_frame, corner_radius=0, fg_color=('#d1d7e1',"gray22"))
        self.work_location_entry_frame1.grid_rowconfigure(10, weight=1)
        self.work_location_entry_frame1.grid_columnconfigure((0, 1, 2, 3), weight=1)

        work_location_entry_label_1 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="Please enter the location:", font=self.large_font, fg_color=self.label_color)
        work_location_entry_label_1.grid(row=0, column=0, columnspan=4, padx=40, pady=(10,5), sticky='')

        work_location_city_1 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="City:", font=self.large_font, fg_color=self.label_color)
        work_location_city_1.grid(row=1, column=0, padx=60, pady=5, sticky='n')

        work_location_state_1 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="State:", font=self.large_font, fg_color=self.label_color)
        work_location_state_1.grid(row=1, column=1, padx=40, pady=5, sticky='n')

        work_location_zipcode_1 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="Zipcode:", font=self.large_font, fg_color=self.label_color)
        work_location_zipcode_1.grid(row=1, column=2, padx=40, pady=5, sticky='n')

        self.work_location_entry1 = customtkinter.CTkEntry(self.work_location_entry_frame1, width=250, placeholder_text='City', font=self.large_font)
        self.work_location_entry1.grid(row=2, column=0, padx=40, pady=5, sticky='n')
        self.work_location_entry1.bind("<Return>", self.work_button_verify)

        self.work_location_entry2 = customtkinter.CTkEntry(self.work_location_entry_frame1, placeholder_text='State', font=self.large_font)
        self.work_location_entry2.grid(row=2, column=1, padx=40, pady=5, sticky='n')
        self.work_location_entry2.bind("<Return>", self.work_button_verify)

        self.work_location_entry3 = customtkinter.CTkEntry(self.work_location_entry_frame1, placeholder_text='Zipcode', font=self.large_font)
        self.work_location_entry3.grid(row=2, column=2, padx=40, pady=5, sticky='n')
        self.work_location_entry3.bind("<Return>", self.work_button_verify)

        # Verify Submission #1
        self.work_location_verify_button_1 = customtkinter.CTkButton(master=self.work_location_entry_frame1, width=120, height=30, border_width=1,text='Verify', text_color="#DCE4EE", font=self.regular_font, command=self.work_button_verify)
        self.work_location_verify_button_1.grid(row=2, column=3, padx=20, pady=(5,10), sticky="n")

        self.work_location_confirmation_output_1 = customtkinter.CTkEntry(self.work_location_entry_frame1, width=450, font=self.large_font, state='disabled')
        
        self.work_location_confirm_button_1 = customtkinter.CTkButton(master=self.work_location_entry_frame1, width=120, height=30, border_width=1, text='Confirm', text_color="#DCE4EE", font=self.regular_font, command=self.work_button_confirm)

        # Work Question #4
        self.work_label4 = customtkinter.CTkLabel(self.work_frame, text="What is the maximum preferable travel distance from the location(s)?", font=self.large_font, fg_color=self.label_color)
        
        self.work_seg_button_4 = customtkinter.CTkSegmentedButton(self.work_frame, font=self.regular_font, command=self.seg_button_work_3, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.work_seg_button_4.configure(values=["10 Miles", "20 Miles", "40 Miles", "60 Miles", "100 Miles", "200 Miles"])
        self.work_seg_button_4.set("40 Miles")
      
        # Work Question #5
        self.work_label5 = customtkinter.CTkLabel(self.work_frame, text="What's your ideal transportation method for commuting to work?", font=self.large_font, fg_color=self.label_color)

        self.work_seg_button_5 = customtkinter.CTkSegmentedButton(self.work_frame, command=self.seg_button_work_4, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.work_seg_button_5.configure(values=["Personal Vehicle", "Public Transportation", "Walking or Biking", "Work From Home"])
        self.work_seg_button_5.set("Personal Vehicle")

        # Work Question #6
        self.work_label6 = customtkinter.CTkLabel(self.work_frame, text="What is the maximum preferable commute time?", font=self.large_font, fg_color=self.label_color)

        self.work_seg_button_6 = customtkinter.CTkSegmentedButton(self.work_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.work_seg_button_6.configure(values=["Under 10 Minutes", "Under 20 Minutes", "Under 30 Minutes", "Under 40 Minutes", "Under 50 Minutes"])
        self.work_seg_button_6.set("Under 30 Minutes")

        # Initalize Work Seg Button #1 & #2 Command
        self.seg_button_work_1(param=self.work_seg_button_1.get())
        self.seg_button_work_2(param=self.work_seg_button_2.get())

        # Navigation Buttons
        work_next_button = customtkinter.CTkButton(master=self.work_frame, width=120, height=30, border_width=1, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_2_forward_event)
        work_next_button.grid(row=13, column=2, padx=20, pady=20, sticky="s")
        #  ------------------
        work_previous_button = customtkinter.CTkButton(master=self.work_frame, width=120, height=30, border_width=1, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_2_backward_event)
        work_previous_button.grid(row=13, column=0, padx=20, pady=20, sticky="sw")


    def build_income_frame_3(self):
        self.income_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.income_frame.grid_rowconfigure((3,6,9,12,15), weight=1)
        self.income_frame.grid_columnconfigure(0, weight=1)

        income_title = customtkinter.CTkLabel(self.income_frame, text="Income Information", font=self.title_font, fg_color=self.label_color)
        income_title.grid(row=0, column=0, padx=20, columnspan=3, ipady=1, ipadx=20, pady=15, sticky='')

        # Income Question #1
        income_label_1 = customtkinter.CTkLabel(self.income_frame, text="What's your annual household income?", font=self.large_font, fg_color=self.label_color)
        income_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Income Entry Frame #1
        self.income_entry_frame1 = customtkinter.CTkFrame(self.income_frame, corner_radius=0, fg_color=('#d1d7e1',"gray22"))
        self.income_entry_frame1.grid(row=2, column=0, columnspan=3, pady=10, padx=4, sticky="nsew")
        self.income_entry_frame1.grid_rowconfigure(0, weight=1)
        self.income_entry_frame1.grid_columnconfigure((0, 1), weight=1)

        self.income_entry1 = customtkinter.CTkEntry(self.income_entry_frame1, font=self.regular_font)
        self.income_entry1.grid(row=0, column=0, padx=40, pady=12, sticky='e')
        self.income_entry1.bind("<Return>", self.income_button_1)

        units = customtkinter.CTkLabel(self.income_entry_frame1, text="$", font=self.large_font)
        units.grid(row=0, column=0, padx=(0, 190), pady=12, sticky='e')

        self.income_submit_button1 = customtkinter.CTkButton(master=self.income_entry_frame1, text='Submit', text_color="#DCE4EE", font=self.regular_font, command=self.income_button_1)
        self.income_submit_button1.grid(row=0, column=1, padx=20, pady=12, sticky="w")

        # Income Question #2
        income_label_2 = customtkinter.CTkLabel(self.income_frame, text="Do you need to take out a mortgage? If so, what term length?", font=self.large_font, fg_color=self.label_color)
        income_label_2.grid(row=4, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.income_seg_button_1 = customtkinter.CTkSegmentedButton(self.income_frame, font=self.regular_font, command=self.seg_button_income, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.income_seg_button_1.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.income_seg_button_1.configure(values=["No Morgage", "15 Years", "30 Years"])
        self.income_seg_button_1.set("30 Years")

        # Income Question #3
        self.income_label3 = customtkinter.CTkLabel(self.income_frame, text="What interest rate do you have on your loan?", font=self.large_font, fg_color=self.label_color)
        self.income_label3.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            
        # Income Entry Frame #2
        self.income_entry_frame2 = customtkinter.CTkFrame(self.income_frame, corner_radius=0, fg_color=('#d1d7e1',"gray22"))
        self.income_entry_frame2.grid(row=8, column=0, columnspan=3, padx=4, pady=10, sticky="nsew")
        self.income_entry_frame2.grid_rowconfigure(0, weight=1)
        self.income_entry_frame2.grid_columnconfigure((0, 1), weight=1)

        self.income_entry2 = customtkinter.CTkEntry(self.income_entry_frame2, font=self.regular_font)
        self.income_entry2.grid(row=0, column=0, padx=40, pady=12, sticky='e')
        self.income_entry2.bind("<Return>", self.income_button_1)

        self.income_entry2_units = customtkinter.CTkLabel(self.income_entry_frame2, text="%", font=self.large_font)
        self.income_entry2_units.grid(row=0, column=0, padx=(0, 190), pady=12, sticky='e')

        self.income_submit_button2 = customtkinter.CTkButton(master=self.income_entry_frame2, text='Submit', text_color="#DCE4EE", font=self.regular_font, command=self.income_button_1)
        self.income_submit_button2.grid(row=0, column=1, padx=20, pady=12, sticky="w")

        # Income Question #4
        self.income_label4 = customtkinter.CTkLabel(self.income_frame, text="What percent of your income can you allocate to home expenses? (Mortgage, Tax, & Insurance)", font=self.large_font, fg_color=self.label_color)

        self.income_seg_button_2 = customtkinter.CTkSegmentedButton(self.income_frame, font=self.regular_font, command=self.income_button_1, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.income_seg_button_2.configure(values=["15%", "20%", "25%", "30%", "35%", "40%"])
        self.income_seg_button_2.set("30%")

        # Income Question #5
        self.income_label5 = customtkinter.CTkLabel(self.income_frame, text="Your affordable home price is $250,000. Do you want to increase or decrease?", font=self.large_bold, fg_color=self.label_color)

        self.income_seg_button_3 = customtkinter.CTkSegmentedButton(self.income_frame, font=self.regular_font, command=self.income_button_1, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.income_seg_button_3.configure(values=["-10%", "-5%", "No Change", "+5%", "+10%"])
        self.income_seg_button_3.set("No Change")

        # Navigation Buttons
        self.income_next_button = customtkinter.CTkButton(master=self.income_frame, width=120, height=30, border_width=1, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_3_forward_event)
        self.income_next_button.grid(row=16, column=2, padx=20, pady=20, sticky="s")
        #  ------------------
        self.income_previous_button = customtkinter.CTkButton(master=self.income_frame, width=120, height=30, border_width=1, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_3_backward_event)
        self.income_previous_button.grid(row=16, column=0, padx=20, pady=20, sticky="sw")

        # Initalize Income Seg Button #1 Command
        self.seg_button_income(param=self.income_seg_button_1.get())

  
    def build_area_classification_frame_4(self):
        self.area_classification_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.area_classification_frame.grid_rowconfigure((3, 6, 9, 12), weight=1)
        self.area_classification_frame.grid_columnconfigure(0, weight=1)

        area_classification_title = customtkinter.CTkLabel(self.area_classification_frame, text="Ideal Lifestyle Preferences", font=self.title_font, fg_color=self.label_color)
        area_classification_title.grid(row=0, column=0, padx=20, columnspan=3, ipady=1, ipadx=20, pady=15, sticky='')

        # Area Classification Question #1
        area_classification_label_1 = customtkinter.CTkLabel(self.area_classification_frame, text="What level of education do you have?", font=self.large_font, fg_color=self.label_color)
        area_classification_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.area_classification_seg_button_1 = customtkinter.CTkSegmentedButton(self.area_classification_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.area_classification_seg_button_1.grid(row=2, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.area_classification_seg_button_1.configure(values=["Less than High School", "High School", "Associate's", "Bachelor's", "Master's", "Doctorate"])
        self.area_classification_seg_button_1.set("High School")

        # Area Classification Question #2
        area_classification_label_2 = customtkinter.CTkLabel(self.area_classification_frame, text="How important is it to be around people with the same education level as you?", font=self.large_font, fg_color=self.label_color)
        area_classification_label_2.grid(row=4, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.area_classification_seg_button_2 = customtkinter.CTkSegmentedButton(self.area_classification_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.area_classification_seg_button_2.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.area_classification_seg_button_2.configure(values=["1", "2", "3", "4", "5"])
        self.area_classification_seg_button_2.set("3")

        # Area Classification Question #3
        area_classification_label_3 = customtkinter.CTkLabel(self.area_classification_frame, text="What kind of living environment is the most preferable?", font=self.large_font, fg_color=self.label_color)
        area_classification_label_3.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.area_classification_list = ["Hyper Rural", "Rural", "Suburban", "Urban", "Hyper Urban"]
        self.area_classification_seg_button_3 = customtkinter.CTkSegmentedButton(self.area_classification_frame, font=self.regular_font, command=self.seg_button_area_classification_3, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.area_classification_seg_button_3.grid(row=8, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.area_classification_seg_button_3.configure(values=self.area_classification_list)
        self.area_classification_seg_button_3.set("Suburban")

        # Area Classification Question #4
        area_classification_label_4 = customtkinter.CTkLabel(self.area_classification_frame, text="What kind of living environment is second most preferable?", font=self.large_font, fg_color=self.label_color)
        area_classification_label_4.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.area_classification_seg_button_4 = customtkinter.CTkSegmentedButton(self.area_classification_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)

        # Initalize Area Classification Seg Button #3 Command
        self.seg_button_area_classification_3(param=self.area_classification_seg_button_3.get())

        # Navigation Buttons
        area_classification_next_button = customtkinter.CTkButton(master=self.area_classification_frame, width=120, height=30, border_width=1, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_4_forward_event)
        area_classification_next_button.grid(row=13, column=2, padx=20, pady=20, sticky="s")
        #  ------------------
        area_classification_previous_button = customtkinter.CTkButton(master=self.area_classification_frame, width=120, height=30, border_width=1, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_4_backward_event)
        area_classification_previous_button.grid(row=13, column=0, padx=20, pady=20, sticky="sw")

    
    def build_weather_frame_5(self):
        self.weather_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.weather_frame.grid_rowconfigure((3,6,9,12,15,18), weight=1)
        self.weather_frame.grid_columnconfigure(0, weight=1)

        weather_title = customtkinter.CTkLabel(self.weather_frame, text="Weather & Temperature Preferences", font=self.title_font, fg_color=self.label_color)
        weather_title.grid(row=0, column=0, padx=20, columnspan=3, ipady=1, ipadx=20, pady=15, sticky='')

        # Weather Question #1
        weather_label_1 = customtkinter.CTkLabel(self.weather_frame, text="What type of weather seasonality is preferable?", font=self.large_font, fg_color=self.label_color)
        weather_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.weather_seg_button_1 = customtkinter.CTkSegmentedButton(self.weather_frame, font=self.regular_font, command=self.seg_button_weather_1, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.weather_seg_button_1.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.weather_seg_button_1.configure(values=["1 Season", "2 Seasons", "4 Seasons"])
        self.weather_seg_button_1.set("4 Seasons")
        # --------------------------------------------
        # Weather Question #2
        self.weather_label2 = customtkinter.CTkLabel(self.weather_frame, text="What's your ideal summer temperature?", font=self.large_font, fg_color=self.label_color)
        self.weather_label2.grid(row=4, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.weather_entry_frame1 = customtkinter.CTkFrame(self.weather_frame, corner_radius=0, fg_color=('#d1d7e1',"gray22"))
        self.weather_entry_frame1.grid(row=5, column=0, columnspan=3, padx=4, pady=10, sticky="nsew")
        self.weather_entry_frame1.grid_rowconfigure(0, weight=1)
        self.weather_entry_frame1.grid_columnconfigure((0, 1), weight=1)

        units = customtkinter.CTkLabel(self.weather_entry_frame1, text="°F", font=self.large_font)
        units.grid(row=0, column=0, padx=(150, 0), pady=12, sticky='e')

        self.weather_entry1 = customtkinter.CTkEntry(self.weather_entry_frame1, font=self.large_font)
        self.weather_entry1.grid(row=0, column=0, padx=40, pady=12, sticky='e')
        self.weather_entry1.bind("<Return>", self.weather_button_1)

        weather_submit_button1 = customtkinter.CTkButton(master=self.weather_entry_frame1, text='Submit', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.weather_button_1)
        weather_submit_button1.grid(row=0, column=1, padx=20, pady=12, sticky="w")
        # --------------------------------------------
        # Weather Question #3
        self.weather_label4 = customtkinter.CTkLabel(self.weather_frame, text="What's your ideal winter temperature?", font=self.large_font, fg_color=self.label_color)

        self.weather_entry_frame2 = customtkinter.CTkFrame(self.weather_frame, corner_radius=0, fg_color=('#d1d7e1',"gray22"))
        self.weather_entry_frame2.grid_rowconfigure(0, weight=1)
        self.weather_entry_frame2.grid_columnconfigure((0, 1), weight=1)

        units = customtkinter.CTkLabel(self.weather_entry_frame2, text="°F", font=self.large_font)
        units.grid(row=0, column=0, padx=(150, 0), pady=12, sticky='e')

        self.weather_entry2 = customtkinter.CTkEntry(self.weather_entry_frame2, font=self.large_font)
        self.weather_entry2.grid(row=0, column=0, padx=40, pady=12, sticky='e')
        self.weather_entry2.bind("<Return>", self.weather_button_1)

        weather_submit_button2 = customtkinter.CTkButton(master=self.weather_entry_frame2, text='Submit', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.weather_button_1)
        weather_submit_button2.grid(row=0, column=1, padx=20, pady=12, sticky="w")
        # --------------------------------------------
        # Weather Question #4
        self.weather_label5 = customtkinter.CTkLabel(self.weather_frame, text="What level of precipitation is most ideal?", font=self.large_font, fg_color=self.label_color)
        self.weather_label5.grid(row=13, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.weather_seg_button_2 = customtkinter.CTkSegmentedButton(self.weather_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.weather_seg_button_2.grid(row=14, column=0, columnspan=3, padx=(20, 10), pady=10, sticky="ew")
        self.weather_seg_button_2.configure(values=["Very Low", "Low", "Average", "High", "Very High"])
        self.weather_seg_button_2.set("Average")
        # --------------------------------------------
        # Weather Question #5
        self.weather_label6 = customtkinter.CTkLabel(self.weather_frame, text="What level of sunshine is most ideal?", font=self.large_font, fg_color=self.label_color)
        self.weather_label6.grid(row=16, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.weather_seg_button_3 = customtkinter.CTkSegmentedButton(self.weather_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.weather_seg_button_3.grid(row=17, column=0, columnspan=3, padx=(20, 10), pady=10, sticky="ew")
        self.weather_seg_button_3.configure(values=["Very Low", "Low", "Average", "High", "Very High"])
        self.weather_seg_button_3.set("Average")

        # Navigation Buttons
        self.weather_next_button = customtkinter.CTkButton(master=self.weather_frame, text='Next', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.frame_5_forward_event)
        self.weather_next_button.grid(row=19, column=2, padx=20, pady=20, sticky="s")
        #  ------------------
        self.weather_previous_button = customtkinter.CTkButton(master=self.weather_frame, text='Previous', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.frame_5_backward_event)
        self.weather_previous_button.grid(row=19, column=0, padx=20, pady=20, sticky="sw")

        # Initalize Weather Seg Button #1 Command
        self.seg_button_weather_1(param=self.weather_seg_button_1.get())
        
  
    def build_natural_disaster_frame_6(self):
        self.natural_disaster_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.natural_disaster_frame.grid_rowconfigure((3,6,9,12), weight=1)
        self.natural_disaster_frame.grid_columnconfigure(0, weight=1)

        natural_disaster_title = customtkinter.CTkLabel(self.natural_disaster_frame, text="Natural Disaster Risk Tolerance", font=self.title_font, fg_color=self.label_color)
        natural_disaster_title.grid(row=0, column=0, padx=20, columnspan=3, ipady=1, ipadx=20, pady=15, sticky='')

        # Natural Disaster Question #1
        natural_disaster_label_1 = customtkinter.CTkLabel(self.natural_disaster_frame, text="How important is it to mitigate natural disaster risk?", font=self.large_font, fg_color=self.label_color)
        natural_disaster_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.natural_disaster_seg_button_1 = customtkinter.CTkSegmentedButton(self.natural_disaster_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.natural_disaster_seg_button_1.grid(row=2, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.natural_disaster_seg_button_1.configure(values=["1", "2", "3", "4", "5"])
        self.natural_disaster_seg_button_1.set("3")

        # Natural Disaster Question #2
        natural_disaster_label_2 = customtkinter.CTkLabel(self.natural_disaster_frame, text="Which natural disaster is the most important to avoid?", font=self.large_font, fg_color=self.label_color)
        natural_disaster_label_2.grid(row=4, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.natural_disaster_list = ["Hurricane", "Tornado", "Thunderstorm", "Earthquake", "Wildfire", "Flood"]
        self.natural_disaster_seg_button_2 = customtkinter.CTkSegmentedButton(self.natural_disaster_frame, font=self.regular_font, command=self.seg_button_natural_disaster_2, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        self.natural_disaster_seg_button_2.grid(row=5, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.natural_disaster_seg_button_2.configure(values=self.natural_disaster_list)
        self.natural_disaster_seg_button_2.set("Tornado")
        
        # Natural Disaster Question #3
        natural_disaster_label_3 = customtkinter.CTkLabel(self.natural_disaster_frame, text="Which natural disaster is the second most important to avoid?", font=self.large_font, fg_color=self.label_color)
        natural_disaster_label_3.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.natural_disaster_seg_button_3 = customtkinter.CTkSegmentedButton(self.natural_disaster_frame, font=self.regular_font, command=self.seg_button_natural_disaster_3, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)
        # --------------------------------------------
        # Natural Disaster Question #4
        natural_disaster_label_4 = customtkinter.CTkLabel(self.natural_disaster_frame, text="Which natural disaster is the third most important to avoid?", font=self.large_font, fg_color=self.label_color)
        natural_disaster_label_4.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            
        self.natural_disaster_seg_button_4 = customtkinter.CTkSegmentedButton(self.natural_disaster_frame, font=self.regular_font, fg_color=self.seg_button_unselected, unselected_color=self.seg_button_unselected, unselected_hover_color=self.seg_button_unselected_hover)

        # Initalize Natural Disaster Seg Button #2 Command
        self.seg_button_natural_disaster_2(param=self.natural_disaster_seg_button_2.get())

        # Navigation Buttons
        natural_disaster_next_button = customtkinter.CTkButton(master=self.natural_disaster_frame, width=120, height=30, border_width=1, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_6_forward_event)
        natural_disaster_next_button.grid(row=13, column=2, padx=20, pady=20, sticky="s")
        #  ------------------
        natural_disaster_previous_button = customtkinter.CTkButton(master=self.natural_disaster_frame, width=120, height=30, border_width=1, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_6_backward_event)
        natural_disaster_previous_button.grid(row=13, column=0, padx=20, pady=20, sticky="sw")


    def build_results_frame_7(self):
        self.results_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e1e5eb',"gray17"), border_width=1, border_color=('#217bd7','#1b66b3'))
        self.results_frame.grid_rowconfigure(10, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)

        results_title = customtkinter.CTkLabel(self.results_frame, text="Congratulations!", font=self.title_font, fg_color=self.label_color)
        results_title.grid(row=0, column=0, padx=20, columnspan=3, ipady=1, ipadx=20, pady=15, sticky='')

        # Results City Match
        self.results_label_1 = customtkinter.CTkLabel(self.results_frame, text="You have a 100% Match with City Name", font=self.large_bold, fg_color=self.label_color)
        self.results_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Results Region
        self.results_label_2 = customtkinter.CTkLabel(self.results_frame, text="It's recommended to look for a home in the greater Area.", font=self.large_font, fg_color=self.label_color)
        self.results_label_2.grid(row=2, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Navigation Buttons
        results_previous_button = customtkinter.CTkButton(master=self.results_frame, text='Previous', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.frame_7_backward_event)
        results_previous_button.grid(row=11, column=0, padx=20, pady=20, sticky="sw")
        # ------------------
        results_restart_button = customtkinter.CTkButton(master=self.results_frame, text='Restart', width=120, height=30, border_width=1, text_color="#DCE4EE", font=self.regular_font, command=self.frame_7_restart_event)
        results_restart_button.grid(row=11, column=2, padx=20, pady=20, sticky="sw")

    # ---------------------------- Buttons ----------------------------

    def family_location_button1_verify(self, return_bind_empty_param: str = ''):
        self.family_location_entry_frame1.focus()

        city = self.family_location_entry1.get()
        state = self.family_location_entry2.get()
        zipcode = self.family_location_entry3.get()

        result = self.IdealHomeDataAnalysis.city_name_zipcode_matcher(state=state,city=city,zipcode=zipcode,index=0)

        if result != self.family_location_confirmation_output_1.get():
            self.family_location_confirmation_output_1.configure(border_width=0)
            self.family_location_valid1 = False

        str_obj = StringVar(self.family_location_confirmation_output_1, result)
        self.family_location_confirmation_output_1.configure(textvariable=str_obj)
        self.family_location_confirmation_output_1.grid(row=3, column=0, columnspan=2, padx=40, pady=(10,15), sticky='e')

        if result not in ['Provide State','Provide City or Zipcode','Please Provide Valid US State','Please Provide Valid Zipcode']:
            self.family_location_confirm_button_1.grid(row=3, column=2, padx=20, pady=(10,15), sticky="")
        else:
            self.family_location_confirm_button_1.grid_forget()

    def family_location_button2_verify(self, return_bind_empty_param: str = ''):
        self.family_location_entry_frame2.focus()

        city = self.family_location_entry4.get()
        state = self.family_location_entry5.get()
        zipcode = self.family_location_entry6.get()

        result = self.IdealHomeDataAnalysis.city_name_zipcode_matcher(state=state,city=city,zipcode=zipcode,index=1)

        if result != self.family_location_confirmation_output_2.get():
            self.family_location_confirmation_output_2.configure(border_width=0)
            self.family_location_valid2 = False
    
        str_obj = StringVar(self.family_location_confirmation_output_2, result)
        self.family_location_confirmation_output_2.configure(textvariable=str_obj)
        self.family_location_confirmation_output_2.grid(row=3, column=0, columnspan=2, padx=40, pady=(10,15), sticky='e')

        if result not in ['Provide State','Provide City or Zipcode','Please Provide Valid US State','Please Provide Valid Zipcode']:
            self.family_location_confirm_button_2.grid(row=3, column=2, padx=20, pady=(10,15), sticky="")
        else:
            self.family_location_confirm_button_2.grid_forget()
            
    def family_location_button1_confirm(self):
        self.family_location_valid1 = True
        self.family_location_confirmation_output_1.configure(border_width=2, border_color='green')
        self.update_center_distance_label()

    def family_location_button2_confirm(self):
        self.family_location_valid2 = True
        self.family_location_confirmation_output_2.configure(border_width=2, border_color='green')
        self.update_center_distance_label()

    def work_button_verify(self, return_bind_empty_param: str = ''):
        self.work_location_entry_frame1.focus()

        city = self.work_location_entry1.get()
        state = self.work_location_entry2.get()
        zipcode = self.work_location_entry3.get()

        result = self.IdealHomeDataAnalysis.city_name_zipcode_matcher(state=state,city=city,zipcode=zipcode,index=2)

        if result != self.work_location_confirmation_output_1.get():
            self.work_location_confirmation_output_1.configure(border_width=0)
            self.work_valid1 = False

        str_obj = StringVar(self.work_location_confirmation_output_1, result)
        self.work_location_confirmation_output_1.configure(textvariable=str_obj)
        self.work_location_confirmation_output_1.grid(row=3, column=0, columnspan=2, padx=40, pady=(10,15), sticky='e')

        if result not in ['Provide State','Provide City or Zipcode','Please Provide Valid US State','Please Provide Valid Zipcode']:
            self.work_location_confirm_button_1.grid(row=3, column=2, padx=20, pady=(10,15), sticky="")
        else:
            self.work_location_confirm_button_1.grid_forget()

    def work_button_confirm(self):
        self.work_valid1 = True
        self.work_location_confirmation_output_1.configure(border_width=2, border_color='green')
        self.update_center_distance_label()

    def income_button_1(self, return_bind_empty_param: str = ''):
        self.income_frame.focus()

        income_entry_value1 = self.income_entry1.get()
        income_entry_value2 = self.income_entry2.get()
        morgage_param = self.income_seg_button_1.get()

        try:
            income_entry_float1 = float(income_entry_value1.replace(',',''))
        except:
            income_entry_float1 = -1
        try:
            income_entry_float2 = float(income_entry_value2.replace(',',''))
        except:
            income_entry_float2 = -1

        if income_entry_value1 and 0 < income_entry_float1 <= 10_000_000:
            self.income_entry1.configure(border_color='green', border_width=2)
            self.income_entry1_valid = True
        elif income_entry_value1 and (income_entry_float1 <= 0 or income_entry_float1 > 10_000_000):
            self.income_entry1.configure(border_color='red', border_width=2)
            self.income_entry1_valid = False
        else:
            self.income_entry1.configure(border_width=0)
            self.income_entry1_valid = False
            
        if income_entry_value2 and morgage_param != 'No Morgage' and 0 < income_entry_float2 < 90:
            self.income_entry2.configure(border_color='green', border_width=2)
            self.income_entry2_valid = True
        elif income_entry_value2 and morgage_param != 'No Morgage' and (income_entry_float2 <= 0 or income_entry_float2 >= 90):
            self.income_entry2.configure(border_color='red', border_width=2)
            self.income_entry2_valid = False
        elif income_entry_value2 and morgage_param == 'No Morgage' and 0 < income_entry_float2 <= 10_000_000:
            self.income_entry2.configure(border_color='green', border_width=2)
            self.income_entry2_valid = True
            self.affordable_home_price = income_entry_float2
        elif income_entry_value2 and morgage_param == 'No Morgage' and (income_entry_float2 <= 0 or income_entry_float2 > 10_000_000):
            self.income_entry2.configure(border_color='red', border_width=2)
            self.income_entry2_valid = False
        else:
            self.income_entry2.configure(border_width=0)
            self.income_entry2_valid = False

        if self.income_entry1_valid and self.income_entry2_valid and morgage_param != 'No Morgage':
            self.affordable_home_price = self.IdealHomeDataAnalysis.calculate_affordable_home_price(income=income_entry_float1,
                percent_income_allocated=self.income_seg_button_2.get(),
                interest_rate=income_entry_float2,
                mortgage_term=self.income_seg_button_1.get(),
                adjustments=self.income_seg_button_3.get())

            affordable_home_price_label = ''.join(reversed([digit + ',' if index % 3 == 0 and index != 0 else digit for index, digit in enumerate(reversed(str(self.affordable_home_price)))]))
            
            self.income_label5.configure(text=f"Your affordable home price is ${affordable_home_price_label}. Do you want to increase or decrease?")
            self.income_label5.grid(row=13, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.income_seg_button_3.grid(row=14, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

    def weather_button_1(self, return_bind_empty_param: str = ''):
        self.weather_frame.focus()

        self.total_weather_entry_valid = False
        weather_entry1_valid = False
        weather_entry2_valid = False

        weather_entry_value1 = self.weather_entry1.get()
        weather_entry_value2 = self.weather_entry2.get()
        seasons_param = self.weather_seg_button_1.get()
        
        try:
            weather_entry_float1 = float(weather_entry_value1)
        except:
            weather_entry_float1 = -100
        try:
            weather_entry_float2 = float(weather_entry_value2)
        except:
            weather_entry_float2 = -100

        if weather_entry_value1 and -40 < weather_entry_float1 <= 100:
            self.weather_entry1.configure(border_color='green', border_width=2)
            weather_entry1_valid = True
        elif weather_entry_value1 and (weather_entry_float1 <= -40 or weather_entry_float1 > 100):
            self.weather_entry1.configure(border_color='red', border_width=2)
            weather_entry1_valid = False

        if weather_entry_value2 and -40 < weather_entry_float2 <= 100 and weather_entry_float2 < weather_entry_float1:
            self.weather_entry2.configure(border_color='green', border_width=2)
            weather_entry2_valid = True
        elif weather_entry_value2 and (weather_entry_float2 <= -40 or weather_entry_float2 > 100 or weather_entry_float2 >= weather_entry_float1):
            self.weather_entry2.configure(border_color='red', border_width=2)
            weather_entry2_valid = False

        if (seasons_param == '4 Seasons' or seasons_param == '2 Seasons') and weather_entry1_valid and weather_entry2_valid:
            self.total_weather_entry_valid = True
        elif seasons_param == '1 Season' and weather_entry1_valid:
            self.total_weather_entry_valid = True
        else:
            self.total_weather_entry_valid = False

    # ---------------------------- Segmented Buttons ----------------------------

    def seg_button_family_location(self, param: str):
        if param == "Yes":
            self.family_location_entry_frame1.grid(row=4, column=0, columnspan=3, padx=4, pady=10, sticky="nsew")
            self.family_location_label2.grid(row=6, column=0, columnspan=3, pady=10, padx=20, sticky="")
            self.family_location_seg_button_2.grid(row=7, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
            self.seg_button_family_location_2(param=self.family_location_seg_button_2.get())
        else:
            self.family_location_entry_frame1.grid_forget()
            self.family_location_label2.grid_forget()
            self.family_location_label3.grid_forget()
            self.family_location_seg_button_2.grid_forget()
            self.family_location_seg_button_3.grid_forget()
            self.family_location_seg_button_2.set("No")
            self.seg_button_family_location_2(param='No')
            # Clear Saved Location
            self.family_location_confirmation_output_1.configure(border_width=0)
            self.family_location_valid1 = False
            self.IdealHomeDataAnalysis.saved_coordinates_list[0] = []

    def seg_button_family_location_2(self, param: str):
        if param == "Yes":
            self.family_location_entry_frame2.grid(row=9, column=0, columnspan=3, padx=4, pady=10, sticky="nsew")
            self.family_location_frame.grid_rowconfigure(10, weight=1)
            self.family_location_label3.grid(row=11, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')
            self.family_location_seg_button_3.grid(row=12, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        else:
            self.family_location_entry_frame2.grid_forget()
            if self.family_location_seg_button_1.get() == 'Yes':
                self.family_location_frame.grid_rowconfigure(10, weight=0)
                self.family_location_label3.grid(row=9, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')
                self.family_location_seg_button_3.grid(row=10, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
            # Clear Saved Location
            self.family_location_confirmation_output_2.configure(border_width=0)
            self.family_location_valid2 = False
            self.IdealHomeDataAnalysis.saved_coordinates_list[1] = [] 

    def seg_button_family_location3(self, param: str):
        self.work_seg_button_4.set(param)
        location_options = self.family_location_seg_button_3.cget('values')
        self.radius_index = location_options.index(param)

    def seg_button_work_1(self, param: str):
        if param == 'Yes':
            self.work_frame.grid_rowconfigure((7,10), weight=1)
            self.work_frame.grid_rowconfigure((6,9), weight=0)
            self.work_label2.grid(row=4, column=0, columnspan=3, pady=10, padx=20, sticky="")
            self.work_seg_button_2.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
            self.work_label3.grid_forget()
            self.work_seg_button_3.grid_forget()
            self.work_label5.grid_forget()
            self.work_seg_button_5.grid_forget()
            self.work_label6.grid_forget()
            self.work_seg_button_6.grid_forget()
            self.seg_button_work_2(param=self.work_seg_button_2.get())
        else:
            self.work_frame.grid_rowconfigure((6,9), weight=1)
            self.work_frame.grid_rowconfigure((7,10), weight=0)
            self.work_label5.grid(row=7, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')
            self.work_seg_button_5.grid(row=8, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
            self.work_label3.grid(row=4, column=0, columnspan=3, pady=10, padx=20, sticky="")
            self.work_seg_button_3.grid(row=5, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
            self.work_label2.grid_forget()
            self.work_seg_button_2.grid_forget()
            self.seg_button_work_2(param='No')
            self.seg_button_work_4(param=self.work_seg_button_5.get())

    def seg_button_work_2(self, param: str):
        if param == 'Yes':
            self.work_location_entry_frame1.grid(row=6, column=0, columnspan=3, padx=4, pady=10, sticky="nsew")
            self.work_label4.grid(row=8, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')
            self.work_seg_button_4.grid(row=9, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        else:
            self.work_location_entry_frame1.grid_forget()
            self.work_label4.grid_forget()
            self.work_seg_button_4.grid_forget()
            # Clear Saved Location
            self.work_location_confirmation_output_1.configure(border_width=0)
            self.work_valid1 = False
            self.IdealHomeDataAnalysis.saved_coordinates_list[2] = []

    def seg_button_work_3(self, param: str):
        self.family_location_seg_button_3.set(param)
        location_options = self.work_seg_button_4.cget('values')
        self.radius_index = location_options.index(param)

    def seg_button_work_4(self, param: str):
        if param == 'Work From Home':
            self.work_label6.grid_forget()
            self.work_seg_button_6.grid_forget()
        else:
            self.work_label6.grid(row=10, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')
            self.work_seg_button_6.grid(row=11, column=0, columnspan=4, padx=20, pady=10, sticky="ew")

    def seg_button_income(self, param: str):
        if param == '30 Years' or param == '15 Years':
            self.income_label3.configure(text="What interest rate do you have on your loan?")
            self.income_entry2_units.configure(text="%")
            self.income_label4.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.income_seg_button_2.grid(row=11, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
            if self.income_entry1_valid and self.income_entry2_valid:
                self.income_label5.grid(row=13, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
                self.income_seg_button_3.grid(row=14, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        else:
            self.income_label3.configure(text="What's your ideal home price?")
            self.income_entry2_units.configure(text="$")
            self.income_entry2.configure(textvariable=StringVar(self.income_entry2, ''))
            self.income_label4.grid_forget()
            self.income_seg_button_2.grid_forget()
            self.income_label5.grid_forget()
            self.income_seg_button_3.grid_forget()
        self.income_button_1()

    def seg_button_weather_1(self, param: str):
        if param == "4 Seasons" or param == "2 Seasons":
            self.weather_label2.configure(text="What's your ideal summer temperature?")

            self.weather_frame.grid_rowconfigure((15,18), weight=1)
            self.weather_label4.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_entry_frame2.grid(row=11, column=0, columnspan=3, padx=4, pady=10, sticky="nsew")
            self.weather_label5.grid(row=13, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_2.grid(row=14, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
            self.weather_label6.grid(row=16, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_3.grid(row=17, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
            self.weather_next_button.grid(row=19, column=2, padx=20, pady=20, sticky="s")
            self.weather_previous_button.grid(row=19, column=0, padx=20, pady=20, sticky="sw")
        else:
            self.weather_label2.configure(text="What's your ideal outside temperature?")

            self.weather_frame.grid_rowconfigure((15, 18), weight=0)
            self.weather_label5.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_2.grid(row=8, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
            self.weather_label6.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_3.grid(row=11, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
            self.weather_next_button.grid(row=13, column=2, padx=20, pady=20, sticky="s")
            self.weather_previous_button.grid(row=13, column=0, padx=20, pady=20, sticky="sw")
            self.weather_label4.grid_forget()
            self.weather_entry_frame2.grid_forget()
          

    def seg_button_area_classification_3(self, param: str):
        area_classification_list = [*self.area_classification_list]
        area_classification_list.remove(param)

        # Segmented Button #3
        self.area_classification_seg_button_4.grid(row=11, column=0, columnspan=3, padx=20, pady=10, sticky="ew")
        self.area_classification_seg_button_4.configure(values=area_classification_list)
        self.area_classification_seg_button_4.set(area_classification_list[0])

    def seg_button_natural_disaster_2(self, param: str):
        self.natural_disaster_list_2 = [*self.natural_disaster_list]
        self.natural_disaster_list_2.remove(param)
        current_value = self.natural_disaster_seg_button_3.get()
        if not current_value or current_value == param:
            current_value = self.natural_disaster_list_2[0]

        # Segmented Button #3
        self.natural_disaster_seg_button_3.grid(row=8, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.natural_disaster_seg_button_3.configure(values=self.natural_disaster_list_2)
        self.natural_disaster_seg_button_3.set(current_value)
        self.seg_button_natural_disaster_3(param=current_value)

    def seg_button_natural_disaster_3(self, param: str):
        natural_disaster_list = [*self.natural_disaster_list_2]
        natural_disaster_list.remove(param)
        current_value = self.natural_disaster_seg_button_4.get()
        if not current_value or current_value == param or current_value == self.natural_disaster_seg_button_2.get():
            current_value = natural_disaster_list[0]

        # Segmented Button #4
        self.natural_disaster_seg_button_4.grid(row=11, column=0, columnspan=4, padx=20, pady=10, sticky="ew")
        self.natural_disaster_seg_button_4.configure(values=natural_disaster_list)
        self.natural_disaster_seg_button_4.set(current_value)

    # ---------------------------- Navigation Buttons ----------------------------

    def instruction_button_event(self):
        self.intro_frame.grid_forget()
        if not self.family_location_frame:
            self.build_family_location_frame_1()
        self.family_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.125)

    # FRAME 1
    def frame_1_forward_event(self):
        if self.check_frame1_progress():
            self.IdealHomeDataAnalysis.family_location_frame_1(radius_index=self.radius_index)
            if self.IdealHomeDataAnalysis.errors:
                messagebox.showerror('Search Results Error', self.IdealHomeDataAnalysis.errors[0])
            else:
                self.IdealHomeDataAnalysis.errors = []
                self.family_location_frame.grid_forget()
                if not self.family_details_frame:
                    self.build_family_details_frame_1b()
                self.family_details_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
                self.progressbar.set(.25)
        else:
            self.error_message(message_type='Segmented_Button')

    def frame_1_backward_event(self):
        self.family_location_frame.grid_forget()
        self.intro_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(0)

    # FRAME 1b
    def frame_1b_forward_event(self):
        self.family_details_frame.grid_forget()
        if not self.work_frame:
            self.build_work_frame_2()
        self.work_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.375)
        self.IdealHomeDataAnalysis.family_details_frame_1b(married=self.family_details_seg_button_1.get(),
            married_importance=self.family_details_seg_button_2.get(),
            children=self.family_details_seg_button_3.get(),
            children_importance=self.family_details_seg_button_4.get(),
            school_enrollment_importance=self.family_details_seg_button_5.get()
        )

    def frame_1b_backward_event(self):
        self.family_details_frame.grid_forget()
        self.family_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.125)

    # FRAME 2
    def frame_2_forward_event(self):
        if self.check_frame2_progress():
            self.IdealHomeDataAnalysis.work_frame_2(employed_status=self.work_seg_button_1.get(),
                radius_index=self.radius_index,
                regional_employment_importance=self.work_seg_button_3.get(),
                work_transportation=self.work_seg_button_5.get(),
                commute_time=self.work_seg_button_6.get()
            )
            if self.IdealHomeDataAnalysis.errors:
                messagebox.showerror('Search Results Error', self.IdealHomeDataAnalysis.errors[0])
            else:
                self.IdealHomeDataAnalysis.errors = []
                self.work_frame.grid_forget()
                if not self.income_frame:
                    self.build_income_frame_3()
                self.income_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
                self.progressbar.set(.5)
        else:
            self.error_message(message_type='Segmented_Button')
 
    def frame_2_backward_event(self):
        self.work_frame.grid_forget()
        self.family_details_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.25)

    # FRAME 3
    def frame_3_forward_event(self):
        self.income_button_1()
        if self.income_entry1_valid and self.income_entry2_valid:
            self.income_frame.grid_forget()
            if not self.area_classification_frame:
                self.build_area_classification_frame_4()
            self.area_classification_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.625)
            self.IdealHomeDataAnalysis.income_frame_3(
                income=self.income_entry1.get(),
                affordable_home_price=self.affordable_home_price
            )
        else:
            self.error_message()

    def frame_3_backward_event(self):
        self.income_frame.grid_forget()
        self.work_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.375)

    # FRAME 4
    def frame_4_forward_event(self):
        self.area_classification_frame.grid_forget()
        if not self.weather_frame:
            self.build_weather_frame_5()
        self.weather_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.75)
        self.IdealHomeDataAnalysis.area_classification_frame_4(education_level=self.area_classification_seg_button_1.get(),
            education_level_importance=self.area_classification_seg_button_2.get(),
            living_enviornment=self.area_classification_seg_button_3.get(),
            living_enviornment2=self.area_classification_seg_button_4.get()
        )

    def frame_4_backward_event(self):
        self.area_classification_frame.grid_forget()
        self.income_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.5)

    # FRAME 5
    def frame_5_forward_event(self):
        self.weather_button_1()
        if self.total_weather_entry_valid:
            self.weather_frame.grid_forget()
            if not self.natural_disaster_frame:
                self.build_natural_disaster_frame_6()
            self.natural_disaster_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.875)
            self.IdealHomeDataAnalysis.weather_frame_5(seasons=self.weather_seg_button_1.get(),
                summer_temperature=self.weather_entry1.get(),
                winter_temperature=self.weather_entry2.get(),
                precipitation_level=self.weather_seg_button_2.get(),
                sunshine_level=self.weather_seg_button_3.get()
            )
        else:
            self.error_message()

    def frame_5_backward_event(self):
        self.weather_frame.grid_forget()
        self.area_classification_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.625)

    # FRAME 6
    def frame_6_forward_event(self):
        self.natural_disaster_frame.grid_forget()
        if not self.results_frame:
            self.build_results_frame_7()
        self.IdealHomeDataAnalysis.natural_disaster_risk_frame_6(natural_disaster_risk=self.natural_disaster_seg_button_1.get(),
            disaster_to_avoid=self.natural_disaster_seg_button_2.get(),
            disaster_to_avoid2=self.natural_disaster_seg_button_3.get(),
            disaster_to_avoid3=self.natural_disaster_seg_button_4.get()
        )
        self.final_results = self.IdealHomeDataAnalysis.results_frame_7()
        self.city_name = self.final_results['Result_City']
        self.city_coordinates = self.final_results['Result_City_Coordinates']
        self.zipcode_prefix_boundary = self.final_results['Zipcode_Prefix_Boundary']
        self.results_label_1.configure(text=f"You have a {self.final_results['Match_Percentage']}% Match with {self.city_name}")
        self.results_label_2.configure(text=f"It's recommended to look for a home in the greater {self.final_results['Region_Name']} Area.")
        self.set_map_position()
        self.after(100, self.set_map_results)
        self.results_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(1)
        if  self.final_results['Afforability_Warning']:
            self.error_message('Afforability_Warning')

    def frame_6_backward_event(self):
        self.natural_disaster_frame.grid_forget()
        self.weather_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.75)

    # FRAME 7
    def frame_7_backward_event(self):
        self.results_frame.grid_forget()
        self.natural_disaster_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.875)

    def frame_7_restart_event(self):
        self.results_frame.grid_forget()
        self.intro_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(0)

    # UTILITIES
    def check_frame1_progress(self):
        if self.family_location_seg_button_1.get() == 'No':
            return True
        else:
            additional_location = self.family_location_seg_button_2.get()
            if additional_location == 'No' and self.family_location_valid1:
                return True
            elif additional_location == 'Yes' and self.family_location_valid1 and self.family_location_valid2:
                return True
            else:
                return False

    def check_frame2_progress(self):
        if self.work_seg_button_1.get() == 'Employed' and self.work_seg_button_2.get() == 'Yes' and not self.work_valid1:
            return False
        else:
            return True

    def update_center_distance_label(self):
        display_options_list = ["10 Miles", "20 Miles", "40 Miles", "60 Miles", "100 Miles", "200 Miles"]

        center_distance = self.IdealHomeDataAnalysis.find_distance_to_center()
        if center_distance > 10:
            display_options_list = [f"{center_distance+10} Miles", f"{center_distance+20} Miles", f"{center_distance+40} Miles", f"{center_distance+60} Miles", f"{center_distance+100} Miles", f"{center_distance+200} Miles"]

        if self.family_location_valid2 or (self.family_location_valid1 and self.work_valid1):
            self.work_label4.configure(text=f"What is the maximum preferable travel distance from the location(s)? (Center Point Distance: {center_distance} Miles)")
            self.family_location_label3.configure(text=f"What is the maximum preferable travel distance from the location(s)? (Center Point Distance: {center_distance} Miles)")
        else:
            self.family_location_label3.configure(text="What is the maximum preferable travel distance from the location(s)?")
            self.work_label4.configure(text="What is the maximum preferable travel distance from the location(s)?")

        location_options = self.work_seg_button_4.cget('values')
        self.radius_index = location_options.index(self.family_location_seg_button_3.get())
        self.family_location_seg_button_3.configure(values=display_options_list)
        self.family_location_seg_button_3.set(display_options_list[self.radius_index])
        self.work_seg_button_4.configure(values=display_options_list)
        self.work_seg_button_4.set(display_options_list[self.radius_index])

    def load_data_analysis(self):
        self.IdealHomeDataAnalysis = IdealHomeDataAnalysis()

    def set_map_position(self):
        self.map_widget = TkinterMapView(self.results_frame, corner_radius=0)
        self.map_widget.grid(row=10, column=0, columnspan=3, sticky="nswe", padx=6, pady=(10,5))
        self.map_widget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png", max_zoom=22)
        self.map_position = self.map_widget.set_position(self.city_coordinates[0], self.city_coordinates[1]) 
        self.map_widget.fit_bounding_box((self.zipcode_prefix_boundary['North_Boundary']+0.1, self.zipcode_prefix_boundary['West_Boundary']-0.1), (self.zipcode_prefix_boundary['South_Boundary']-0.1, self.zipcode_prefix_boundary['East_Boundary']+0.1))

    def set_map_results(self, **kwargs):
        if self.map_marker:
            self.map_marker_region.delete()
            self.map_marker.delete()
            self.results_polygon.delete()

        self.map_marker = self.map_widget.set_marker(self.city_coordinates[0], self.city_coordinates[1], text=f"{self.city_name}")
        self.results_polygon = self.map_widget.set_polygon([(self.zipcode_prefix_boundary['North_Boundary'], self.zipcode_prefix_boundary['West_Boundary']), 
            (self.zipcode_prefix_boundary['North_Boundary'], self.zipcode_prefix_boundary['East_Boundary']),
            (self.zipcode_prefix_boundary['South_Boundary'], self.zipcode_prefix_boundary['East_Boundary']),
            (self.zipcode_prefix_boundary['South_Boundary'], self.zipcode_prefix_boundary['West_Boundary'])],
            fill_color=None,
            outline_color="green",
            border_width=4)
        self.map_marker_region = self.map_widget.set_marker(self.zipcode_prefix_boundary['North_Boundary'], (self.zipcode_prefix_boundary['East_Boundary'] + self.zipcode_prefix_boundary['West_Boundary']) / 2,
            marker_color_circle='green',
            marker_color_outside='green',
            text=f"{self.final_results['Region_Name']}")
    
    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    def error_message(self, message_type: str = 'Entry_Field'):
        if message_type == 'Entry_Field':
            messagebox.showerror('Entry Field Invalid Submission', 'Please fill in all fields with valid input.')
        elif message_type == 'Segmented_Button':
            messagebox.showerror('Incomplete Submission', 'Please complete submission fields or deselect the location requirement.')
        elif message_type == 'Afforability_Warning':
            messagebox.showerror('Warning', 'The result shown is outside of an afforable range for your home value.')

    def github_more_information(self):
        webbrowser.open_new('https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
        self._windows_set_titlebar_color('dark')
        self.update()

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
