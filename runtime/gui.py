from tkinter import messagebox
import customtkinter
from tkintermapview import TkinterMapView
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
        self.geometry(f"{1100}x{1000}")

        # Load Custom Fonts
        Font(file="assets/fonts/Telex-Regular.ttf")
        Font(file="assets/fonts/Cabin-Bold.ttf")
        
        title_font = customtkinter.CTkFont(family='Cabin', size=28, weight="bold")
        self.regular_font = customtkinter.CTkFont(family='Telex', size=16, weight="normal")
        small_font = customtkinter.CTkFont(family='Telex', size=14, weight="normal")
        regular_font_underline = customtkinter.CTkFont(family='Telex', size=16, weight="normal", underline=True)
        self.large_font = customtkinter.CTkFont(family='Telex', size=19, weight="normal")
        self.large_bold = customtkinter.CTkFont(family='Telex', size=19, weight="bold")
        self.large_font_underline = customtkinter.CTkFont(family='Telex', size=19, weight="normal", underline=True)

        # Configure App Grid Layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)


        """ 
            Header Frame 
        """
        self.header_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#e5f1fc','#333333'))
        self.header_frame.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.header_frame.grid_rowconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        # Logo Image
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/assets/images/Ideal_Home_Location_Matcher.png"),size=(358, 87))
        self.bg_image_label = customtkinter.CTkLabel(self.header_frame, text='', image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky='nw')
        # Github Link
        self.github_image = customtkinter.CTkImage(light_image=Image.open(current_path + "/assets/images/github-mark.png"),dark_image=Image.open(current_path + "/assets/images/github-mark-white.png"), size=(101, 25))
        self.github_button = customtkinter.CTkButton(self.header_frame, image=self.github_image, width=90, hover_color=('#fff','#000'), text='', compound='right', fg_color='transparent', bg_color='transparent', command=self.github_more_information)
        self.github_button.grid(row=0, column=1, padx=15, pady=(10, 10), sticky='e')

        """ 
            Sidebar Frame 
        """
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0, fg_color=('#e5f1fc','#333333'))
        self.sidebar_frame.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        # Finish Label
        self.finish_label = customtkinter.CTkLabel(self.sidebar_frame, text="Finish Line", anchor="center", font=regular_font_underline, fg_color=('#ccc','#333'))
        self.finish_label.grid(row=0, column=0, ipadx=10, padx=10, pady=(40, 20))
        # Progres Bar Initalize
        self.progressbar = customtkinter.CTkProgressBar(self.sidebar_frame, orientation="vertical", border_width=1)
        self.progressbar.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky='ns')
        self.progressbar.set(0)
        # Start Label
        self.start_label = customtkinter.CTkLabel(self.sidebar_frame, text="Start Line", font=regular_font_underline, fg_color=('#ccc','#333'))
        self.start_label.grid(row=3, column=0, ipadx=10, padx=10, pady=(20, 20), sticky='')
        # Appearance Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", font=small_font)
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, width=100, values=["Light", "Dark", "System"], anchor='center', command=self.change_appearance_mode_event, font=small_font, dropdown_font=self.regular_font)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(10, 10))
        self.appearance_mode_optionemenu.set("System")
        # US Scaling
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", font=small_font)
        self.scaling_label.grid(row=7, column=0, padx=10, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, width=100, values=["80%", "90%", "100%", "110%", "120%"], anchor='center', command=self.change_scaling_event, font=small_font, dropdown_font=self.regular_font)
        self.scaling_optionemenu.grid(row=8, column=0, padx=10, pady=(10, 20))
        self.scaling_optionemenu.set("100%")


        """ 
            Instructions Frame 
        """
        self.intro_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.intro_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.intro_frame.grid_rowconfigure(3, weight=1)
        self.intro_frame.grid_columnconfigure(0, weight=1)

        instructions_title = customtkinter.CTkLabel(self.intro_frame, text="Instructions", font=title_font, fg_color=('#ccc','#333'))
        instructions_title.grid(row=0, column=0, columnspan=3, ipadx=20, padx=20, pady=(20, 15), sticky='')

        textbox = customtkinter.CTkTextbox(self.intro_frame, fg_color='transparent', height=400, font=self.regular_font)
        textbox.grid(row=1, column=0, columnspan=3, padx=(33, 20), pady=(20, 0), sticky="nsew")

        textbox.insert("0.0", "Hello, Welcome to the Ideal Home Location Matcher! \n Today")
        textbox.configure(state="disabled")

        instruction_get_started_button = customtkinter.CTkButton(master=self.intro_frame, text='Get Started', text_color="#DCE4EE", font=self.regular_font, command=self.instruction_button_event)
        instruction_get_started_button.grid(row=3, column=2, padx=20, pady=20, sticky="s")


        # After Instructions Frame Load Data Analysis Class
        self.IdealHomeDataAnalysis = IdealHomeDataAnalysis()
        state_keys = sorted([*self.IdealHomeDataAnalysis.zipcode_coordinate_data.keys()])

        """ 
            Family Location Frame 1
        """
        self.family_location_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.family_location_frame.grid_rowconfigure(10, weight=1)
        self.family_location_frame.grid_columnconfigure(0, weight=1)

        family_location_title = customtkinter.CTkLabel(self.family_location_frame, text="Ideal Family Preferences", font=title_font, fg_color=('#ccc','#333'))
        family_location_title.grid(row=0, column=0, columnspan=3, ipadx=20, padx=20, pady=(20, 15), sticky='')

        family_location_label_1 = customtkinter.CTkLabel(self.family_location_frame, text="Do you want to be close to family members?", font=self.large_font_underline)
        family_location_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.family_location_frame, font=self.regular_font, command=self.seg_button_family_location)
        self.seg_button_1.grid(row=2, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.seg_button_1.configure(values=["Yes", "No"])
        self.seg_button_1.set("Yes")

        # Family Location Entry Frame 1
        self.family_location_entry_frame1 = customtkinter.CTkFrame(self.family_location_frame, corner_radius=0)
        self.family_location_entry_frame1.grid(row=3, column=0, columnspan=3, pady=10, sticky="nsew")
        self.family_location_entry_frame1.grid_rowconfigure(10, weight=1)
        self.family_location_entry_frame1.grid_columnconfigure((0, 1, 2, 3), weight=1)

        f_location_label1 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="Please enter the location of family member #1:", font=self.large_font)
        f_location_label1.grid(row=0, column=0, columnspan=4, padx=40, pady=12, sticky='')

        f_location_label2 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="City:", font=self.large_font)
        f_location_label2.grid(row=1, column=0, padx=60, pady=12, sticky='n')

        f_location_label3 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="State:", font=self.large_font)
        f_location_label3.grid(row=1, column=1, padx=40, pady=12, sticky='n')

        f_location_label4 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="Zipcode:", font=self.large_font)
        f_location_label4.grid(row=1, column=2, padx=40, pady=12, sticky='n')


        self.family_location_entry1 = customtkinter.CTkEntry(self.family_location_entry_frame1, width=250, placeholder_text='City')
        self.family_location_entry1.grid(row=2, column=0, padx=40, pady=12, sticky='n')

        self.family_location_entry2 = customtkinter.CTkEntry(self.family_location_entry_frame1, placeholder_text='State')
        self.family_location_entry2.grid(row=2, column=1, padx=40, pady=12, sticky='n')

        self.family_location_entry3 = customtkinter.CTkEntry(self.family_location_entry_frame1, placeholder_text='Zipcode')
        self.family_location_entry3.grid(row=2, column=2, padx=40, pady=12, sticky='n')

        self.f_location_button_1 = customtkinter.CTkButton(master=self.family_location_entry_frame1, text='Verify', text_color=("gray10", "#DCE4EE"), font=self.regular_font)
        self.f_location_button_1.grid(row=2, column=3, padx=(20, 20), pady=12, sticky="n")

        self.f_location_label5 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="I", font=self.large_font)
        self.f_location_label5.grid(row=3, column=0, columnspan=2, padx=40, pady=12, sticky='e')

        self.f_location_button_2 = customtkinter.CTkButton(master=self.family_location_entry_frame1, text='Confirm', text_color=("gray10", "#DCE4EE"), font=self.regular_font)
        self.f_location_button_2.grid(row=3, column=2, padx=(20, 20), pady=12, sticky="")


        self.family_location_label2 = customtkinter.CTkLabel(self.family_location_frame, text="Additional Location?", font=self.large_font_underline)
        self.family_location_label2.grid(row=4, column=0, columnspan=3, pady=10, padx=20, sticky="")

        self.seg_button_2 = customtkinter.CTkSegmentedButton(self.family_location_frame, font=self.regular_font, command=self.seg_button_family_location_2)
        self.seg_button_2.grid(row=5, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.seg_button_2.configure(values=["Yes", "No"])
        self.seg_button_2.set("Yes")

        # Family Location Entry Frame 2
        self.family_location_entry_frame2 = customtkinter.CTkFrame(self.family_location_frame, corner_radius=0)
        self.family_location_entry_frame2.grid(row=6, column=0, columnspan=3, pady=10, sticky="nsew")
        self.family_location_entry_frame2.grid_rowconfigure(10, weight=1)
        self.family_location_entry_frame2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        f2_location_label1 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="Please enter the location of family member #2:", font=self.large_font)
        f2_location_label1.grid(row=0, column=0, columnspan=4, padx=40, pady=12, sticky='')

        f2_location_label2 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="City:", font=self.large_font)
        f2_location_label2.grid(row=1, column=0, padx=60, pady=12, sticky='n')

        f2_location_label3 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="State:", font=self.large_font)
        f2_location_label3.grid(row=1, column=1, padx=40, pady=12, sticky='n')

        f2_location_label4 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="Zipcode:", font=self.large_font)
        f2_location_label4.grid(row=1, column=2, padx=40, pady=12, sticky='n')


        self.family_location_entry4 = customtkinter.CTkEntry(self.family_location_entry_frame2, width=250, placeholder_text='City')
        self.family_location_entry4.grid(row=2, column=0, padx=40, pady=12, sticky='n')

        self.family_location_entry5 = customtkinter.CTkEntry(self.family_location_entry_frame2, placeholder_text='State')
        self.family_location_entry5.grid(row=2, column=1, padx=40, pady=12, sticky='n')

        self.family_location_entry6 = customtkinter.CTkEntry(self.family_location_entry_frame2, placeholder_text='Zipcode')
        self.family_location_entry6.grid(row=2, column=2, padx=40, pady=12, sticky='n')

        self.f2_location_button_1 = customtkinter.CTkButton(master=self.family_location_entry_frame2, text='Verify', text_color=("gray10", "#DCE4EE"), font=self.regular_font)
        self.f2_location_button_1.grid(row=2, column=3, padx=(20, 20), pady=12, sticky="n")

        self.f2_location_label5 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="I", font=self.large_font)
        self.f2_location_label5.grid(row=3, column=0, columnspan=2, padx=40, pady=12, sticky='e')

        self.f2_location_button_2 = customtkinter.CTkButton(master=self.family_location_entry_frame2, text='Confirm', text_color=("gray10", "#DCE4EE"), font=self.regular_font)
        self.f2_location_button_2.grid(row=3, column=2, padx=(20, 20), pady=12, sticky="")


        family_location_next_button = customtkinter.CTkButton(master=self.family_location_frame, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_1_forward_event)
        family_location_next_button.grid(row=11, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        family_location_previous_button = customtkinter.CTkButton(master=self.family_location_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_1_backward_event)
        family_location_previous_button.grid(row=11, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")
        

        """ 
            Family Details Frame 1b
        """
        self.family_details_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.family_details_frame.grid_rowconfigure((3,6,9,12,15), weight=1)
        self.family_details_frame.grid_columnconfigure(0, weight=1)

        family_details_title = customtkinter.CTkLabel(self.family_details_frame, text="Ideal Family Preferences", font=title_font)
        family_details_title.grid(row=0, column=0, padx=20, columnspan=4, pady=(20, 15), sticky='')


        self.family_details_label1 = customtkinter.CTkLabel(self.family_details_frame, text="What is the maximum driving distance prefered?", font=self.large_font_underline)
        self.family_details_label1.grid(row=1, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_1 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font)
        self.family_details_seg_button_1.grid(row=2, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_1.configure(values=["30 minutes", "60 minutes"])
        self.family_details_seg_button_1.set("60 minutes")


        self.family_details_label2 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to be around people with the same relationship status as you?", font=self.large_font_underline)
        self.family_details_label2.grid(row=4, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_2 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font)
        self.family_details_seg_button_2.grid(row=5, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_2.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_2.set("3")


        self.family_details_label3 = customtkinter.CTkLabel(self.family_details_frame, text="Do you have children?", font=self.large_font_underline)
        self.family_details_label3.grid(row=7, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')


        self.family_details_seg_button_3 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font)
        self.family_details_seg_button_3.grid(row=8, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_3.configure(values=["Yes", "No"])
        self.family_details_seg_button_3.set("Yes")

        self.family_details_label4 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to be around people with the same family status as you?", font=self.large_font_underline)
        self.family_details_label4.grid(row=10, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_4 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font)
        self.family_details_seg_button_4.grid(row=11, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_4.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_4.set("3")

        self.family_details_label5 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to have a large percent of the children enrolled in school?", font=self.large_font_underline)
        self.family_details_label5.grid(row=13, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_5 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=self.regular_font)
        self.family_details_seg_button_5.grid(row=14, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_5.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_5.set("3")

        family_details_next_button = customtkinter.CTkButton(master=self.family_details_frame, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_1b_forward_event)
        family_details_next_button.grid(row=16, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        family_details_previous_button = customtkinter.CTkButton(master=self.family_details_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_1b_backward_event)
        family_details_previous_button.grid(row=16, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")
        

        """ 
            Work Location Frame 2
        """
        self.work_location_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.work_location_frame.grid_rowconfigure(10, weight=1)
        self.work_location_frame.grid_columnconfigure(0, weight=1)

        work_location_title = customtkinter.CTkLabel(self.work_location_frame, text="Ideal Work Preferences", font=title_font)
        work_location_title.grid(row=0, column=0, padx=20, columnspan=4, pady=(20, 15), sticky='')

        work_location_label_1 = customtkinter.CTkLabel(self.work_location_frame, text="Are you employed?", font=self.large_font_underline)
        work_location_label_1.grid(row=1, column=0, columnspan=3, pady=10, padx=20, sticky="")

        self.work_location_seg_button_1 = customtkinter.CTkSegmentedButton(self.work_location_frame, font=self.regular_font, command=self.seg_button_work_location_1)
        self.work_location_seg_button_1.grid(row=2, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_location_seg_button_1.configure(values=["Yes", "No"])
        self.work_location_seg_button_1.set("Yes")


        # self.work_location_label2 = customtkinter.CTkLabel(self.work_location_frame, text="How important is it to have a large amount of employment opportunities?", font=self.large_font_underline)
        # self.work_location_label2.grid(row=3, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        # self.work_location_seg_button_2 = customtkinter.CTkSegmentedButton(self.work_location_frame, font=self.regular_font)
        # self.work_location_seg_button_2.grid(row=4, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        # self.work_location_seg_button_2.configure(values=["1", "2", "3", "4", "5"])
        # self.work_location_seg_button_2.set("3")

        self.work_location_label2 = customtkinter.CTkLabel(self.work_location_frame, text="Do you want to be close to work?", font=self.large_font_underline)
        self.work_location_label2.grid(row=3, column=0, columnspan=3, pady=10, padx=20, sticky="")

        self.work_location_seg_button_2 = customtkinter.CTkSegmentedButton(self.work_location_frame, font=self.regular_font, command=self.seg_button_work_location_2)
        self.work_location_seg_button_2.grid(row=4, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_location_seg_button_2.configure(values=["Yes", "No"])
        self.work_location_seg_button_2.set("Yes")

        # Work Location Entry Frame 1
        self.work_location_entry_frame1 = customtkinter.CTkFrame(self.work_location_frame, corner_radius=0)
        self.work_location_entry_frame1.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")
        self.work_location_entry_frame1.grid_rowconfigure(10, weight=1)
        self.work_location_entry_frame1.grid_columnconfigure((0, 1, 2, 3), weight=1)

        w_location_label1 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="Please enter the location of work office #1:", font=self.large_font)
        w_location_label1.grid(row=0, column=0, columnspan=4, padx=40, pady=12, sticky='')

        w_location_label2 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="City:", font=self.large_font)
        w_location_label2.grid(row=1, column=0, padx=60, pady=12, sticky='n')

        w_location_label3 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="State:", font=self.large_font)
        w_location_label3.grid(row=1, column=1, padx=40, pady=12, sticky='n')

        w_location_label4 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="Zipcode:", font=self.large_font)
        w_location_label4.grid(row=1, column=2, padx=40, pady=12, sticky='n')


        self.work_location_entry1 = customtkinter.CTkEntry(self.work_location_entry_frame1, width=250, placeholder_text='City')
        self.work_location_entry1.grid(row=2, column=0, padx=40, pady=12, sticky='n')

        self.work_location_entry2 = customtkinter.CTkEntry(self.work_location_entry_frame1, placeholder_text='State')
        self.work_location_entry2.grid(row=2, column=1, padx=40, pady=12, sticky='n')

        self.work_location_entry3 = customtkinter.CTkEntry(self.work_location_entry_frame1, placeholder_text='Zipcode')
        self.work_location_entry3.grid(row=2, column=2, padx=40, pady=12, sticky='n')

        self.w_location_button_1 = customtkinter.CTkButton(master=self.work_location_entry_frame1, text='Verify', text_color="#DCE4EE", font=self.regular_font)
        self.w_location_button_1.grid(row=2, column=3, padx=(20, 20), pady=12, sticky="n")

        self.w_location_label5 = customtkinter.CTkLabel(self.work_location_entry_frame1, text="I", font=self.large_font)
        self.w_location_label5.grid(row=3, column=0, columnspan=2, padx=40, pady=12, sticky='e')

        self.w_location_button_2 = customtkinter.CTkButton(master=self.work_location_entry_frame1, text='Confirm', text_color="#DCE4EE", font=self.regular_font)
        self.w_location_button_2.grid(row=3, column=2, padx=(20, 20), pady=12, sticky="")


        self.work_location_label2 = customtkinter.CTkLabel(self.work_location_frame, text="Additional Location?", font=self.large_font_underline)
        self.work_location_label2.grid(row=6, column=0, columnspan=3, pady=10, padx=20, sticky="")

        self.seg_button_3 = customtkinter.CTkSegmentedButton(self.work_location_frame, font=self.regular_font, command=self.seg_button_work_location_2)
        self.seg_button_3.grid(row=7, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.seg_button_3.configure(values=["Yes", "No"])
        self.seg_button_3.set("Yes")

        # Work Location Entry Frame 2
        self.work_location_entry_frame2 = customtkinter.CTkFrame(self.work_location_frame, corner_radius=0)
        self.work_location_entry_frame2.grid(row=8, column=0, columnspan=3, pady=10, sticky="nsew")
        self.work_location_entry_frame2.grid_rowconfigure(10, weight=1)
        self.work_location_entry_frame2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        w2_location_label1 = customtkinter.CTkLabel(self.work_location_entry_frame2, text="Please enter the location of work office #2:", font=self.large_font)
        w2_location_label1.grid(row=0, column=0, columnspan=4, padx=40, pady=12, sticky='')

        w2_location_label2 = customtkinter.CTkLabel(self.work_location_entry_frame2, text="City:", font=self.large_font)
        w2_location_label2.grid(row=1, column=0, padx=60, pady=12, sticky='n')

        w2_location_label3 = customtkinter.CTkLabel(self.work_location_entry_frame2, text="State:", font=self.large_font)
        w2_location_label3.grid(row=1, column=1, padx=40, pady=12, sticky='n')

        w2_location_label4 = customtkinter.CTkLabel(self.work_location_entry_frame2, text="Zipcode:", font=self.large_font)
        w2_location_label4.grid(row=1, column=2, padx=40, pady=12, sticky='n')


        self.work_location_entry4 = customtkinter.CTkEntry(self.work_location_entry_frame2, width=250, placeholder_text='City')
        self.work_location_entry4.grid(row=2, column=0, padx=40, pady=12, sticky='n')

        self.work_location_entry5 = customtkinter.CTkEntry(self.work_location_entry_frame2, placeholder_text='State')
        self.work_location_entry5.grid(row=2, column=1, padx=40, pady=12, sticky='n')

        self.work_location_entry6 = customtkinter.CTkEntry(self.work_location_entry_frame2, placeholder_text='Zipcode')
        self.work_location_entry6.grid(row=2, column=2, padx=40, pady=12, sticky='n')

        self.w2_location_button_1 = customtkinter.CTkButton(master=self.work_location_entry_frame2, text='Verify', text_color="#DCE4EE", font=self.regular_font)
        self.w2_location_button_1.grid(row=2, column=3, padx=(20, 20), pady=12, sticky="n")

        self.w2_location_label5 = customtkinter.CTkLabel(self.work_location_entry_frame2, text="I", font=self.large_font)
        self.w2_location_label5.grid(row=3, column=0, columnspan=2, padx=40, pady=12, sticky='e')

        self.w2_location_button_2 = customtkinter.CTkButton(master=self.work_location_entry_frame2, text='Confirm', text_color="#DCE4EE", font=self.regular_font)
        self.w2_location_button_2.grid(row=3, column=2, padx=(20, 20), pady=12, sticky="")


        work_location_next_button = customtkinter.CTkButton(master=self.work_location_frame, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_2_forward_event)
        work_location_next_button.grid(row=11, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        work_location_previous_button = customtkinter.CTkButton(master=self.work_location_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_2_backward_event)
        work_location_previous_button.grid(row=11, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        
        """ 
            Work Details Frame 2b
        """
        self.work_details_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.work_details_frame.grid_rowconfigure(10, weight=1)
        self.work_details_frame.grid_columnconfigure(0, weight=1)

        work_details_title = customtkinter.CTkLabel(self.work_details_frame, text="Ideal Work Preferences", font=title_font)
        work_details_title.grid(row=0, column=0, padx=20, columnspan=3, pady=(20, 15), sticky='')

        self.work_details_label1 = customtkinter.CTkLabel(self.work_details_frame, text="Are you single or married?", font=self.large_font_underline)
        self.work_details_label1.grid(row=1, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.work_details_seg_button_1 = customtkinter.CTkSegmentedButton(self.work_details_frame, font=self.regular_font)
        self.work_details_seg_button_1.grid(row=2, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_details_seg_button_1.configure(values=["Single", "Married"])
        self.work_details_seg_button_1.set("Single")

        self.work_details_label4 = customtkinter.CTkLabel(self.work_details_frame, text="What is your prefered method of getting to work?", font=self.large_font_underline)
        self.work_details_label4.grid(row=7, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.work_details_seg_button_2 = customtkinter.CTkSegmentedButton(self.work_details_frame, font=self.regular_font)
        self.work_details_seg_button_2.grid(row=8, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_details_seg_button_2.configure(values=["Car, Truck, Personal Vehicle", "Public Transportation", "Walking or Biking", 'Not Applicable'])
        self.work_details_seg_button_2.set("Car, Truck, Personal Vehicle")

        self.work_details_label5 = customtkinter.CTkLabel(self.work_details_frame, text="What is your ideal commute time?", font=self.large_font_underline)
        self.work_details_label5.grid(row=9, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.work_details_seg_button_3 = customtkinter.CTkSegmentedButton(self.work_details_frame, font=self.regular_font)
        self.work_details_seg_button_3.grid(row=10, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_details_seg_button_3.configure(values=["Less than 20 minutes", "Less than 30 minutes", "Less than 40 minutes", "Flexible"])
        self.work_details_seg_button_3.set("Flexible")

        work_details_next_button = customtkinter.CTkButton(master=self.work_details_frame, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_2b_forward_event)
        work_details_next_button.grid(row=11, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        work_details_previous_button = customtkinter.CTkButton(master=self.work_details_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_2b_backward_event)
        work_details_previous_button.grid(row=11, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        
        """ 
            Income Metrics Frame 3
        """
        self.income_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.income_frame.grid_rowconfigure((3,6,9,12,15), weight=1)
        self.income_frame.grid_columnconfigure(0, weight=1)

        income_title = customtkinter.CTkLabel(self.income_frame, text="Income Information", font=title_font)
        income_title.grid(row=0, column=0, padx=20, columnspan=3, pady=(20, 15), sticky='')

        income_label_1 = customtkinter.CTkLabel(self.income_frame, text="What is your annual household income?", font=self.large_font_underline)
        income_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Income Entry Frame 2
        self.income_entry_frame1 = customtkinter.CTkFrame(self.income_frame, corner_radius=0)
        self.income_entry_frame1.grid(row=2, column=0, columnspan=3, pady=10, sticky="nsew")
        self.income_entry_frame1.grid_rowconfigure(0, weight=1)
        self.income_entry_frame1.grid_columnconfigure((0, 1), weight=1)

        self.income_entry1 = customtkinter.CTkEntry(self.income_entry_frame1, font=self.regular_font)
        self.income_entry1.grid(row=0, column=0, padx=40, pady=12, sticky='e')
        self.income_entry1.bind("<Return>", self.income_button_1)

        units = customtkinter.CTkLabel(self.income_entry_frame1, text="$", font=self.large_font)
        units.grid(row=0, column=0, padx=(0, 190), pady=12, sticky='e')

        self.income_sumbit_button1 = customtkinter.CTkButton(master=self.income_entry_frame1, text='Submit', text_color="#DCE4EE", font=self.regular_font, command=self.income_button_1)
        self.income_sumbit_button1.grid(row=0, column=1, padx=(20, 20), pady=12, sticky="w")

        income_label_2 = customtkinter.CTkLabel(self.income_frame, text="Do you need to take out a morgage? What term length fits you?", font=self.large_font_underline)
        income_label_2.grid(row=4, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.income_seg_button_1 = customtkinter.CTkSegmentedButton(self.income_frame, font=self.regular_font, command=self.seg_button_income)
        self.income_seg_button_1.grid(row=5, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.income_seg_button_1.configure(values=["No Morgage", "15 Years", "30 Years"])
        self.income_seg_button_1.set("30 Years")

        self.income_label3 = customtkinter.CTkLabel(self.income_frame, text="What interest rate do you expect to receive?", font=self.large_font_underline)
        self.income_label3.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            
        # Income Entry Frame 2
        self.income_entry_frame2 = customtkinter.CTkFrame(self.income_frame, corner_radius=0)
        self.income_entry_frame2.grid(row=8, column=0, columnspan=3, pady=10, sticky="nsew")
        self.income_entry_frame2.grid_rowconfigure(0, weight=1)
        self.income_entry_frame2.grid_columnconfigure((0, 1), weight=1)

        self.income_entry2 = customtkinter.CTkEntry(self.income_entry_frame2, font=self.regular_font)
        self.income_entry2.grid(row=0, column=0, padx=40, pady=12, sticky='e')
        self.income_entry2.bind("<Return>", self.income_button_1)

        self.income_entry2_units = customtkinter.CTkLabel(self.income_entry_frame2, text="%", font=self.large_font)
        self.income_entry2_units.grid(row=0, column=0, padx=(0, 190), pady=12, sticky='e')

        self.income_sumbit_button2 = customtkinter.CTkButton(master=self.income_entry_frame2, text='Submit', text_color="#DCE4EE", font=self.regular_font, command=self.income_button_1)
        self.income_sumbit_button2.grid(row=0, column=1, padx=(20, 20), pady=12, sticky="w")

       
        self.income_seg_button_2 = customtkinter.CTkSegmentedButton(self.income_frame, font=self.regular_font)
        self.income_seg_button_2.configure(values=["15%", "20%", "25%", "30%", "35%"])
        self.income_seg_button_2.set("25%")

        self.income_label4 = customtkinter.CTkLabel(self.income_frame, text="What percent of your income can you allocated to home expenses? (Morgage, Tax, Insurance)", font=self.large_font_underline)
        self.income_label5 = customtkinter.CTkLabel(self.income_frame, text="Your Afforadable Home Price is $250,000. Increase or Decrease?", font=self.large_bold)

        self.income_seg_button_3 = customtkinter.CTkSegmentedButton(self.income_frame, font=self.regular_font)
        self.income_seg_button_3.configure(values=["-10%", "-5%", "No Change", "+5%", "+10%"])
        self.income_seg_button_3.set("No Change")

        self.income_next_button = customtkinter.CTkButton(master=self.income_frame, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_3_forward_event)
        self.income_next_button.grid(row=16, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.income_previous_button = customtkinter.CTkButton(master=self.income_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_3_backward_event)
        self.income_previous_button.grid(row=16, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        self.seg_button_income(param='30 Years')

        """ 
            Area Classification Frame 4
        """
        self.area_classification_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.area_classification_frame.grid_rowconfigure((3, 6, 9, 12), weight=1)
        self.area_classification_frame.grid_columnconfigure(0, weight=1)

        area_classification_title = customtkinter.CTkLabel(self.area_classification_frame, text="Ideal Lifestyle Preferences", font=title_font)
        area_classification_title.grid(row=0, column=0, padx=20, columnspan=3, pady=(20, 15), sticky='')

        area_classification_label_1 = customtkinter.CTkLabel(self.area_classification_frame, text="What level of education do you have?", font=self.large_font_underline)
        area_classification_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Segmented Button #1
        self.area_classification_seg_button_1 = customtkinter.CTkSegmentedButton(self.area_classification_frame, font=self.regular_font)
        self.area_classification_seg_button_1.grid(row=2, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.area_classification_seg_button_1.configure(values=["Less than High School", "High School", "Associate's", "Bachelor's", "Master's", "Doctorate"])
        self.area_classification_seg_button_1.set("High School")

        area_classification_label_2 = customtkinter.CTkLabel(self.area_classification_frame, text="How important is it to be around people with the same education level as you?", font=self.large_font_underline)
        area_classification_label_2.grid(row=4, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Segmented Button #2
        self.area_classification_seg_button_2 = customtkinter.CTkSegmentedButton(self.area_classification_frame, font=self.regular_font)
        self.area_classification_seg_button_2.grid(row=5, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.area_classification_seg_button_2.configure(values=["1", "2", "3", "4", "5"])
        self.area_classification_seg_button_2.set("3")

        area_classification_label_3 = customtkinter.CTkLabel(self.area_classification_frame, text="What kind of living environment do you prefer?", font=self.large_font_underline)
        area_classification_label_3.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Segmented Button #3
        self.area_classification_list = ["Hyper Rural", "Rural", "Suburban", "Urban", "Hyper Urban"]
        self.area_classification_seg_button_3 = customtkinter.CTkSegmentedButton(self.area_classification_frame, font=self.regular_font, command=self.seg_button_area_classification_3)
        self.area_classification_seg_button_3.grid(row=8, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.area_classification_seg_button_3.configure(values=self.area_classification_list)
        self.area_classification_seg_button_3.set("Suburban")
        self.seg_button_area_classification_3(param='Suburban')

        area_classification_label_4 = customtkinter.CTkLabel(self.area_classification_frame, text="What kind of living environment is second most prefered?", font=self.large_font_underline)
        area_classification_label_4.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        area_classification_next_button = customtkinter.CTkButton(master=self.area_classification_frame, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_4_forward_event)
        area_classification_next_button.grid(row=13, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        area_classification_previous_button = customtkinter.CTkButton(master=self.area_classification_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_4_backward_event)
        area_classification_previous_button.grid(row=13, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        """ 
            Weather Metrics Frame 5
        """
        self.weather_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.weather_frame.grid_rowconfigure((3,6,9,12,15,18), weight=1)
        self.weather_frame.grid_columnconfigure(0, weight=1)

        weather_title = customtkinter.CTkLabel(self.weather_frame, text="Weather & Temperature Preferences", font=title_font)
        weather_title.grid(row=0, column=0, padx=20, columnspan=3, pady=(20, 15), sticky='')

        weather_label_1 = customtkinter.CTkLabel(self.weather_frame, text="How many Seasons do you prefer?", font=self.large_font_underline)
        weather_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Segmented Button #1
        self.weather_seg_button_1 = customtkinter.CTkSegmentedButton(self.weather_frame, font=self.regular_font, command=self.seg_button_weather_1)
        self.weather_seg_button_1.grid(row=2, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.weather_seg_button_1.configure(values=["1 Season", "2 Seasons", "4 Seasons"])
        self.weather_seg_button_1.set("4 Seasons")

        self.weather_label2 = customtkinter.CTkLabel(self.weather_frame, text="What is your ideal summer temperature?", font=self.large_font_underline)
        self.weather_label2.grid(row=4, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Weather Entry Frame 1
        self.weather_entry_frame1 = customtkinter.CTkFrame(self.weather_frame, corner_radius=0)
        self.weather_entry_frame1.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")
        self.weather_entry_frame1.grid_rowconfigure(0, weight=1)
        self.weather_entry_frame1.grid_columnconfigure((0, 1), weight=1)

        units = customtkinter.CTkLabel(self.weather_entry_frame1, text="°F", font=self.large_font)
        units.grid(row=0, column=0, padx=(150, 0), pady=12, sticky='e')

        self.weather_entry1 = customtkinter.CTkEntry(self.weather_entry_frame1, font=self.large_font)
        self.weather_entry1.grid(row=0, column=0, padx=40, pady=12, sticky='e')
        self.weather_entry1.bind("<Return>", self.weather_button_1)

        self.weather_submit_button1 = customtkinter.CTkButton(master=self.weather_entry_frame1, text='Submit', text_color="#DCE4EE", font=self.regular_font, command=self.weather_button_1)
        self.weather_submit_button1.grid(row=0, column=1, padx=(20, 20), pady=12, sticky="w")

        self.weather_label3 = customtkinter.CTkLabel(self.weather_frame, text="What is your ideal transition temperature?", font=self.large_font_underline)
        self.weather_label4 = customtkinter.CTkLabel(self.weather_frame, text="What is your ideal winter temperature?", font=self.large_font_underline)
            
        # Weather Entry Frame 2
        self.weather_entry_frame2 = customtkinter.CTkFrame(self.weather_frame, corner_radius=0)
        #self.weather_entry_frame2.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")
        self.weather_entry_frame2.grid_rowconfigure(0, weight=1)
        self.weather_entry_frame2.grid_columnconfigure((0, 1), weight=1)

        self.weather_entry2 = customtkinter.CTkEntry(self.weather_frame, font=self.large_font)

        # Weather Entry Frame 3
        self.weather_entry_frame3 = customtkinter.CTkFrame(self.weather_frame, corner_radius=0)
        #self.weather_entry_frame3.grid(row=5, column=0, columnspan=3, pady=10, sticky="nsew")
        self.weather_entry_frame3.grid_rowconfigure(0, weight=1)
        self.weather_entry_frame3.grid_columnconfigure((0, 1), weight=1)

        self.weather_entry3 = customtkinter.CTkEntry(self.weather_frame, font=self.large_font)

        self.weather_label5 = customtkinter.CTkLabel(self.weather_frame, text="What level of yearly precipitation do you prefer?", font=self.large_font_underline)
        self.weather_label5.grid(row=13, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.weather_seg_button_2 = customtkinter.CTkSegmentedButton(self.weather_frame, font=self.regular_font)
        self.weather_seg_button_2.grid(row=14, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.weather_seg_button_2.configure(values=["Very Low", "Low", "Average", "High", "Very High"])
        self.weather_seg_button_2.set("Average")

        self.weather_label6 = customtkinter.CTkLabel(self.weather_frame, text="What level of yearly sunshine do you prefer?", font=self.large_font_underline)
        self.weather_label6.grid(row=16, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.weather_seg_button_3 = customtkinter.CTkSegmentedButton(self.weather_frame, font=self.regular_font)
        self.weather_seg_button_3.grid(row=17, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.weather_seg_button_3.configure(values=["Very Low", "Low", "Average", "High", "Very High"])
        self.weather_seg_button_3.set("Average")

        self.weather_next_button = customtkinter.CTkButton(master=self.weather_frame, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_5_forward_event)
        self.weather_next_button.grid(row=19, column=2, padx=20, pady=20, sticky="s")
     
        self.weather_previous_button = customtkinter.CTkButton(master=self.weather_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_5_backward_event)
        self.weather_previous_button.grid(row=19, column=0, padx=20, pady=20, sticky="sw")

        self.seg_button_weather_1(param="4 Seasons")
        
        """ 
            Natural Disaster Risk Frame 6
        """
        self.natural_disaster_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.natural_disaster_frame.grid_rowconfigure((3,6,9,12), weight=1)
        self.natural_disaster_frame.grid_columnconfigure(0, weight=1)

        natural_disaster_title = customtkinter.CTkLabel(self.natural_disaster_frame, text="Natural Disaster Risk Tolerance", font=title_font)
        natural_disaster_title.grid(row=0, column=0, padx=20, columnspan=3, pady=(20, 15), sticky='')

        natural_disaster_label_1 = customtkinter.CTkLabel(self.natural_disaster_frame, text="How imporant is it to migitate natural disaster risk?", font=self.large_font_underline)
        natural_disaster_label_1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Segmented Button #1
        self.natural_disaster_seg_button_1 = customtkinter.CTkSegmentedButton(self.natural_disaster_frame, font=self.regular_font)
        self.natural_disaster_seg_button_1.grid(row=2, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.natural_disaster_seg_button_1.configure(values=["1", "2", "3", "4", "5"])
        self.natural_disaster_seg_button_1.set("3")

        natural_disaster_label_2 = customtkinter.CTkLabel(self.natural_disaster_frame, text="Which natural disaster is the #1 priority to avoid?", font=self.large_font_underline)
        natural_disaster_label_2.grid(row=4, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        # Segmented Button #2 & #3
        self.natural_disaster_list = ["Flood", "Tornado", "Thunderstorm", "Drought", "Wildfire", "Earthquake", "Huricane"]
        self.natural_disaster_seg_button_2 = customtkinter.CTkSegmentedButton(self.natural_disaster_frame, font=self.regular_font, command=self.seg_button_natural_disaster_2)
        self.natural_disaster_seg_button_2.grid(row=5, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.natural_disaster_seg_button_2.configure(values=self.natural_disaster_list)
        self.natural_disaster_seg_button_2.set("Thunderstorm")
        self.seg_button_natural_disaster_2(param='Thunderstorm')

        natural_disaster_label_3 = customtkinter.CTkLabel(self.natural_disaster_frame, text="Which natural disaster is the #2 priority to avoid?", font=self.large_font_underline)
        natural_disaster_label_3.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        natural_disaster_label_4 = customtkinter.CTkLabel(self.natural_disaster_frame, text="Which natural disaster is the #3 priority to avoid?", font=self.large_font_underline)
        natural_disaster_label_4.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        natural_disaster_next_button = customtkinter.CTkButton(master=self.natural_disaster_frame, text='Next', text_color="#DCE4EE", font=self.regular_font, command=self.frame_6_forward_event)
        natural_disaster_next_button.grid(row=13, column=2, padx=20, pady=20, sticky="s")
     
        natural_disaster_previous_button = customtkinter.CTkButton(master=self.natural_disaster_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_6_backward_event)
        natural_disaster_previous_button.grid(row=13, column=0, padx=20, pady=20, sticky="sw")

        """ 
            Results Frame 7
        """
        self.results_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.results_frame.grid_rowconfigure(10, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)

        self.results_title = customtkinter.CTkLabel(self.results_frame, text="Congratulations!", font=title_font)
        self.results_title.grid(row=0, column=0, padx=20, columnspan=3, pady=(20, 15), sticky='')

        self.map_widget = TkinterMapView(self.results_frame, corner_radius=0)
        self.map_widget.grid(row=10, column=0, columnspan=3, sticky="nswe", padx=(0, 0), pady=(0, 0))
        self.map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
        self.map_widget.set_position(48.860381, 2.338594) 
        # self.map_widget.fit_bounding_box((49, -3), (47, 3))
        # self.map_widget.set_polygon([(46.0732306, 6.0095215),(46.0732306, 6.4195215),(46.3732306, 6.0095215),(46.3772542, 6.4160156)],fill_color=None,outline_color="red",border_width=10,
        #                            name="switzerland_polygon")
        # self.map_widget.set_marker(52.516268, 13.377695, text="Brandenburger Tor")

        results_previous_button = customtkinter.CTkButton(master=self.results_frame, text='Previous', text_color="#DCE4EE", font=self.regular_font, command=self.frame_7_backward_event)
        results_previous_button.grid(row=11, column=0, padx=20, pady=20, sticky="sw")

        results_restart_button = customtkinter.CTkButton(master=self.results_frame, text='Restart', text_color="#DCE4EE", font=self.regular_font, command=self.frame_7_restart_event)
        results_restart_button.grid(row=11, column=2, padx=20, pady=20, sticky="sw")

    # ----------------------- Buttons ---------------------------

    def income_button_1(self):
        self.income_frame.focus()
        self.income_entry1_valid = False
        self.income_entry2_valid = False
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
            
        if income_entry_value2 and morgage_param != 'No Morgage' and 0 <= income_entry_float2 < 90:
            self.income_entry2.configure(border_color='green', border_width=2)
            self.income_entry2_valid = True
        elif income_entry_value2 and morgage_param != 'No Morgage' and (income_entry_float2 < 0 or income_entry_float2 >= 90):
            self.income_entry2.configure(border_color='red', border_width=2)
        elif income_entry_value2 and morgage_param == 'No Morgage' and 0 < income_entry_float2 <= 10_000_000:
            self.income_entry2.configure(border_color='green', border_width=2)
            self.income_entry2_valid = True
        elif income_entry_value2 and morgage_param == 'No Morgage' and (income_entry_float2 <= 0 or income_entry_float2 > 10_000_000):
            self.income_entry2.configure(border_color='red', border_width=2)

        if self.income_entry1_valid and self.income_entry2_valid and morgage_param != 'No Morgage':
            self.income_label5.grid(row=13, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.income_seg_button_3.grid(row=14, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")

    def weather_button_1(self):
        pass


    # ----------------------- Segmented Buttons ---------------------------

    def seg_button_family_location(self, param: str):
        print(param)

    def seg_button_family_location_2(self, param: str):
        print(param)

    def seg_button_work_location_1(self, param: str):
        print(param)

    def seg_button_work_location_2(self, param: str):
        print(param)

    def seg_button_income(self, param: str):
        if param == '30 Years' or param == '15 Years':
            self.income_label3.configure(text="What interest rate do you expect to receive?")
            self.income_entry2_units.configure(text="%")
            self.income_label4.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.income_seg_button_2.grid(row=11, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")

        else:
            self.income_label3.configure(text="What home price can you afford?")
            self.income_entry2_units.configure(text="$")
            self.income_label4.grid_forget()
            self.income_seg_button_2.grid_forget()

    def seg_button_weather_1(self, param: str):

        if param == "4 Seasons":
            self.weather_label2.configure(text="What is your ideal summer temperature?")

            self.weather_label3.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_entry2.grid(row=8, column=0, columnspan=3, padx=40, pady=12, sticky='n')

            self.weather_label4.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_entry3.grid(row=11, column=0, columnspan=3, padx=40, pady=12, sticky='n')

            self.weather_frame.grid_rowconfigure((15,18), weight=1)
            self.weather_label5.grid(row=13, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_2.grid(row=14, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.weather_label6.grid(row=16, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_3.grid(row=17, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.weather_next_button.grid(row=19, column=2, padx=20, pady=20, sticky="s")
            self.weather_previous_button.grid(row=19, column=0, padx=20, pady=20, sticky="sw")

        elif param == "2 Seasons":
            self.weather_label2.configure(text="What is your ideal summer temperature?")

            self.weather_label4.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_entry3.grid(row=8, column=0, columnspan=3, padx=40, pady=12, sticky='n')

            self.weather_frame.grid_rowconfigure(15, weight=1)
            self.weather_frame.grid_rowconfigure(18, weight=0)
            self.weather_label5.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_2.grid(row=11, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.weather_label6.grid(row=13, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_3.grid(row=14, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.weather_next_button.grid(row=16, column=2, padx=20, pady=20, sticky="s")
            self.weather_previous_button.grid(row=16, column=0, padx=20, pady=20, sticky="sw")
            try:
                self.weather_label3.grid_forget()
                self.weather_entry2.grid_forget()
            except:
                pass

        else:
            self.weather_label2.configure(text="What is your ideal outside temperature?")

            self.weather_frame.grid_rowconfigure((15, 18), weight=0)
            self.weather_label5.grid(row=7, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_2.grid(row=8, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.weather_label6.grid(row=10, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')
            self.weather_seg_button_3.grid(row=11, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
            self.weather_next_button.grid(row=13, column=2, padx=20, pady=20, sticky="s")
            self.weather_previous_button.grid(row=13, column=0, padx=20, pady=20, sticky="sw")
            try:
                self.weather_label4.grid_forget()
                self.weather_entry3.grid_forget()
            except:
                pass
            try:
                self.weather_label3.grid_forget()
                self.weather_entry2.grid_forget()
            except:
                pass

    def seg_button_area_classification_3(self, param: str):
        area_classification_list = [*self.area_classification_list]
        area_classification_list.remove(param)

        # Segmented Button #3
        self.area_classification_seg_button_4 = customtkinter.CTkSegmentedButton(self.area_classification_frame, font=self.regular_font)
        self.area_classification_seg_button_4.grid(row=11, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.area_classification_seg_button_4.configure(values=area_classification_list)
        self.area_classification_seg_button_4.set(area_classification_list[0])

    def seg_button_natural_disaster_2(self, param: str):
        self.natural_disaster_list_2 = [*self.natural_disaster_list]
        self.natural_disaster_list_2.remove(param)

        # Segmented Button #3
        self.natural_disaster_seg_button_3 = customtkinter.CTkSegmentedButton(self.natural_disaster_frame, font=self.regular_font, command=self.seg_button_natural_disaster_3)
        self.natural_disaster_seg_button_3.grid(row=8, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.natural_disaster_seg_button_3.configure(values=self.natural_disaster_list_2)
        self.natural_disaster_seg_button_3.set(self.natural_disaster_list_2[0])
        self.seg_button_natural_disaster_3(param=self.natural_disaster_list_2[0])

    def seg_button_natural_disaster_3(self, param: str):
        natural_disaster_list = [*self.natural_disaster_list_2]
        natural_disaster_list.remove(param)

        # Segmented Button #4
        self.natural_disaster_seg_button_4 = customtkinter.CTkSegmentedButton(self.natural_disaster_frame, font=self.regular_font)
        self.natural_disaster_seg_button_4.grid(row=11, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.natural_disaster_seg_button_4.configure(values=natural_disaster_list)
        self.natural_disaster_seg_button_4.set(natural_disaster_list[0])

    # ----------------------- Navigation Buttons ---------------------------

    def instruction_button_event(self):
        self.intro_frame.grid_forget()
        self.family_location_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.11)

    # FRAME 1
    def frame_1_forward_event(self):
        self.family_location_frame.grid_forget()
        self.family_details_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.22)
   

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
        self.work_details_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.44)
 
    def frame_2_backward_event(self):
        self.work_location_frame.grid_forget()
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
        self.income_button_1()
        if self.income_entry1_valid and self.income_entry2_valid:
            self.income_frame.grid_forget()
            self.area_classification_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
            self.progressbar.set(.66)
        else:
            messagebox.showerror('Entry Field Invalid Submission', 'Please fill in all fields with valid input.')

    def frame_3_backward_event(self):
        self.income_frame.grid_forget()
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

    def frame_7_restart_event(self):
        self.results_frame.grid_forget()
        self.intro_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(0)

    # UTILITIES
    def github_more_information(self):
        webbrowser.open_new('https://github.com/andrew-drogalis/Ideal-Home-Location-Matcher')

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
