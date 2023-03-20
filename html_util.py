from bs4 import BeautifulSoup


def example_vnpy_interface(text):
    import re

    soup = BeautifulSoup(text, "html.parser")
    root = soup.find("div", attrs={"class": "section", "id": "id8"})
    targets = root.find_all("div", attrs={"class": "section"})
    res = list()
    for target in targets:
        if re.match("id.?", target["id"]) is not None:
            continue
        name = target.find("h3").text[:-1]

        system = [t.text for t in target.find("div").find("li").find_all("li")]
        sorted(system)

        res.append((name, system))

    return res
