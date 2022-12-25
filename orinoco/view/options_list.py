from view import str_format as sf 

def _display_options(all_options,title,type):
    option_num = 1
    option_list = []
    print("\n",sf.underline(title),"\n")
    for option in all_options:
        code = option[0]
        desc = option[1]
        print("{0}.\t{1}".format(option_num, desc))
        option_num = option_num + 1
        option_list.append(code)
    selected_option = 0
    while selected_option > len(option_list) or selected_option == 0:
        prompt = "Enter the number against the "+type+" you want to choose: "
        try:
            selected_option = int(input(prompt))
        except:
            print(sf.error("\nPlease enter a number\n"))
        
    return option_list[selected_option - 1]

