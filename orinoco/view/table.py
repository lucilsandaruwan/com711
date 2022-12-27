# this view is created to display tables 
from view import str_format as sf

def dinamic_table(title, headers, data):
    """This is to drow tables regarding to the given headers and data. The number of element of hearers should be equal to the 
        number of elements in each record of data object to use this function. Refered https://www.educba.com/python-print-table/ 
        to build this function to match with the requirement of this application
        Args:
            title(string): the title of the table
            headers(tuple): this should have list of dictionaries having following elements for each colomn of the table
                length(int): The charactor length of the colomn
                lable(string): header lable to be printed
            data(list):  this is a list of tuples having values of each column in the header.
        Returns: void, this is just to draw the table according to input
    """
    print("\n")
    print(sf.underline(sf.bold(title)))
    header_txt = "\n"
    for ele in headers:
        header_txt += "{1:<{0}}".format(ele["length"], ele["lable"])
    print(sf.bold(header_txt))
    
    for item in data:
        data_txt = ""
        for k, v in enumerate(item):
            data_txt += "{1:<{0}}".format(headers[k]["length"], str(v))
        print(data_txt)
    