"""GUI module."""

#Native Modules:
from tkinter import ttk, messagebox
#from PIL import Image, ImageTk
import tkinter as tk
import subprocess
import webbrowser
#import threading
import re

#External Modules:
from selenium import webdriver

#Internal Modules:
from HAF.GUI.CallHandler.CallEditor import NewCall
from HAF.Constants import Paths, GUIConstants, URL
from HAF.FileHandler.JsonHandler import LoadJson
from HAF.FileHandler.Config import ConfigClass
from HAF import __version__ as HAFVersion


class GUI(tk.Tk):
    """
    Graphical User Interface Class.\n
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Private Attributes:
        - __config: A loaded ConfigClass object.
        - __driver: A loaded Chrome webdriver object.
        - __exit_value: An integer that is returned when GUI closes, exit codes bellow.
        - __lang: A loaded language resource.
        - __auto_open_flag: A boolean indicating whether or not the GUI should auto-start at program execution.
        - __StatusBar: Initialized StatusBar object.
        - __CallTab: Initialized Calltab object.
        - __TemplateTab: Initialized TemplateTab object.

    Exit Codes:
        - 0: Standard exit sequence.
        - 1: Full exit sequence.
        - 2: Restart sequence.
    """
    
    def __init__(self, config:ConfigClass, driver:webdriver.Chrome) -> None:
        """
        Creates a new GUI object, use :mod:`foo.Start()` to start the main loop.

        Arguments:
            - config: A loaded ConfigClass object.
            - driver: A loaded Chrome webdriver object.

        Dependencies:
            - :mod:`__CreateWidgets()`: For tkinter widget creation.
        """
        
        super().__init__()

        self.__driver = driver
        self.__config = config

        self.__exit_value = int(0) #Refer to exit codes documented bellow class definition.
        self.__lang = LoadJson(Paths.RESOURCES_FOLDER_PATH + self.__config.GetLanguage + '.json')
        self.__auto_open_flag = tk.IntVar(); self.__auto_open_flag.set(self.__config.AutoOpenStatus)

        self.title('HAF ' + HAFVersion)
        self.geometry('800x620')
        self.resizable(width = False, height = False)

        self.__CreateWidgets()


    def Start(self) -> bool:
        """
        Starts main screen main loop.

        Returns an integer stored in 'self.__exit_value' that indicates how to program was closed.
        """

        self.mainloop()
        return self.__exit_value


    def Restart(self) -> None:
        """Finishes main loop with exit value of 2 (Restart)."""

        self.__exit_value = 2
        self.destroy()


    def __Exit(self) -> None:
        """
        Private Method:
        Finishes main loop with exit value of 1 (Close).
        """

        self.__exit_value = 1
        self.destroy()


    def __CreateWidgets(self) -> None:
        """
        Private Method:
        Loads widgets for the main screen.
        
        Dependencies:
            - :mod:`__Exit()` for exit sequence.
        """

        #Menu bar configuration:
        menu_bar = tk.Menu(self)

        #'File' menu configuration:
        file_menu = tk.Menu(menu_bar, tearoff = False)
        configure_submenu = tk.Menu(menu_bar, tearoff = False)
        file_menu.add_cascade( #'Configure...' submenu.
            label = self.__lang['Labels']['File_Label']['Configure']['Title'],
            menu = configure_submenu
        )
        ##'Configure' sub-menu configuration:
        configure_submenu.add_command( #'Microsoft Account Configuration' option.
            label = self.__lang['Labels']['File_Label']['Configure']['Microsoft_Acc'],
            command = lambda: AccountConfiguration(self, self.__lang, self.__config).Start()
        )
        configure_submenu.add_command( #'Language' option.
            label = self.__lang['Labels']['File_Label']['Configure']['Language'],
            command = lambda: LanguageConfiguration(self, self.__lang, self.__config).Start()
        )
        configure_submenu.add_checkbutton( #Auto open Checkbutton.
            label = self.__lang['Labels']['File_Label']['Configure']['AutoOpen'],
            selectcolor = 'lightgreen',
            variable = self.__auto_open_flag,
            offvalue = 0,
            onvalue = 1,
            command = lambda: self.__config.UpdateAutoOpenFlag(bool(self.__auto_open_flag.get()))
        )
        file_menu.add_command( #'Open logs' option.
            label = self.__lang['Labels']['File_Label']['Open_Logs'],
            command = lambda: subprocess.Popen('explorer /open, ' + Paths.LOG_TXT_PATH)
        )
        file_menu.add_separator()
        file_menu.add_command( #'Exit' option.
            label = self.__lang['Labels']['File_Label']['Exit'],
            command = self.__Exit
        )

        #'Help' menu configuration:
        help_menu = tk.Menu(menu_bar, tearoff = False)
        help_menu.add_command( #'About' option.
            label = self.__lang['Labels']['Help_Label']['About'],
            command = lambda: webbrowser.open(URL.ABOUT_PROJECT_URL, autoraise = True)
        )

        #Menu bar definition:
        menu_bar.add_cascade(label = self.__lang['Labels']['File_Label']['Title'], menu = file_menu)
        menu_bar.add_cascade(label = self.__lang['Labels']['Help_Label']['Title'], menu = help_menu)
        self.config(menu = menu_bar)


        #Status bar:
        self.__StatusBar = StatusBar(self, self.__lang)


        #Tab configuration:
        tab_control = ttk.Notebook(self)
        tab_control.pack(expand = True, fill = 'both')

        self.__CallTab = CallTab(self.__driver, self.__StatusBar, tab_control, self.__lang)
        tab_control.add(self.__CallTab, text = self.__lang['Tabs']['CallTab'])

        self.__TemplateTab = TemplateTab(tab_control, self.__lang)
        tab_control.add(self.__TemplateTab, text = self.__lang['Tabs']['TemplateTab'])


class StatusBar(tk.Frame): #TODO
    """"""

    def __init__(self, parent:GUI, selected_language:dict) -> None:
        """"""
        
        super().__init__()

        self.__lang = selected_language

        self.master = parent

        self.__CreateWidgets()

    
    def __CreateWidgets(self) -> None:
        """Creates status bar widgets."""

        self.config(background = GUIConstants.COLOR_CUSTOM_BLUE)
        self.pack(side = tk.BOTTOM, fill = tk.X)

        #Text:
        self.__text = tk.Label(
            self,
            text = self.__lang['Text_Labels']['Idle'],
            background = GUIConstants.COLOR_CUSTOM_BLUE,
            foreground = 'white'
        )
        self.__text.pack(
            side = tk.LEFT,
            padx = 10
        )

        #Buffering icon:
        frame_count = 8
        buffering_frames = [
            tk.PhotoImage(
                file = Paths.BUFFERING_GIF,
                format = 'gif -index %i' % (i)
            ) for i in range(frame_count)
        ]
        
        icon_canvas = tk.Canvas(
            self,
            height = 25,
            width = 25,
            background = GUIConstants.COLOR_CUSTOM_BLUE,
            highlightthickness = 0
        )
        icon_canvas.pack(
            side = tk.RIGHT,
            padx = 10,
            pady = 2
        )
        #icon_canvas.create_image(, y, image = buffering_frames[0], anchor = tk.NE)


    def ChangeText(self, string:str = 'Default Message') -> None:
        """
        Changes status bar text.

        Optional Arguments:
            - string: A new string to be displayed, dafaults to 'Idle' message.
        """
        
        if string == 'Default Message':
            string = self.__lang['Text_Labels']['Idle']
        self.__text.config(text = string)


    def ShowBuffering(self, flag:bool) -> None: #TODO: IMPLEMENT
        """
        Configures status bar buffering icon.

        Arguments:
            - flag: A bool indicating whether the buffering icon should be turned on or off.
        """

        if flag:
            return
        else:
            return


class CallTab(ttk.Frame): #TODO: Document / Threading
    """"""

    def __init__(self, driver:webdriver.Chrome, statusbar:StatusBar, FatherTab:ttk.Notebook, selected_language:dict) -> None: #TODO: Document
        """"""

        super().__init__()

        self.__driver = driver
        self.__statusbar = statusbar
        self.__lang = dict(selected_language)

        self.__call_dictionary = LoadJson(Paths.DICTIONARY_JSON_PATH)
        self.__usernamecash = []

        self.__valid_user_ID_flag = bool(False)
        self.__valid_user_contact_flag = bool(False)
        self.__formatted_user_contact = str('')

        self.master = FatherTab

        self.__CreateWidgets()

    
    def __CreateWidgets(self) -> None: #TODO: Document
        """"""

        #Header Entries.
        ##User ID Entry.
        tk.Label(
            self,
            text = self.__lang['Text_Labels']['User_ID'] + ':'
        ).grid(
            column = 0,
            row = 0,
            padx = 12,
            sticky = tk.NW
        )
        self.__user_ID_error = tk.Label(
            self,
            text = '',
            foreground = 'red'
        )
        self.__user_ID_error.grid(
            column = 0,
            row = 0,
            padx = 12,
            sticky = tk.NE
        )
        self.__user_ID_entry = tk.Entry(
            self,
            width = 30,
            validate = 'focusout',
            validatecommand = (self.register(self.__UserIDValidator), '%P'),
            invalidcommand = lambda: [
                self.__user_ID_entry.config(
                    foreground = 'red'
                ),
                self.__user_ID_error.config(
                    text = self.__lang['Text_Labels']['Invalid_User_ID']
                )
            ]
        )
        self.__user_ID_entry.grid(
            column = 0,
            row = 1,
            padx = 12,
            pady = [0, 10],
            sticky = tk.NW
        )
        self.__user_ID_entry.bind('<FocusIn>', lambda _: [
                self.__user_ID_entry.config(
                    foreground = 'black'
                ),
                self.__user_ID_error.config(
                    text = ''
                )
            ]
        )
        self.__user_ID_entry.bind('<FocusOut>', lambda _: self.__CTVUpdate())
        self.__user_ID_entry.bind('<KeyRelease>', lambda _: self.__CTVUpdate())
        
        ##User Contact Entry.
        tk.Label(
            self,
            text = self.__lang['Text_Labels']['User_Contact'] + ':'
        ).grid(
            column = 1,
            row = 0,
            padx = [0, 12],
            sticky = tk.NW
        )
        self.__user_contact_error = tk.Label(
            self,
            text = '',
            foreground = 'red'
        )
        self.__user_contact_error.grid(
            column = 1,
            row = 0,
            padx = 12,
            sticky = tk.NE
        )
        self.__user_contact_entry = tk.Entry(
            self,
            width = 30,
            validate = 'focusout',
            validatecommand = (self.register(self.__UserContactValidator), '%P'),
            invalidcommand = lambda: [
                self.__user_contact_entry.config(
                    foreground = 'red'
                ),
                self.__user_contact_error.config(
                    text = self.__lang['Text_Labels']['Invalid_User_Contact']
                )
            ]
        )
        self.__user_contact_entry.grid(
            column = 1,
            row = 1,
            padx = [0, 12],
            pady = [0, 10],
            sticky = tk.NW
        )
        self.__user_contact_entry.bind('<FocusIn>', lambda _: [
                self.__user_contact_entry.config(
                    foreground = 'black'
                ),
                self.__user_contact_error.config(
                    text = ''
                )
            ]
        )
        self.__user_contact_entry.bind('<FocusOut>', lambda _: self.__CTVUpdate())
        self.__user_contact_entry.bind('<KeyRelease>', lambda _: [
                self.__UserContactValidator(self.__user_contact_entry.get()),
                self.__CTVUpdate()
            ]
        )
        
        ##User Hostname Entry.
        tk.Label(
            self,
            text = self.__lang['Text_Labels']['User_Hostname'] + ':'
        ).grid(
            column = 2,
            row = 0,
            padx = [0, 12],
            sticky = tk.NW
        )
        self.__user_hostname_entry = tk.Entry(
            self,
            width = 30,
            state = tk.DISABLED
        )
        self.__user_hostname_entry.grid(
            column = 2,
            row = 1,
            padx = [0, 12],
            pady = [0, 10],
            sticky = tk.NW
        )
        self.__user_hostname_entry.bind('<FocusOut>', lambda _: self.__CTVUpdate())
        self.__user_hostname_entry.bind('<KeyRelease>', lambda _: self.__CTVUpdate())
        
        ##Variable Entry.
        tk.Label(
            self,
            text = self.__lang['Text_Labels']['Variable'] + ':'
        ).grid(
            column = 3,
            row = 0,
            padx = [0, 12],
            sticky = tk.NW
        )
        self.__variable_entry = tk.Entry(
            self,
            width = 30,
            state = tk.DISABLED
        )
        self.__variable_entry.grid(
            column = 3,
            row = 1,
            padx = [0, 12],
            pady = [0, 10],
            sticky = tk.NW
        )
        self.__variable_entry.bind('<FocusOut>', lambda _: self.__CTVUpdate())
        self.__variable_entry.bind('<KeyRelease>', lambda _: self.__CTVUpdate())


        #Separator
        ttk.Separator(self).grid(
            column = 0,
            row = 2,
            columnspan = 4,
            sticky = 'we'
        )


        #Call Visualizer.
        self.__CallTabVisualizer()


        #Option Frame Widget.
        self.OptionsFrame = tk.LabelFrame(
            self,
            text = self.__lang['Text_Labels']['Options_Label'],
            font = ('Arial', 10, 'bold'),
            foreground = 'gray'
        )
        self.OptionsFrame.grid(
            column = 0,
            row = 19,
            columnspan = 2,
            rowspan = 2,
            padx = 12,
            pady = 10,
            sticky = tk.NW
        )
        
        ##Ticket Type.
        tk.Label(
            self.OptionsFrame,
            text = self.__lang['Text_Labels']['Ticket_Type'] + ':'
        ).grid(
            column = 0,
            row = 0,
            padx = 12,
            sticky = tk.NE
        )
        self.__ticket_type_options = [str(self.__lang['Text_Labels']['Selection'])] + list(self.__call_dictionary.keys())
        self.__ticket_type_variable = tk.StringVar()
        self.__ticket_type_variable.set(self.__lang['Text_Labels']['Selection'])
        self.__ticket_type_menu = ttk.OptionMenu(
            self.OptionsFrame,
            self.__ticket_type_variable,
            *self.__ticket_type_options,
            direction = 'right',
            command = lambda _: self.__onTicketTypeSelection(self.__call_dictionary[self.__ticket_type_variable.get()])
        )
        self.__ticket_type_menu.grid(
            column = 1,
            row = 0,
            sticky = tk.NW
        )
        self.__ticket_type_menu.bind('<Configure>', lambda _: self.__CTVUpdate())
        
        ##Solution Type.
        tk.Label(
            self.OptionsFrame,
            text = self.__lang['Text_Labels']['Solution_Type'] + ':'
        ).grid(
            column = 0,
            row = 1,
            padx = 12,
            sticky = tk.NE
        )
        self.__solution_type_options = [str(self.__lang['Text_Labels']['Selection'])]
        self.__solution_type_variable = tk.StringVar()
        self.__solution_type_variable.set(self.__lang['Text_Labels']['Selection'])
        self.__solution_type_menu = ttk.OptionMenu(
            self.OptionsFrame,
            self.__solution_type_variable,
            *self.__solution_type_options,
        ); self.__solution_type_menu.config(state = tk.DISABLED)
        self.__solution_type_menu.grid(
            column = 1,
            row = 1,
            sticky = tk.NW
        )
        

        #Clear button.
        tk.Button(
            self,
            text = self.__lang['Buttons']['Clear'],
            height = 4,
            width = 15,
            command = self.__onClearButtonPress
        ).grid(
            column = 2,
            row = 19,
            rowspan = 2,
            padx = 12,
            pady = 10,
            sticky = tk.NE
        )


        #Send button.
        self.__sendbutton = tk.Button(
            self,
            text = self.__lang['Buttons']['Send'],
            height = 4,
            width = 15,
            command = self.__onSendButtonPress,
            state = tk.DISABLED
        )
        self.__sendbutton.grid(
            column = 3,
            row = 19,
            rowspan = 2,
            padx = 12,
            pady = 10,
            sticky = tk.NE
        )


    def __CallTabVisualizer(self) -> None: #TODO: Document
        """"""

        #Visualizer Frame Widget
        PreviewFrame = tk.LabelFrame(
            self,
            text = self.__lang['Text_Labels']['Frame_Label'],
            font = ('Arial', 10, 'bold'),
            background = 'white',
            foreground = 'gray'
        )
        PreviewFrame.grid(
            column = 0,
            row = 3,
            columnspan = 4,
            rowspan = 16,
            padx = 87,
            pady = 10,
            sticky = tk.NW
        )
        ##Ticket Title.
        tk.Label(
            PreviewFrame,
            text = self.__lang['Text_Labels']['Ticket_Title'] + ':',
            background = 'white'
        ).grid(
            column = 0,
            row = 0,
            padx = 87,
            sticky = tk.NW
        )
        self.__VisualizerTitleText = tk.Text(
            PreviewFrame,
            background = GUIConstants.COLOR_CUSTOM_GRAY,
            font = ('Helvetica', 15),
            state = 'disabled',
            height = 1,
            width = 40
        )
        self.__VisualizerTitleText.grid(
            column = 0,
            row = 1,
            padx = 87,
            pady = [0, 25],
            sticky = tk.NW
        )
        ##Ticket Body.
        tk.Label(
            PreviewFrame,
            text = self.__lang['Text_Labels']['Ticket_Body'] + ':',
            background = 'white'
        ).grid(
            column = 0,
            row = 2,
            padx = 87,
            sticky = tk.NW
        )
        self.__VisualizerBodyText = tk.Text(
            PreviewFrame,
            background = GUIConstants.COLOR_CUSTOM_GRAY,
            font = ('Helvetica', 15),
            state = 'disabled',
            height = 6,
            width = 40
        )
        self.__VisualizerBodyText.grid(
            column = 0,
            row = 3,
            rowspan = 6,
            padx = 87,
            pady = [0, 25],
            sticky = tk.NW
        )
        ##Ticket Solution.
        tk.Label(
            PreviewFrame,
            text = self.__lang['Text_Labels']['Ticket_Solution'] + ':',
            background = 'white'
        ).grid(
            column = 0,
            row = 9,
            padx = 87,
            sticky = tk.NW
        )
        self.__VisualizerSolutionText = tk.Text(
            PreviewFrame,
            background = GUIConstants.COLOR_CUSTOM_GRAY,
            font = ('Helvetica', 15),
            state = 'disabled',
            height = 3,
            width = 40
        )
        self.__VisualizerSolutionText.grid(
            column = 0,
            row = 10,
            rowspan = 2,
            padx = 87,
            pady = [0, 25],
            sticky = tk.NW
        )


    def __UserIDValidator(self, string:str) -> bool:
        """
        Private Method:
        Checks if string is a valid user ID.

        Returns true if strig a valid user ID, false otherwise.

        Arguments:
            - string: String to be validated.
        """
        
        self.__valid_user_ID_flag = False
        if string and len(string) == 10:
            if string in self.__usernamecash:
                self.__valid_user_ID_flag = True
                return self.__valid_user_ID_flag

            p = subprocess.Popen(
                f'net user /domain {string}',
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
            error = p.stderr.read()

            if not error:
                self.__usernamecash.append(str(string))
                self.__valid_user_ID_flag = True
        return self.__valid_user_ID_flag


    def __UserContactValidator(self, string:str) -> bool: #TODO: Document
        """"""

        self.__valid_user_contact_flag = False
        if string.isnumeric():
            valid_sizes = [6, 10, 11]
            if len(string) in valid_sizes:
                self.__valid_user_contact_flag = True
        return self.__valid_user_contact_flag


    def __onTicketTypeSelection(self, dictionary:dict) -> None: #TODO: Document
        """"""

        if dictionary['Needs_Hostname']:
            self.__user_hostname_entry.config(state = tk.NORMAL)
        else:
            self.__user_hostname_entry.delete('0', tk.END)
            self.__user_hostname_entry.config(state = tk.DISABLED)

        if dictionary['Needs_Variable']:
            self.__variable_entry.config(state = tk.NORMAL)
        else:
            self.__variable_entry.delete('0', tk.END)
            self.__variable_entry.config(state = tk.DISABLED)
        
        if dictionary['Process-Type'] == 'close': #Updates solution menu for 'close' ticket types.
            #Makes a numeric list for every answer availate for the ticket template.
            numberlist = [str(self.__lang['Text_Labels']['Selection'])]
            for i in range (0, len(list(dictionary['Answer']))):
                numberlist.append(str(i))
            self.__solution_type_options = numberlist
            self.__solution_type_variable.set(self.__lang['Text_Labels']['Selection'])

            #Recreates solution selection widget (editing it causes undefined behaviour).
            self.__solution_type_menu.destroy()
            self.__solution_type_menu = ttk.OptionMenu(
                self.OptionsFrame,
                self.__solution_type_variable,
                *self.__solution_type_options,
                direction = 'right',
                command = lambda _: self.__CTVUpdate()
            )
            self.__solution_type_menu.grid(
            column = 1,
            row = 1,
            sticky = tk.NW
            )
        else: #The process type is not 'close', resets solution menu to default settings.
            self.__solution_type_options = [str(self.__lang['Text_Labels']['Selection'])]
            self.__solution_type_variable.set(self.__solution_type_options[0])
            self.__solution_type_menu.config(state = tk.DISABLED)

        self.__SendButtonUpdate()


    def __PhoneNumberFormatter(self, input_string:str) -> str:
        """
        Private Method:
        Formats phone number (e.g. '(12) 9 1234 - 5678' | 
        '(12) 1234 - 5678' | '(12) 1234').
        
        Return:
            - A string with the formatted number.
            - Raw input if not a valid number.
        
        Arguments:
            - input_string: String to be formatted.
        """

        result_string = ''

        if self.__valid_user_contact_flag:
                match len(input_string):
                    case 6: #Branch Line.
                        result_string = (
                            '(' + input_string[:2] + ') ' +
                            input_string[2:]
                        )
                    case 10: #Land line.
                        result_string = (
                            '(' + input_string[:2] + ') ' +
                            input_string[2:6] +
                            ' - ' +
                            input_string[6:]
                        )
                    case 11: #Phone Number.
                        result_string = (
                            '(' + input_string[:2] + ') ' +
                            input_string[2] + ' ' +
                            input_string[3:7] +
                            ' - ' +
                            input_string[7:]
                        )
        else:
            result_string = input_string
        
        return result_string

    
    def __CTVUpdate(self) -> None: #TODO: Document
        """"""

        if self.__ticket_type_variable.get() != self.__lang['Text_Labels']['Selection']:
            dictionary = self.__call_dictionary[self.__ticket_type_variable.get()]

            #Visualizer ticket title update.
            try:
                self.__VisualizerTitleText.config(state = tk.NORMAL)
                self.__VisualizerTitleText.delete('1.0', tk.END)
                self.__VisualizerTitleText.insert(tk.END, str(dictionary['Title']).format(
                    Variable = self.__variable_entry.get()
                ))
                self.__VisualizerTitleText.config(state = tk.DISABLED)
                self.__VisualizerTitleText.config(foreground = 'black')
            except KeyError:
                self.__VisualizerTitleText.config(state = tk.NORMAL)
                self.__VisualizerTitleText.delete('1.0', tk.END)
                self.__VisualizerTitleText.insert(tk.END, self.__lang['Messages']["Does_Not_Apply"])
                self.__VisualizerTitleText.config(state = tk.DISABLED)
                self.__VisualizerTitleText.config(foreground = 'red')
            
            #Visualizer ticket body update.
            self.__formatted_user_contact = self.__PhoneNumberFormatter(self.__user_contact_entry.get()) #Calls for contact number fomatter.
            self.__VisualizerBodyText.config(state = tk.NORMAL)
            self.__VisualizerBodyText.delete('1.0', tk.END)
            self.__VisualizerBodyText.insert(tk.END, str(dictionary['Body']).format(
                User_ID = self.__user_ID_entry.get(),
                Contact = self.__formatted_user_contact,
                Hostname = self.__user_hostname_entry.get(),
                Variable = self.__variable_entry.get()
            ))
            self.__VisualizerBodyText.config(state = tk.DISABLED)

            #Visualizer ticket solution update.
            if dictionary['Process-Type'] == 'close':
                if self.__solution_type_variable.get() != self.__lang['Text_Labels']['Selection']:
                    self.__VisualizerSolutionText.config(state = tk.NORMAL)
                    self.__VisualizerSolutionText.delete('1.0', tk.END)
                    self.__VisualizerSolutionText.insert(
                        tk.END,
                        str(dictionary['Answer'][int(self.__solution_type_variable.get())]).format(
                            Variable = self.__variable_entry.get()
                        )
                    )
                    self.__VisualizerSolutionText.config(state = tk.DISABLED)
                    self.__VisualizerSolutionText.config(foreground = 'black')
                else:
                    self.__VisualizerSolutionText.config(state = tk.NORMAL)
                    self.__VisualizerSolutionText.delete('1.0', tk.END)
                    self.__VisualizerSolutionText.insert(tk.END, self.__lang['Messages']["Missing_Selection"])
                    self.__VisualizerSolutionText.config(state = tk.DISABLED)
                    self.__VisualizerSolutionText.config(foreground = 'red')
            else:
                self.__VisualizerSolutionText.config(state = tk.NORMAL)
                self.__VisualizerSolutionText.delete('1.0', tk.END)
                self.__VisualizerSolutionText.insert(tk.END, self.__lang['Messages']["Does_Not_Apply"])
                self.__VisualizerSolutionText.config(state = tk.DISABLED)
                self.__VisualizerSolutionText.config(foreground = 'red')
        
            self.__SendButtonUpdate()


    def __onClearButtonPress(self) -> None:
        """
        Private Method:
        Resets all 'call' tab widgets to their default state.

        Dependencies:
            - :mod:` __SendButtonUpdate()`: For send button reset.
        """

        #Resets solution type menu:
        self.__solution_type_options = [str(self.__lang['Text_Labels']['Selection'])]
        self.__solution_type_variable.set(self.__solution_type_options[0])
        self.__solution_type_menu.config(state = tk.DISABLED)

        #Resets ticket type menu:
        self.__ticket_type_variable.set(self.__ticket_type_options[0])

        #Resets user input:
        self.__valid_user_ID_flag
        self.__valid_user_contact_flag
        self.__user_ID_entry.delete('0', tk.END)
        self.__user_ID_error.config(text = '')
        self.__user_contact_entry.delete('0', tk.END)
        self.__user_contact_error.config(text = '')
        self.__user_hostname_entry.delete('0', tk.END)
        self.__user_hostname_entry.config(state = tk.DISABLED)
        self.__variable_entry.delete('0', tk.END)
        self.__variable_entry.config(state = tk.DISABLED)
        self.__formatted_user_contact = ''

        #Resets preview:
        self.__VisualizerTitleText.config(state = tk.NORMAL)
        self.__VisualizerTitleText.delete('1.0', tk.END)
        self.__VisualizerTitleText.config(state = tk.DISABLED)
        self.__VisualizerBodyText.config(state = tk.NORMAL)
        self.__VisualizerBodyText.delete('1.0', tk.END)
        self.__VisualizerBodyText.config(state = tk.DISABLED)
        self.__VisualizerSolutionText.config(state = tk.NORMAL)
        self.__VisualizerSolutionText.delete('1.0', tk.END)
        self.__VisualizerSolutionText.config(state = tk.DISABLED)

        #Resets send button:
        self.__SendButtonUpdate()


    def __SendButtonUpdate(self) -> None:
        """
        Private Method:
        Changes 'send' button state.
        """

        ticket_type = self.__ticket_type_variable.get()

        if(
            self.__valid_user_ID_flag and
            self. __valid_user_contact_flag and
            ticket_type != self.__lang['Text_Labels']['Selection']
        ): #User ID and user contact are valid and ticktet type is selected.
            if(
                self.__call_dictionary[ticket_type]['Process-Type'] != 'close' or
                self.__call_dictionary[ticket_type]['Process-Type'] == 'close' and
                self.__solution_type_variable.get() != self.__lang['Text_Labels']['Selection']
            ): #Ticket type is 'close' and solution type is selected or ticket type is not 'close' (does not need solution type).
                if(
                    not self.__call_dictionary[ticket_type]['Needs_Hostname'] or
                    self.__call_dictionary[ticket_type]['Needs_Hostname'] and
                    self.__user_hostname_entry.get()
                ): #Ticket template needs hostname and 'user hostname' entry has a valid hostname or ticket template does not need a hostname.
                    if(
                        not self.__call_dictionary[ticket_type]['Needs_Variable'] or
                        self.__call_dictionary[ticket_type]['Needs_Variable'] and
                        self.__variable_entry.get()
                    ): #Ticket template needs variable and variable entry has text or ticket template does not need a variable.
                        self.__sendbutton.config(state = tk.NORMAL)
                        return
        self.__sendbutton.config(state = tk.DISABLED)


    def __onSendButtonPress(self) -> None: #TODO: Document / Therading
        """"""

        if self.__UserIDValidator(self.__user_ID_entry.get()):
            self.__statusbar.ChangeText(self.__lang['Text_Labels']['Registering'])
            self.__sendbutton.config(state = tk.DISABLED)

            call_type = self.__ticket_type_variable.get()
            
            if self.__call_dictionary[call_type]['Needs_Hostname']:
                hostname = self.__user_hostname_entry.get()
            else:
                hostname = 'Not Required'

            if self.__call_dictionary[call_type]['Process-Type'] == 'close':
                solution = int(self.__solution_type_variable.get())
            else:
                solution = 0

            if self.__call_dictionary[call_type]['Needs_Variable']:
                variable = self.__variable_entry.get()
            else:
                variable = 'Not Required'

            print('\nHAF> call register')
            NewCall(
                self.__driver,
                self.__user_ID_entry.get(),
                self.__formatted_user_contact,
                hostname,
                call_type,
                solution,
                variable
            )

            messagebox.showinfo('HAF', self.__lang['Messages']['Call_Register'])
            self.__statusbar.ChangeText()

            self.__onTicketTypeSelection(self.__call_dictionary[self.__ticket_type_variable.get()])
            self.__CTVUpdate()
        else:
            self.__SendButtonUpdate()


class TemplateTab(ttk.Frame): #TODO ALL
    """"""

    def __init__(self, FatherTab:ttk.Notebook, selected_language:dict) -> None:
        """"""

        super().__init__()

        self.__lang = dict(selected_language)
        self.__call_dictionary = LoadJson(Paths.DICTIONARY_JSON_PATH)

        self.master = FatherTab

        self.__CreateWidgets()


    def __CreateWidgets(self):
        tk.Label(
                self,
                text = 'Feature in development.'
            ).grid(column = 0, row = 0)


class AccountConfiguration(tk.Toplevel):
    """
    Account Configuration sub screen class for GUI class.\n
    * Uses double undescore to specify private methods/attributes instead of the convenional single underscore.

    Private Attributes:
        - __lang: A loaded language resource.
        - __config: A loaded ConfigClass object.
        - __valid_email_flag: A boolean indicating whether or not 
        user input on e-mail entry is a a valid e-mail.
        - __valid_password_flag: A boolean indicating whether or 
        not user input on password entry is a a valid password.
        - __email_error: Tkinter label widget for e-mail entry error messages.
        - __email_entry: Tkinter entry widget for e-mail user input.
        - __password_error: Tkinter label widget for password entry error messages.
        - __password_entry: Tkinter entry widget for password user input.
        - __save_button: Tkinter button widget for sending user input to 'config.ini' file.
    """

    def __init__(self, parent:GUI, selected_language:dict, config:ConfigClass) -> None:
        """

        Arguements:
            - parent: Object referente to GUI main screen for 'master' attribute definition.
            - selected_language: A loaded language resource.
            - config: A loaded ConfigClass object.

        Dependencies:
            - :mod:`__CreateWidgets()`: For tkinter widget creation.
        """

        super().__init__()

        self.__lang = dict(selected_language)
        self.__config = config

        self.master = parent
        self.title(self.master.title() + ': ' + self.__lang['Window_Titles']['Microsoft_Acc'])
        self.resizable(width = False, height = False)
        self.grab_set()

        self.__valid_email_flag = bool(False)
        self.__valid_password_flag = bool(False)

        self.__CreateWidgets()

    
    def Start(self) -> None:
        """"""

        self.mainloop()


    def __CreateWidgets(self) -> None:
        """"""

        #Email Field.
        tk.Label(
            self,
            text = 'E-mail:'
        ).grid(
            column = 0,
            row = 0,
            padx = [10, 0],
            pady = [6, 0],
            sticky = tk.W
        )
        self.__email_error = tk.Label(
            self,
            foreground = 'red'
        )
        self.__email_error.grid(
            column = 1,
            row = 0,
            padx = [0, 10],
            pady = [6, 0],
            sticky = tk.E
        )
        self.__email_entry = tk.Entry(
            self,
            width = 50,
            validate = 'focusout',
            validatecommand = (self.register(self.__EmailValidator), '%P'),
            invalidcommand = lambda: [
                self.__email_error.config(text = self.__lang['Text_Labels']['Invalid_E-mail']),
                self.__email_entry.config(foreground = 'red')
            ]
        )
        self.__email_entry.grid(
            column = 0,
            columnspan = 2,
            row = 1,
            padx = 10,
            pady = [0, 5]
        )
        self.__email_entry.bind('<FocusIn>', lambda _: [
                self.__email_entry.config(foreground = 'black'),
                self.__email_error.config(text = '')
            ]
        )
        self.__email_entry.bind('<FocusOut>', lambda _: self.__ButtonStateHandler())
        self.__email_entry.bind('<Key>', lambda _: self.__ButtonStateHandler())


        #Password Field.
        tk.Label(
            self,
            text = self.__lang['Text_Labels']['Password'] + ':'
        ).grid(
            column = 0,
            row = 2,
            padx = [10, 0],
            sticky = tk.W
        )
        self.__password_error = tk.Label(
            self,
            foreground = 'red'
        )
        self.__password_error.grid(
            column = 1,
            row = 2,
            padx = [0, 10],
            sticky = tk.E
        )        
        self.__password_entry = tk.Entry(
            self,
            show = '•',
            width = 50,
            validate = 'focusout',
            validatecommand = (self.register(self.__PasswordValidator), '%P'),
            invalidcommand = lambda: [
                self.__password_error.config(text = self.__lang['Text_Labels']['Invalid_Password']),
                self.__password_entry.config(foreground = 'red')
            ]
        )
        self.__password_entry.grid(
            column = 0,
            columnspan = 2,
            row = 3,
            padx = 10,
            pady = [0, 10]
        )
        self.__password_entry.bind('<FocusIn>', lambda _: [
                self.__password_entry.config(foreground = 'black'),
                self.__password_error.config(text = '')
            ]
        )
        self.__password_entry.bind('<FocusOut>', lambda _: self.__ButtonStateHandler())
        self.__password_entry.bind('<Key>', lambda _: self.__ButtonStateHandler())


        #Save button.
        self.__save_button = tk.Button(
            self,
            text = self.__lang['Buttons']['Save'],
            height = 2,
            width = 10,
            state = 'disabled',
            command = self.__ButtonPress
        )
        self.__save_button.grid(
            column = 4,
            row = 1,
            rowspan = 2,
            padx = [0, 10]
        )


    def __EmailValidator(self, input:str) -> bool:
        """
        Private Method: Validates if input string is a valid e-mail.

        Returns true if the input is a valid e-mail, false otherwise.
        """
        
        if re.fullmatch(GUIConstants.EMAIL_REGEX, input) is None:
            self.__valid_email_flag = False
        else:
            self.__valid_email_flag = True
        return self.__valid_email_flag


    def __PasswordValidator(self, input:str) -> bool:
        """
        Private Method: Validates if input string is a valid password.

        Returns true if the input is a valid password, false otherwise.
        """

        if re.fullmatch(GUIConstants.PASSWORD_REGEX, input) is None:
            self.__valid_password_flag = False
        else:
            self.__valid_password_flag = True
        return self.__valid_password_flag


    def __ButtonStateHandler(self) -> None:
        """
        Private Method:
        Enables send button if user input is valid.

        Dependencies:
            - :mod:`__EmailValidator()`: For user input validation on e-mail entry.
            - :mod:`__PasswordValidator()`: For user input validation on password entry.
        """

        #Forces user input validation.
        self.__EmailValidator(self.__email_entry.get())
        self.__PasswordValidator(self.__password_entry.get())

        if self.__valid_email_flag and self.__valid_password_flag:
            self.__save_button.config(state = 'normal')
        else:
            self.__save_button.config(state = 'disabled')

    
    def __ButtonPress(self) -> None:
        """
        Private Method:
        Send user input to 'config.ini' file and closes sub screen.
        """

        self.__config.UpdateCredentials(self.__email_entry.get(), self.__password_entry.get())
        self.destroy()
        
        messagebox.showinfo('HAF', self.__lang['Messages']['AccountUpdate'])


class LanguageConfiguration(tk.Toplevel): #TODO: Document
    """"""

    def __init__(self, parent:GUI, selected_language:dict, config:ConfigClass) -> None:
        """"""

        super().__init__()

        self.__parent = parent
        self.__lang = dict(selected_language)
        self.__config = config
        self.__current_language = str(self.__config.GetLanguage)

        self.master = parent
        self.title(self.master.title() + ': ' + self.__lang['Window_Titles']['Language_Config'])
        self.resizable(width = False, height = False)
        self.grab_set()

        self.__CreateWidgets()


    def Start(self) -> None: #TODO: Document
        """"""

        self.mainloop()

    
    def __CreateWidgets(self) -> None: #TODO: Document
        """"""

        Frame = tk.LabelFrame(
            self,
            text = self.__lang['Text_Labels']['Language'],
            font = ('Arial', 10, 'bold'),
            background = 'white',
            foreground = 'gray'
        )
        Frame.grid(
            row = 0,
            column = 0,
            padx = 150,
            pady = [50, 0]
        )
        tk.Label(
            Frame,
            text = self.__lang['Text_Labels']['Select_Language'] + ':',
            background = 'white'
        ).grid(
            row = 0,
            column = 0,
            padx = 10,
        )

        options_list = [str(self.__lang['Text_Labels']['Selection'])] + GUIConstants.VALID_LANGS
        self.__language_menu_variable = tk.StringVar()
        self.__language_menu_variable.set(self.__lang['Text_Labels']['Selection'])
        language_menu = ttk.OptionMenu(
            Frame,
            self.__language_menu_variable,
            *options_list,
            direction = 'right',
            command = lambda _: self.__onMenuChange()
        )
        language_menu.grid(
            column = 0,
            row = 1
        )

        self.__refresh_button = tk.Button(
            self,
            text = self.__lang['Buttons']['Restart'],
            command = self.__RefreshButtonPress,
            state = tk.DISABLED
        )
        self.__refresh_button.grid(
            row = 1,
            column = 0,
            padx = 150,
            pady = [0, 50]
        )


    def __onMenuChange(self) -> None: #TODO: Document
        """"""
        
        user_selection = self.__language_menu_variable.get()
        if( #!
            user_selection != self.__lang['Text_Labels']['Selection'] and 
            user_selection != self.__current_language
        ):
            self.__refresh_button.config(state = tk.NORMAL)
        else: #!
            self.__refresh_button.config(state = tk.DISABLED)


    def __RefreshButtonPress(self) -> None: #TODO: Document
        """"""

        self.__config.UpdateLanguage(self.__language_menu_variable.get())
        self.destroy()
        
        messagebox.showinfo('HAF', self.__lang['Messages']['LanguageUpdate'])

        self.__parent.Restart()


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')