
# This file contains functions to rout user inputs withing the application. 
# It calls to handler functions of controllers according to user inputs.


from controller import shopper as s_cntrl
from controller import order as o_cntrl
from controller import basket as b_cntrl
from view import validated_input as vi
from view import str_format as sf

#The global variable holds the menu items to display when it is required to display
MENUE_ITEMS = (
    "\n{}\n" 
    "\n0   Show menue"
    "\n1   Display your order history"
    "\n2   Add an item to your basket"
    "\n3   View your basket"
    "\n4   Checkout"
    "\n5   Exit"
    "\n6   Change Shopper"
).format(sf.underline("ORINOCO – SHOPPER MAIN MENU                                           "))

def exit_greeting():
    print(sf.sucess("Good bye!"))
def exception_msg():
    print(sf.warning("There is an exception, please try again"))


def route(shopper_id):
    """ To display the menue and rout the selected menue number to relevent controller after user login to the system.
            Args:
                shopper_id (string): the shopper id of shoppers table
 
            Returns:
                void
    """

    print("\nPlease slect an option from the following menue to continue \n{}".format(MENUE_ITEMS)) 
    try:
        # The loop will keep going and serv to user request untill user enter 5(exit) or 6(change user) as menue item
        while True:
            #taking validated menue item number from user with the help of 'validated_input' view
            m_item = int(vi.defined_values(
                "\nPlease enter the number against the menue item or {} to see menue again: ".format(sf.blue("0"))
                ,(0,1,2,3,4,5,6)
                ,True
            ))
            
            if m_item == 0:
                print(MENUE_ITEMS)
            elif m_item == 1:
                o_cntrl.order_history(shopper_id)
            elif m_item == 2:
                b_cntrl.add_item(shopper_id)
            elif m_item == 3:
                b_cntrl.view_basket(shopper_id)
            elif m_item == 4:
                o_cntrl.checkout(shopper_id)
            elif m_item == 5:
                exit_greeting()
                break
            elif m_item == 6:
                # if user want to log another user, the init function should be called to initiate the app and return from the menue loop
                return init()
            else: # Idealy, user should not see this message because the input is validated from relevent view
                print(sf.error("\nYou have entered an invalid menu item number. Please select a correct number from the menue"))   
    except:
        exception_msg()
        return route(shopper_id)

def init():
    """This is the entry point of app. It calls login function from the controller to get shopper_id and rout function to rout
        user requests
            Returns:
                void
    """
    try:
        shopper = s_cntrl.login()
        if shopper:
            shopper_id = shopper["shopper_id"]
            route(shopper_id)    
        else: 
            exit_greeting()
    except :
        exception_msg()
        init()
# the entry point of the app which calls the init function to boot application
init()
