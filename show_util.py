from prettytable import PrettyTable


def example_vnpy_interface(inter_data):
    table = PrettyTable()
    table.field_names = ["NAME", "Windows", "Ubuntu", "Mac"]

    for name, systems in inter_data:
        mp = dict()
        for system in ["Windows", "Ubuntu", "Mac"]:
            if system in systems:
                mp[system] = "\u2713"
            else:
                mp[system] = ""

        table.add_row([name] + [v for k, v in mp.items()])

    print(table)
