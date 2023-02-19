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
        self.geometry(f"{1100}x{950}")

        # Load Custom Fonts
        Font(file="assets/fonts/Neuton-Regular.ttf")
        Font(file="assets/fonts/Cabin-Regular.ttf")
        Font(file="assets/fonts/Cabin-Medium.ttf")
        Font(file="assets/fonts/Cabin-SemiBold.ttf")
        Font(file="assets/fonts/Cabin-Bold.ttf")
        
        title_font = customtkinter.CTkFont(family='Neuton', size=24, weight="normal")
        regular_font = customtkinter.CTkFont(family='Cabin', size=16, weight="normal")
        large_font = customtkinter.CTkFont(family='Cabin', size=20, weight="normal")
        bold_font = customtkinter.CTkFont(family='Cabin', size=16, weight="bold")

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
        self.bg_image = customtkinter.CTkImage(Image.open(current_path + "/assets/images/Ideal_Home_Location_Matcher.png"),size=(360, 85))
        self.bg_image_label = customtkinter.CTkLabel(self.header_frame, text='', image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky='nw')
        # Github Link
        self.github_image = customtkinter.CTkImage(light_image=Image.open(current_path + "/assets/images/github-mark.png"),dark_image=Image.open(current_path + "/assets/images/github-mark-white.png"), size=(76, 25))
        self.github_button = customtkinter.CTkButton(self.header_frame, image=self.github_image, width=90, hover_color=('#fff','#000'), text='', compound='right', fg_color='transparent', bg_color='transparent', command=self.github_more_information)
        self.github_button.grid(row=0, column=1, padx=10, pady=(10, 10), sticky='ne')

        """ 
            Sidebar Frame 
        """
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=3, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        # Finish Label
        self.finish_label = customtkinter.CTkLabel(self.sidebar_frame, text="Finish Line", anchor="n", font=regular_font)
        self.finish_label.grid(row=0, column=0, padx=10, pady=(20, 20))
        # Progres Bar Initalize
        self.progressbar = customtkinter.CTkProgressBar(self.sidebar_frame, orientation="vertical")
        self.progressbar.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky='ns')
        self.progressbar.set(0)
        # Start Label
        self.start_label = customtkinter.CTkLabel(self.sidebar_frame, text="Start Line", font=regular_font)
        self.start_label.grid(row=3, column=0, padx=10, pady=(20, 20), sticky='n')
        # Appearance Mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w", font=regular_font)
        self.appearance_mode_label.grid(row=5, column=0, padx=10, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event, font=regular_font, dropdown_font=regular_font)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=10, pady=(10, 10))
        self.appearance_mode_optionemenu.set("System")
        # US Scaling
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w", font=regular_font)
        self.scaling_label.grid(row=7, column=0, padx=10, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event, font=regular_font, dropdown_font=regular_font)
        self.scaling_optionemenu.grid(row=8, column=0, padx=10, pady=(10, 20))
        self.scaling_optionemenu.set("100%")


        """ 
            Introduction Frame 
        """
        self.intro_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.intro_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.intro_frame.grid_rowconfigure(3, weight=1)
        self.intro_frame.grid_columnconfigure(0, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.intro_frame, text="Introduction", font=title_font)
        self.logo_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 15), sticky='')

        self.textbox = customtkinter.CTkTextbox(self.intro_frame, fg_color='transparent', height=400, font=regular_font)
        self.textbox.grid(row=1, column=0, columnspan=3, padx=(33, 20), pady=(20, 0), sticky="nsew")

        self.textbox.insert("0.0", "CTkTextbox")
        self.textbox.configure(state="disabled")

        self.intro_button_1 = customtkinter.CTkButton(master=self.intro_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.intro_button_event)
        self.intro_button_1.grid(row=3, column=2, padx=(20, 20), pady=(20, 20), sticky="s")


        # After Introduction Frame Load Data Analysis Class
        self.IdealHomeDataAnalysis = IdealHomeDataAnalysis()
        state_keys = sorted([*self.IdealHomeDataAnalysis.zipcode_coordinate_data.keys()])

        """ 
            Family Location Frame 1
        """
        self.family_location_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.family_location_frame.grid_rowconfigure(10, weight=1)
        self.family_location_frame.grid_columnconfigure(0, weight=1)

        self.family_location_label = customtkinter.CTkLabel(self.family_location_frame, text="Ideal Family Preferences", font=title_font)
        self.family_location_label.grid(row=0, column=0, columnspan=3, padx=20, pady=(20, 15), sticky='')


        self.family_location_label1 = customtkinter.CTkLabel(self.family_location_frame, text="Do you want to be close to family members?", font=large_font)
        self.family_location_label1.grid(row=1, column=0, columnspan=3, padx=40, pady=(20, 15), sticky='')

        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.family_location_frame, font=regular_font, command=self.seg_button_family_location)
        self.seg_button_1.grid(row=2, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.seg_button_1.configure(values=["Yes", "No"])
        self.seg_button_1.set("Yes")

        # Family Location Entry Frame 1
        self.family_location_entry_frame1 = customtkinter.CTkFrame(self.family_location_frame, corner_radius=0)
        self.family_location_entry_frame1.grid(row=3, column=0, columnspan=3, sticky="nsew")
        self.family_location_entry_frame1.grid_rowconfigure(10, weight=1)
        self.family_location_entry_frame1.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.f_location_label1 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="Please enter the location of the family member:", font=large_font)
        self.f_location_label1.grid(row=0, column=0, columnspan=4, padx=40, pady=12, sticky='')

        self.f_location_label2 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="City:", font=large_font)
        self.f_location_label2.grid(row=1, column=0, padx=60, pady=12, sticky='n')

        self.f_location_label3 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="State:", font=large_font)
        self.f_location_label3.grid(row=1, column=1, padx=40, pady=12, sticky='n')

        self.f_location_label4 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="Zipcode:", font=large_font)
        self.f_location_label4.grid(row=1, column=2, padx=40, pady=12, sticky='n')


        self.family_location_entry1 = customtkinter.CTkEntry(self.family_location_entry_frame1, width=250, placeholder_text='City')
        self.family_location_entry1.grid(row=2, column=0, padx=40, pady=12, sticky='n')

        self.family_location_entry2 = customtkinter.CTkEntry(self.family_location_entry_frame1, placeholder_text='State')
        self.family_location_entry2.grid(row=2, column=1, padx=40, pady=12, sticky='n')

        self.family_location_entry3 = customtkinter.CTkEntry(self.family_location_entry_frame1, placeholder_text='Zipcode')
        self.family_location_entry3.grid(row=2, column=2, padx=40, pady=12, sticky='n')

        self.f_location_button_1 = customtkinter.CTkButton(master=self.family_location_entry_frame1, text='Verify', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font)
        self.f_location_button_1.grid(row=2, column=3, padx=(20, 20), pady=12, sticky="n")

        self.f_location_label5 = customtkinter.CTkLabel(self.family_location_entry_frame1, text="I", font=large_font)
        self.f_location_label5.grid(row=3, column=1, padx=40, pady=12, sticky='')

        self.f_location_button_2 = customtkinter.CTkButton(master=self.family_location_entry_frame1, text='Confirm', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font)
        self.f_location_button_2.grid(row=3, column=2, padx=(20, 20), pady=12, sticky="")


        self.family_location_label2 = customtkinter.CTkLabel(self.family_location_frame, text="Additional Location?", font=large_font)
        self.family_location_label2.grid(row=4, column=0, columnspan=3, pady=10, padx=20, sticky="")

        self.seg_button_2 = customtkinter.CTkSegmentedButton(self.family_location_frame, font=regular_font, command=self.seg_button_family_location_2)
        self.seg_button_2.grid(row=5, column=0, columnspan=3, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.seg_button_2.configure(values=["Yes", "No"])
        self.seg_button_2.set("Yes")

        # Family Location Entry Frame 2
        self.family_location_entry_frame2 = customtkinter.CTkFrame(self.family_location_frame, corner_radius=0)
        self.family_location_entry_frame2.grid(row=6, column=0, columnspan=3, sticky="nsew")
        self.family_location_entry_frame2.grid_rowconfigure(10, weight=1)
        self.family_location_entry_frame2.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.f2_location_label1 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="Please enter the location of the family member:", font=large_font)
        self.f2_location_label1.grid(row=0, column=0, columnspan=4, padx=40, pady=12, sticky='')

        self.f2_location_label2 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="City:", font=large_font)
        self.f2_location_label2.grid(row=1, column=0, padx=60, pady=12, sticky='n')

        self.f2_location_label3 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="State:", font=large_font)
        self.f2_location_label3.grid(row=1, column=1, padx=40, pady=12, sticky='n')

        self.f2_location_label4 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="Zipcode:", font=large_font)
        self.f2_location_label4.grid(row=1, column=2, padx=40, pady=12, sticky='n')


        self.family_location_entry4 = customtkinter.CTkEntry(self.family_location_entry_frame2, width=250, placeholder_text='City')
        self.family_location_entry4.grid(row=2, column=0, padx=40, pady=12, sticky='n')

        self.family_location_entry5 = customtkinter.CTkEntry(self.family_location_entry_frame2, placeholder_text='State')
        self.family_location_entry5.grid(row=2, column=1, padx=40, pady=12, sticky='n')

        self.family_location_entry6 = customtkinter.CTkEntry(self.family_location_entry_frame2, placeholder_text='Zipcode')
        self.family_location_entry6.grid(row=2, column=2, padx=40, pady=12, sticky='n')

        self.f2_location_button_1 = customtkinter.CTkButton(master=self.family_location_entry_frame2, text='Verify', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font)
        self.f2_location_button_1.grid(row=2, column=3, padx=(20, 20), pady=12, sticky="n")

        self.f2_location_label5 = customtkinter.CTkLabel(self.family_location_entry_frame2, text="I", font=large_font)
        self.f2_location_label5.grid(row=3, column=1, padx=40, pady=12, sticky='')

        self.f2_location_button_2 = customtkinter.CTkButton(master=self.family_location_entry_frame2, text='Confirm', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font)
        self.f2_location_button_2.grid(row=3, column=2, padx=(20, 20), pady=12, sticky="")


        self.family_location_button_1 = customtkinter.CTkButton(master=self.family_location_frame, text='Next', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_forward_event)
        self.family_location_button_1.grid(row=11, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_location_button_2 = customtkinter.CTkButton(master=self.family_location_frame, text='Previous', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1_backward_event)
        self.family_location_button_2.grid(row=11, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")
        

        """ 
            Family Details Frame 1b
        """
        self.family_details_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.family_details_frame.grid_rowconfigure(11, weight=1)
        self.family_details_frame.grid_columnconfigure(0, weight=1)

        self.family_details_label = customtkinter.CTkLabel(self.family_details_frame, text="Ideal Family Preferences", font=title_font)
        self.family_details_label.grid(row=0, column=0, padx=20, columnspan=4, pady=(20, 15), sticky='')


        self.family_details_label1 = customtkinter.CTkLabel(self.family_details_frame, text="Are you single or married?", font=large_font)
        self.family_details_label1.grid(row=1, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_1 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=regular_font)
        self.family_details_seg_button_1.grid(row=2, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_1.configure(values=["Single", "Married"])
        self.family_details_seg_button_1.set("Single")


        self.family_details_label2 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to be around people with the same relationship status as you?", font=large_font)
        self.family_details_label2.grid(row=3, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_2 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=regular_font)
        self.family_details_seg_button_2.grid(row=4, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_2.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_2.set("3")


        self.family_details_label3 = customtkinter.CTkLabel(self.family_details_frame, text="Do you have children?", font=large_font)
        self.family_details_label3.grid(row=5, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')


        self.family_details_seg_button_3 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=regular_font)
        self.family_details_seg_button_3.grid(row=6, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_3.configure(values=["Yes", "No"])
        self.family_details_seg_button_3.set("Yes")

        self.family_details_label4 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to be around people with the same family status as you?", font=large_font)
        self.family_details_label4.grid(row=7, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_4 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=regular_font)
        self.family_details_seg_button_4.grid(row=8, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_4.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_4.set("3")

        self.family_details_label5 = customtkinter.CTkLabel(self.family_details_frame, text="How important is it to have a large percent of the children enrolled in school?", font=large_font)
        self.family_details_label5.grid(row=9, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.family_details_seg_button_5 = customtkinter.CTkSegmentedButton(self.family_details_frame, font=regular_font)
        self.family_details_seg_button_5.grid(row=10, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.family_details_seg_button_5.configure(values=["1", "2", "3", "4", "5"])
        self.family_details_seg_button_5.set("3")

        self.family_details_button_1 = customtkinter.CTkButton(master=self.family_details_frame, text='Next', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1b_forward_event)
        self.family_details_button_1.grid(row=12, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.family_details_button_2 = customtkinter.CTkButton(master=self.family_details_frame, text='Previous', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_1b_backward_event)
        self.family_details_button_2.grid(row=12, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")
        

        """ 
            Work Location Frame 2
        """
        self.work_location_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.work_location_frame.grid_rowconfigure(3, weight=1)
        self.work_location_frame.grid_columnconfigure(0, weight=1)

        self.work_location_label = customtkinter.CTkLabel(self.work_location_frame, text="Ideal Work Preferences", font=title_font)
        self.work_location_label.grid(row=1, column=0, padx=20, columnspan=4, pady=(20, 15), sticky='')

        self.work_location_label1 = customtkinter.CTkLabel(self.work_location_frame, text="Input 1 or 2 Work Locations:", font=regular_font)
        self.work_location_label1.grid(row=2, column=0, padx=40, pady=(20, 15), sticky='')

        self.work_location_button_1 = customtkinter.CTkButton(master=self.work_location_frame, text='Next', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_2_forward_event)
        self.work_location_button_1.grid(row=10, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.work_location_button_2 = customtkinter.CTkButton(master=self.work_location_frame, text='Previous', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_2_backward_event)
        self.work_location_button_2.grid(row=10, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        
        """ 
            Work Details Frame 2b
        """
        self.work_details_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.work_details_frame.grid_rowconfigure(10, weight=1)
        self.work_details_frame.grid_columnconfigure(0, weight=1)

        self.work_details_label = customtkinter.CTkLabel(self.work_details_frame, text="Ideal Work Preferences", font=title_font)
        self.work_details_label.grid(row=0, column=0, padx=20, columnspan=3, pady=(20, 15), sticky='')


        self.work_details_label1 = customtkinter.CTkLabel(self.work_details_frame, text="Are you single or married?", font=large_font)
        self.work_details_label1.grid(row=1, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.work_details_seg_button_1 = customtkinter.CTkSegmentedButton(self.work_details_frame, font=regular_font)
        self.work_details_seg_button_1.grid(row=2, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_details_seg_button_1.configure(values=["Single", "Married"])
        self.work_details_seg_button_1.set("Single")


        self.work_details_label2 = customtkinter.CTkLabel(self.work_details_frame, text="How important is it to be around people with the same relationship status as you?", font=large_font)
        self.work_details_label2.grid(row=3, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.work_details_seg_button_2 = customtkinter.CTkSegmentedButton(self.work_details_frame, font=regular_font)
        self.work_details_seg_button_2.grid(row=4, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_details_seg_button_2.configure(values=["1", "2", "3", "4", "5"])
        self.work_details_seg_button_2.set("3")


        self.work_details_label3 = customtkinter.CTkLabel(self.work_details_frame, text="Do you have children?", font=large_font)
        self.work_details_label3.grid(row=5, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')


        self.work_details_seg_button_3 = customtkinter.CTkSegmentedButton(self.work_details_frame, font=regular_font)
        self.work_details_seg_button_3.grid(row=6, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_details_seg_button_3.configure(values=["Yes", "No"])
        self.work_details_seg_button_3.set("Yes")

        self.work_details_label4 = customtkinter.CTkLabel(self.work_details_frame, text="How important is it to be around people with the same family status as you?", font=large_font)
        self.work_details_label4.grid(row=7, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.work_details_seg_button_4 = customtkinter.CTkSegmentedButton(self.work_details_frame, font=regular_font)
        self.work_details_seg_button_4.grid(row=8, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_details_seg_button_4.configure(values=["1", "2", "3", "4", "5"])
        self.work_details_seg_button_4.set("3")

        self.work_details_label5 = customtkinter.CTkLabel(self.work_details_frame, text="How important is it to have a large percent of the children enrolled in school?", font=large_font)
        self.work_details_label5.grid(row=9, column=0, columnspan=4, padx=40, pady=(20, 15), sticky='')

        self.work_details_seg_button_5 = customtkinter.CTkSegmentedButton(self.work_details_frame, font=regular_font)
        self.work_details_seg_button_5.grid(row=10, column=0, columnspan=4, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.work_details_seg_button_5.configure(values=["1", "2", "3", "4", "5"])
        self.work_details_seg_button_5.set("3")

        self.work_details_button_1 = customtkinter.CTkButton(master=self.work_details_frame, text='Next', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_2b_forward_event)
        self.work_details_button_1.grid(row=11, column=2, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.work_details_button_2 = customtkinter.CTkButton(master=self.work_details_frame, text='Previous', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_2b_backward_event)
        self.work_details_button_2.grid(row=11, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        
        """ 
            Income Metrics Frame 3
        """
        self.income_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.income_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.income_frame.grid_rowconfigure(3, weight=1)
        self.income_frame.grid_columnconfigure(0, weight=1)

        self.income_label = customtkinter.CTkLabel(self.income_frame, text="Current Income Information", font=title_font)
        self.income_label.grid(row=1, column=0, padx=20, columnspan=4, pady=(20, 15), sticky='')


        self.income_label1 = customtkinter.CTkLabel(self.income_frame, text="What is your current household income?:", font=regular_font)
        self.income_label1.grid(row=2, column=0, padx=40, pady=(20, 15), sticky='')

        self.income_button_1 = customtkinter.CTkButton(master=self.income_frame, text='Next', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_3_forward_event)
        self.income_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.income_button_2 = customtkinter.CTkButton(master=self.income_frame, text='Previous', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_3_backward_event)
        self.income_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        
        """ 
            Area Classification Frame 4
        """
        self.area_classification_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.area_classification_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.area_classification_frame.grid_rowconfigure(3, weight=1)
        self.area_classification_frame.grid_columnconfigure(0, weight=1)

        self.area_classification_label = customtkinter.CTkLabel(self.area_classification_frame, text="Ideal Lifestyle Preferences", font=title_font)
        self.area_classification_label.grid(row=1, column=0, padx=20, columnspan=4, pady=(20, 15), sticky='')

        self.area_classification_button_1 = customtkinter.CTkButton(master=self.area_classification_frame, text='Next', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_4_forward_event)
        self.area_classification_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.area_classification_button_2 = customtkinter.CTkButton(master=self.area_classification_frame, text='Previous', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_4_backward_event)
        self.area_classification_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        """ 
            Weather Metrics Frame 5
        """
        self.weather_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.weather_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.weather_frame.grid_rowconfigure(3, weight=1)
        self.weather_frame.grid_columnconfigure(0, weight=1)

        self.weather_label = customtkinter.CTkLabel(self.weather_frame, text="Weather & Temperature Preferences", font=title_font)
        self.weather_label.grid(row=1, column=0, padx=20, columnspan=4, pady=(20, 15), sticky='')

        self.weather_button_1 = customtkinter.CTkButton(master=self.weather_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_5_forward_event)
        self.weather_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.weather_button_2 = customtkinter.CTkButton(master=self.weather_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_5_backward_event)
        self.weather_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")
        
        """ 
            Natural Disaster Risk Frame 6
        """
        self.natural_disaster_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.natural_disaster_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.natural_disaster_frame.grid_rowconfigure(3, weight=1)
        self.natural_disaster_frame.grid_columnconfigure(0, weight=1)

        self.natural_disaster_label = customtkinter.CTkLabel(self.natural_disaster_frame, text="Natural Disaster Risk Tolerance", font=title_font)
        self.natural_disaster_label.grid(row=1, column=0, padx=20, columnspan=4, pady=(20, 15), sticky='')

        self.natural_disaster_button_1 = customtkinter.CTkButton(master=self.natural_disaster_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_6_forward_event)
        self.natural_disaster_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="s")
     
        self.natural_disaster_button_2 = customtkinter.CTkButton(master=self.natural_disaster_frame, text='Get Started', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_6_backward_event)
        self.natural_disaster_button_2.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        """ 
            Results Frame 7
        """
        self.results_frame = customtkinter.CTkFrame(self, corner_radius=0)
        #self.natural_disaster_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.results_frame.grid_rowconfigure(3, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)


        self.results_button_1 = customtkinter.CTkButton(master=self.results_frame, text='Previous', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_7_backward_event)
        self.results_button_1.grid(row=3, column=0, padx=(20, 20), pady=(20, 20), sticky="sw")

        self.results_button_2 = customtkinter.CTkButton(master=self.results_frame, text='Restart', border_width=2, text_color=("gray10", "#DCE4EE"), font=regular_font, command=self.frame_7_restart_event)
        self.results_button_2.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="sw")


    def seg_button_family_location(self, param: str):
        print(param)

    def seg_button_family_location_2(self, param: str):
        print(param)

    # ----------------------- Navigation Buttons ---------------------------

    def intro_button_event(self):
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
        self.income_frame.grid_forget()
        self.area_classification_frame.grid(row=1, column=0, rowspan=3, columnspan=3, sticky="nsew")
        self.progressbar.set(.66)

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
