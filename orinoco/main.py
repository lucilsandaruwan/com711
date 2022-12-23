from controller import shopper as s_cntrl
from controller import order as o_cntrl
from controller import basket as b_cntrl
MENUE_ITEMS = (
    "\n1   Display your order history"
    "\n2   Add an item to your basket"
    "\n3   View your basket"
    "\n4   Checkout"
    "\n5   Exit"
    "\n6   Change Shopper"
)

def view_basket(shopper):
    print("your basket")

def checkout(shopper):
    print("checkout")

def route(shopper):
    print("\nPlease slect an option from the following menue to continue {}".format(MENUE_ITEMS)) 
    while True:
        try:
            m_item = int(input("\nPlease enter the number against the menue item ( or 0 to see menue again): "))
            
            if m_item == 0:
                print(MENUE_ITEMS)
            elif m_item == 1:
                o_cntrl.order_history(shopper)
            elif m_item == 2:
                b_cntrl.add_item(shopper)
            elif m_item == 3:
                b_cntrl.view_basket(shopper)
            elif m_item == 4:
                checkout(shopper)
            elif m_item == 5:
                print("Good bye!")
                break
            elif m_item == 6:
                main()
                return
            else:
                print("\nYou have entered an invalid menu item number. Please select a correct number from the menue")
        except:
            print("\nSomething wrong with your input, please try again")   
            raise   

def main():
    shopper = s_cntrl.login()
    route(shopper)       
main()