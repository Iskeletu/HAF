""""""

#Native Modules:
from tkinter import ttk, messagebox
import tkinter as tk
import subprocess
import webbrowser
import re

#External Modules:
from selenium import webdriver

#Internal Modules:
from HAF.Constants import Paths, GUIConstants, URL
from HAF.FileHandler.JsonHandler import LoadJson
from HAF.FileHandler.Config import ConfigClass
from HAF import __version__ as HAFVersion
from HAF.FileHandler.JsonHandler import *
from HAF.CLI.Commands import *


class GUI(tk.Tk): #TODO: ALL
    """
        - __driver:
        - __config:
        - __exit_flag:
        - __lang:
        - __auto_open_flag:
        - __Tabcontrol:
    """

    def __init__(self, config:ConfigClass, driver:webdriver.Chrome) -> None: #TODO: Document
        """"""

        super().__init__()

        self.__driver = driver
        self.__config = config
        self.__exit_value = int(0)

        self.__lang = LoadJson(Paths.RESOURCES_FOLDER_PATH + self.__config.GetLanguage + '.json')
        self.__auto_open_flag = tk.IntVar(); self.__auto_open_flag.set(self.__config.AutoOpenStatus)

        self.title('HAF ' + HAFVersion)
        self.geometry('800x600')
        self.resizable(width = False, height = False)

        self.__CreateWidgets()


    def Start(self) -> bool: #TODO: Document
        """"""

        self.mainloop()
        return self.__exit_value
        

    def Restart(self) -> None: #TODO: Document
        """"""

        self.__exit_value = 2
        self.destroy()


    def __CreateWidgets(self) -> None: #TODO: Document
        """"""

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
            command = self.__ExitSequence
        )


        #'Help' menu configuration:
        help_menu = tk.Menu(menu_bar, tearoff = False)
        help_menu.add_command( #'About' option.
            label = self.__lang['Labels']['Help_Label']['About'],
            command = lambda: webbrowser.open(URL.ABOUT_PROJECT_URL, autoraise = True)
        )


        menu_bar.add_cascade(label = self.__lang['Labels']['File_Label']['Title'], menu = file_menu)
        menu_bar.add_cascade(label = self.__lang['Labels']['Help_Label']['Title'], menu = help_menu)
        self.config(menu = menu_bar)


        #Tab configuration:
        self.__TabControl = ttk.Notebook(self)
        self.__TabControl.pack(expand = True, fill = 'both')

        self.__calltab = CallTab(self.__TabControl, self.__lang)
        self.__TabControl.add(self.__calltab, text = self.__lang['Tabs']['CallTab'])

        self.__ConfigureTemplateTab()


    def __ConfigureTemplateTab(self) -> None: #transform to class
        TemplateTab = ttk.Frame(self.__TabControl)
        self.__TabControl.add(TemplateTab, text = self.__lang['Tabs']['TemplateTab'])

        tk.Label(
            TemplateTab,
            text = 'Feature in development.'
        ).grid(column = 0, row = 0)


    def __ExitSequence(self) -> None: #TODO: Document
        """"""

        self.__exit_value = 1
        self.destroy()


class CallTab(ttk.Frame): #TODO ALL
    """"""

    def __init__(self, FatherTab:ttk.Notebook, selected_language:dict) -> None:
        """"""

        super().__init__()

        self.__lang = dict(selected_language)
        self.__call_dictionary = LoadJson(Paths.DICTIONARY_JSON_PATH)
        self.__usernamecash = []

        self.master = FatherTab

        self.__CreateWidgets()

    
    def __CreateWidgets(self) -> None: #TODO: Commands/Document
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
        self.__user_ID_entry = tk.Entry(
            self,
            width = 30,
            validate = 'focusout',
            validatecommand = (self.register(self.__UserIDValidator), '%P'),
            invalidcommand = lambda: self.__user_ID_entry.config(
                foreground = 'red'
            )
        )
        self.__user_ID_entry.grid(
            column = 0,
            row = 1,
            padx = 12,
            pady = [0, 10],
            sticky = tk.NW
        )
        self.__user_ID_entry.bind('<FocusIn>', lambda _: self.__user_ID_entry.config(
                foreground = 'black'
        ))
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
        self.__user_contact_entry = tk.Entry(
            self,
            width = 30,
            validate = 'focusout',
            validatecommand = (self.register(self.__UserIDValidator), '%P'),
            #invalidcommand = 
        )
        self.__user_contact_entry.grid(
            column = 1,
            row = 1,
            padx = [0, 12],
            pady = [0, 10],
            sticky = tk.NW
        )
        self.__user_contact_entry.bind('<FocusOut>', lambda _: self.__CTVUpdate())
        self.__user_contact_entry.bind('<KeyRelease>', lambda _: self.__CTVUpdate())
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
        ticket_type_options = ['Selection'] + list(self.__call_dictionary.keys())
        self.ticket_type_variable = tk.StringVar()
        self.ticket_type_variable.set('Selection')
        ticket_type_menu = ttk.OptionMenu(
            self.OptionsFrame,
            self.ticket_type_variable,
            *ticket_type_options,
            direction = 'right',
            command = lambda _: self.__onTicketTypeSelection(self.__call_dictionary[self.ticket_type_variable.get()])
        )
        ticket_type_menu.grid(
            column = 1,
            row = 0,
            sticky = tk.NW
        )
        ticket_type_menu.bind('<Configure>', lambda _: self.__CTVUpdate())
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
        self.__solution_type_options = ['Selection']
        self.solution_type_variable = tk.StringVar()
        self.solution_type_variable.set('Selection')
        self.__solution_type_menu = ttk.OptionMenu(
            self.OptionsFrame,
            self.solution_type_variable,
            *self.__solution_type_options,
        ); self.__solution_type_menu.config(state = tk.DISABLED)
        self.__solution_type_menu.grid(
            column = 1,
            row = 1,
            sticky = tk.NW
        )
        

        #Send button.
        tk.Button(
            self,
            text = self.__lang['Buttons']['Send'],
            height = 4,
            width = 15
            #command = #TODO
        ).grid(
            column = 3,
            row = 19,
            rowspan = 2,
            padx = 12,
            pady = 10,
            sticky = tk.NE
        )


    def __CallTabVisualizer(self) -> None: #TODO: document
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
        self.VisualizerTitleText = tk.Text(
            PreviewFrame,
            background = GUIConstants.COLOR_CUSTOM_GRAY,
            font = ('Helvetica', 15),
            state = 'disabled',
            height = 1,
            width = 40
        )
        self.VisualizerTitleText.grid(
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
        self.VisualizerBodyText = tk.Text(
            PreviewFrame,
            background = GUIConstants.COLOR_CUSTOM_GRAY,
            font = ('Helvetica', 15),
            state = 'disabled',
            height = 6,
            width = 40
        )
        self.VisualizerBodyText.grid(
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
        self.VisualizerSolutionText = tk.Text(
            PreviewFrame,
            background = GUIConstants.COLOR_CUSTOM_GRAY,
            font = ('Helvetica', 15),
            state = 'disabled',
            height = 3,
            width = 40
        )
        self.VisualizerSolutionText.grid(
            column = 0,
            row = 10,
            rowspan = 2,
            padx = 87,
            pady = [0, 25],
            sticky = tk.NW
        )


    def __UserIDValidator(self, string:str) -> bool: #TODO
        """"""
        
        if string and len(string) == 10:
            if string in self.__usernamecash:
                return True


            p = subprocess.Popen(
                f'net user /domain {string}',
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE
            )
            error = p.stderr.read()

            if not error:
                self.__usernamecash.append(str(string))
                return True
        return False


    def __CTVUpdate(self) -> None: #TODO
        """"""

        if self.ticket_type_variable.get() != 'Selection':
            dictionary = self.__call_dictionary[self.ticket_type_variable.get()]

            #Visualizer ticket title update.
            try:
                self.VisualizerTitleText.config(state = tk.NORMAL)
                self.VisualizerTitleText.delete('1.0', tk.END)
                self.VisualizerTitleText.insert(tk.END, str(dictionary['Title']).format(
                    Variable = self.__variable_entry.get()
                ))
                self.VisualizerTitleText.config(state = tk.DISABLED)
                self.VisualizerTitleText.config(foreground = 'black')
            except KeyError:
                self.VisualizerTitleText.config(state = tk.NORMAL)
                self.VisualizerTitleText.delete('1.0', tk.END)
                self.VisualizerTitleText.insert(tk.END, '{Does not apply for this ticket}')
                self.VisualizerTitleText.config(state = tk.DISABLED)
                self.VisualizerTitleText.config(foreground = 'red')
            
            #Visualizer ticket body update.
            self.VisualizerBodyText.config(state = tk.NORMAL)
            self.VisualizerBodyText.delete('1.0', tk.END)
            self.VisualizerBodyText.insert(tk.END, str(dictionary['Body']).format(
                Contact = self.__user_contact_entry.get(),
                Hostname = self.__user_hostname_entry.get(),
                Variable = self.__variable_entry.get()
            ))
            self.VisualizerBodyText.config(state = tk.DISABLED)

            #Visualizer ticket solution update.
            if dictionary['Process-Type'] == 'close':
                if self.solution_type_variable.get() != 'Selection':
                    self.VisualizerSolutionText.config(state = tk.NORMAL)
                    self.VisualizerSolutionText.delete('1.0', tk.END)
                    self.VisualizerSolutionText.insert(tk.END, str(dictionary['Answer'][int(self.solution_type_variable.get())]).format(
                        Variable = self.__variable_entry.get()
                    ))
                    self.VisualizerSolutionText.config(state = tk.DISABLED)
                    self.VisualizerSolutionText.config(foreground = 'black')
                else:
                    self.VisualizerSolutionText.config(state = tk.NORMAL)
                    self.VisualizerSolutionText.delete('1.0', tk.END)
                    self.VisualizerSolutionText.insert(tk.END, '{Please, select a solution type in the options}')
                    self.VisualizerSolutionText.config(state = tk.DISABLED)
                    self.VisualizerSolutionText.config(foreground = 'red')
            else:
                self.VisualizerSolutionText.config(state = tk.NORMAL)
                self.VisualizerSolutionText.delete('1.0', tk.END)
                self.VisualizerSolutionText.insert(tk.END, '{Does not apply for this ticket}')
                self.VisualizerSolutionText.config(state = tk.DISABLED)
                self.VisualizerSolutionText.config(foreground = 'red')


    def __onTicketTypeSelection(self, dictionary:dict) -> None: #TODO
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
            numberlist = ['Selection']
            for i in range (0, len(list(dictionary['Answer']))):
                numberlist.append(str(i))
            self.__solution_type_options = numberlist
            self.solution_type_variable.set('Selection')

            #Recreates widget (editing it causes undefined bahaviour).
            self.__solution_type_menu.destroy()
            self.__solution_type_menu = ttk.OptionMenu(
                self.OptionsFrame,
                self.solution_type_variable,
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
            self.__solution_type_options = ['Selection']
            self.solution_type_variable.set(self.__solution_type_options[0])
            self.__solution_type_menu.config(state = tk.DISABLED)


class AccountConfiguration(tk.Toplevel): #TODO: REFACTOR/DOCUMENT
    """"""

    def __init__(self, parent:GUI, selected_language:dict, config:ConfigClass) -> None:
        """"""

        super().__init__()

        self.__lang = dict(selected_language)
        self.__config = config

        self.master = parent
        self.title(self.master.title() + ': ' + self.__lang['Window_Titles']['Microsoft_Acc'])
        self.resizable(width = False, height = False)
        self.grab_set()

        self.__valid_email_flag = bool(False)
        self.__valid_password_flag = bool(False)

        self.__create_widgets()

    
    def Start(self) -> None:
        """"""

        self.mainloop()


    def __create_widgets(self) -> None:
        """"""

        #Email Field.
        ttk.Label(
            self,
            text = 'E-mail:'
        ).grid(row = 0, column = 0, padx = 5)
        self.__email_error = ttk.Label(self, foreground='red')
        self.__email_entry = ttk.Entry(
            self,
            width = 50,
            validate = 'focusout',
            validatecommand = (self.register(self.__EmailValidator), '%P'),
            invalidcommand = self.__on_InvalidEmail
        )
        self.__email_entry.bind('<FocusIn>', self.__on_EmailFocus)
        self.__email_entry.bind('<FocusOut>', self.__ButtonStateHandler)
        self.__email_entry.bind('<Key>', self.__ButtonStateHandler)

        self.__email_entry.grid(row = 0, column = 1, columnspan = 2, padx = 5)
        self.__email_error.grid(row = 1, column = 1, padx = 5, sticky = tk.W)


        #Password Field.
        ttk.Label(
            self,
            text = self.__lang['Text_Labels']['Password'] + ':'
        ).grid(row = 2, column = 0, padx = 5)
        self.__password_error = ttk.Label(self, foreground='red')
        self.__password_entry = ttk.Entry(
            self,
            show = '*',
            width = 50,
            validate = 'focusout',
            validatecommand = (self.register(self.__PasswordValidator), '%P'),
            invalidcommand = self.__on_InvalidPassword
        )
        self.__password_entry.bind('<FocusIn>', self.__on_PasswordFocus)
        self.__password_entry.bind('<FocusOut>', self.__ButtonStateHandler)
        self.__password_entry.bind('<Key>', self.__ButtonStateHandler)

        self.__password_entry.grid(row = 2, column = 1, columnspan = 2, padx = 5)
        self.__password_error.grid(row = 3, column = 1, sticky = tk.W, padx = 5)


        #Save button.
        self.__save_button = ttk.Button(
            self,
            text = self.__lang['Buttons']['Save'],
            state = 'disabled',
            command = self.__ButtonPress
        )
        self.__save_button.grid(row = 0, column = 4, padx = 5)


    def __EmailValidator(self, input:str) -> bool:
        """"""
        
        if re.fullmatch(GUIConstants.EMAIL_REGEX, input) is None:
            return False
        return True


    def __on_InvalidEmail(self) -> None:
        """"""

        self.__email_error['text'] = 'Invalid E-mail!'
        self.__email_entry['foreground'] = 'red'


    def __on_EmailFocus(self, event:tk.Event) -> None:
        """"""

        self.__email_entry['foreground'] = 'black'
        self.__email_error['text'] = ''

    
    def __PasswordValidator(self, input:str) -> bool:
        """"""

        if re.fullmatch(GUIConstants.PASSWORD_REGEX, input) is None:
            return False
        return True


    def __on_InvalidPassword(self) -> None:
        """"""

        self.__password_error['text'] = 'Invalid Password!'
        self.__password_entry['foreground'] = 'red'


    def __on_PasswordFocus(self, event:tk.Event) -> None:
        """"""

        self.__password_entry['foreground'] = 'black'
        self.__password_error['text'] = ''


    def __ButtonStateHandler(self, event:tk.Event) -> None:
        """"""

        self.valid_email_flag = self.__EmailValidator(self.__email_entry.get())
        self.valid_password_flag = self.__PasswordValidator(self.__password_entry.get())

        if self.valid_email_flag and self.valid_password_flag:
            self.__save_button.config(state = 'normal')
        else:
            self.__save_button.config(state = 'disabled')

    
    def __ButtonPress(self) -> None:
        """"""

        self.__config.UpdateCredentials(self.__email_entry.get(), self.__password_entry.get())
        self.destroy()
        
        messagebox.showinfo('HAF', self.__lang['Messages']['AccountUpdate'])


class LanguageConfiguration(tk.Toplevel): #TODO: ALL
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

        options_list = ['Selection'] + GUIConstants.VALID_LANGS
        self.__language_menu_variable = tk.StringVar()
        self.__language_menu_variable.set('Selection')
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


    def __onMenuChange(self) -> None:
        """"""
        
        user_selection = self.__language_menu_variable.get()
        if( #!
            user_selection != 'Selection' and 
            user_selection != self.__current_language
        ):
            self.__refresh_button.config(state = tk.NORMAL)
        else: #!
            self.__refresh_button.config(state = tk.DISABLED)


    def __RefreshButtonPress(self) -> None:
        """"""

        self.__config.UpdateLanguage(self.__language_menu_variable.get())
        self.destroy()
        
        messagebox.showinfo('HAF', self.__lang['Messages']['LanguageUpdate'])

        self.__parent.Restart()


#This is NOT a script file.
if __name__ == '__main__':
    exit('ERROR: Not a script file!')