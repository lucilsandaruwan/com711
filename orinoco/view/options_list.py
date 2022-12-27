# This view is called when there are list of options and user need to select one of them and take the code of that option.

from view import str_format as sf 

def _display_options(all_options,title,type):
    """This is the given function in the assignment to be used in all option lists.
        *** thanks for making the implementation easier by giving this :)
        Args:
            all_options(list): list of arrays having following elements in each
                [0](string): expected code to be returned after user selecting the option
                [1](string): The text to show as option.
            title(string): The title of the option list
            type(string): the type of the option that shoudl be shown in the prompt request.
        Returns:
            string: The code([0] element) of the selected option.
    """
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

