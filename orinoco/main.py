"""
This file contains code to rout user inputs withing the application. 
It calls to handler functions of controllers according to user inputs.
"""
from controller import shopper as s_cntrl
from controller import order as o_cntrl
from controller import basket as b_cntrl
from view import validated_input as vi
from view import str_format as sf

#The global variable holds the menu itme to display when it is required to display
MENUE_ITEMS = (
    "\n0   Show menue"
    "\n1   Display your order history"
    "\n2   Add an item to your basket"
    "\n3   View your basket"
    "\n4   Checkout"
    "\n5   Exit"
    "\n6   Change Shopper"
)

#The Funtion display the menue when use login to the system and rout the selected menue number to relevent controller.
#input: shopper dictionary gaving elements (id, name ...)
def route(shopper):
    #introduce the menue to user
    print("\nPlease slect an option from the following menue to continue \n{}".format(MENUE_ITEMS)) 
    while True:
        #taking validated menue item number from user
        m_item = int(vi.defined_values(
            "\nPlease enter the number against the menue item ( or 0 to see menue again): "
            ,(0,1,2,3,4,5,6)
            ,True
        ))
        
        if m_item == 0:
            print(MENUE_ITEMS)
        elif m_item == 1:
            o_cntrl.order_history(shopper)
        elif m_item == 2:
            b_cntrl.add_item(shopper)
        elif m_item == 3:
            b_cntrl.view_basket(shopper)
        elif m_item == 4:
            o_cntrl.checkout(shopper)
        elif m_item == 5:
            print(sf.sucess("Good bye!"))
            break
        elif m_item == 6:
            return main()
        else: # 
            print(sf.error("\nYou have entered an invalid menu item number. Please select a correct number from the menue"))   

def main():
    shopper = s_cntrl.login()
    route(shopper)       
main()