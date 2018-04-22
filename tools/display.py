import time

import tools.defines as td

def colored_display(options):
    styles = {
            # styles
            'reset': '\033[0m',
            'bold': '\033[01m',
            'disabled': '\033[02m',
            'underline': '\033[04m',
            'reverse': '\033[07m',
            'strike_through': '\033[09m',
            'invisible': '\033[08m',
            # text colors
            'fg_black': '\033[30m',
            'fg_red': '\033[31m',
            'fg_green': '\033[32m',
            'fg_orange': '\033[33m',
            'fg_blue': '\033[34m',
            'fg_purple': '\033[35m',
            'fg_cyan': '\033[36m',
            'fg_light_grey': '\033[37m',
            'fg_dark_grey': '\033[90m',
            'fg_light_red': '\033[91m',
            'fg_light_green': '\033[92m',
            'fg_yellow': '\033[93m',
            'fg_light_blue': '\033[94m',
            'fg_pink': '\033[95m',
            'fg_light_cyan': '\033[96m',
            # background colors
            'bg_black': '\033[40m',
            'bg_red': '\033[41m',
            'bg_green': '\033[42m',
            'bg_orange': '\033[43m',
            'bg_blue': '\033[44m',
            'bg_purple': '\033[45m',
            'bg_cyan': '\033[46m',
            'bg_light_grey': '\033[47m'
    }
    for elt in options:
        print(styles[elt], end='', flush=True)
    

def display_steps(*args, query, dic, end_display="", sleep=True, bypass=False):
    if td.op_visualisation is True or bypass is True:
        
        print(args[0], end='', flush=True)
        for arg in args[1:]:
            for letter in arg:
                option = []

                if td.op_color and td.op_visualisation:
                        
                    if letter is query:
                        option.append("bold")

                    if letter.isupper():
                        if dic[letter][0] is td.v_true:
                            option.append("fg_green")  
                        elif (dic[letter][0] is td.v_false 
                            and dic[letter][2] is not td.m_default):
                            option.append("fg_red") 
                        elif dic[letter][0] is td.v_undef:
                            option.append("fg_light_blue")  
                        elif dic[letter][0] is td.v_bugged: 
                            option.append("fg_dark_grey") 
                        else:
                            option.append("fg_light_grey")

                    else:
                        option.append("fg_light_grey")

                    colored_display(option)
                    print("%s%s" % (letter, '\033[0;0m'), end='', flush=True)
                    
                else:
                    print("%s" % letter, end='', flush=True)
                    

        print(end_display)
        if sleep is True:
            time.sleep(1)

