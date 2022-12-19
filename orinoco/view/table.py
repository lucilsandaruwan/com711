def dinamic_table(headers, data):
    # headers = (
    #     {"length": 8, "lable": "Pos"}
    #     ,{"length": 30, "lable": "Lang"}
    #     ,{"length": 10, "lable": "Percent"}
    #     ,{"length": 10, "lable": "Change"}
    # )
    header_txt = "\n"
    for ele in headers:
        header_txt += "{1:<{0}}".format(ele["length"], ele["lable"])
    print (header_txt)
    # separator = ""
    # for c in header_txt:
    #     separator += "-"
    # print("{}".format(separator))
    # data = (
    #     [1234567,"Java", 23.54, 'DOWN']
    #     ,[2,"1234567812345678912345671234", 17.22, 'UP']
    #     ,[3,"Lua", 10.55, 'DOWN']
    #     ,[4,"Groovy", 9.22, 'DOWN']
    #     ,[5,"C", 1.55, 'UP']
    # )
    # d = {1: ["Pythonafafffsafasfffdfssfasf asfdasfasf asfasfs", 33.2, 'UP'],
    # 2: ["Java", 23.54, 'DOWN'],
    # 3: ["Ruby", 17.22, 'UP'],
    # 10: ["Lua", 10.55, 'DOWN'],
    # 5: ["Groovy", 9.22, 'DOWN'],
    # 6: ["C", 1.55, 'UP']
    # } 
    
    for item in data:
        data_txt = ""
        for k, v in enumerate(item):
            # print(k, headers[k], v)
            data_txt += "{1:<{0}}".format(headers[k]["length"], v)
        print(data_txt)
    # for k, v in d.items():
    #     data_txt = ""
    #     lang, perc, change = v
    #     print
    #     print ("{:<8} {:<30} {:<10} {:<10}".format(k, lang, perc, change))