from view import str_format as sf

def dinamic_table(title, headers, data):
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
    