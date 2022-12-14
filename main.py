import itertools
import os

import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from fpdf import FPDF
from bing_image_downloader import downloader
from PIL import Image

G = nx.Graph()

osoby = []
dane = []
with open('osoby.txt', encoding='utf-8') as f:
    for linia in f:
        osoba = []
        split = linia.split(",")
        imie, kraj, zawod = linia.split(",")
        temp = {'imie': imie.strip(), 'kraj': kraj.strip(), 'zawod': zawod.strip()}
        osoby.append(temp)
        for elem in split:
            # print(elem.strip())
            osoba.append(elem.strip())

        osoby.append(temp)
        dane.append(osoba)

# print(dane)
for elem in dane:
    G.add_node(elem[0])

polaczenia = []
for elem in dane:
    for elem2 in dane:
        if (elem[1] == elem2[1] or elem[2] == elem2[2]) and elem2[0] != elem[0]:
            # print(elem[1], elem2[1], elem[2], elem2[2])
            polaczenia.append((elem[0], elem2[0]))

pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('copper'))
nx.draw_networkx_labels(G, pos)
G.add_edges_from(polaczenia)
# print(len(polaczenia))
nx.draw_networkx_edges(G, pos)
net = Network(notebook=True, height="550px", width="100%", bgcolor="eeeeee",
              font_color="black", filter_menu=True, select_menu=True)
net.repulsion()
net.from_nx(G)
# print(net.nodes)
for e in net.nodes:
    for osoba in osoby:
        if e['id'] == osoba['imie']:
            if osoba['zawod'] == "polityka":
                e['color'] = "red"
                e['zawod'] = "Polityka"
            elif osoba['zawod'] == "sądownictwo":
                e['color'] = "yellow"
                e['zawod'] = "Sądownictwo"
            elif osoba['zawod'] == "dziennikarstwo":
                e['color'] = "blue"
                e['zawod'] = "Dziennikarstwo"
            elif osoba['zawod'] == "działalność społeczna":
                e['color'] = "pink"
                e['zawod'] = "Działalność społeczna"
            elif osoba['zawod'] == "aktorstwo":
                e['color'] = "orange"
                e['zawod'] = "Aktorstwo"
            elif osoba['zawod'] == "wojsko":
                e['color'] = "darkgreen"
                e['zawod'] = "Wojsko"
            elif osoba['zawod'] == "CEO":
                e['color'] = "purple"
                e['zawod'] = "CEO"
            elif osoba['zawod'] == "muzyka":
                e['color'] = "lightblue"
                e['zawod'] = "Muzyka"
            elif osoba['zawod'] == "architekt":
                e['color'] = "brown"
                e['zawod'] = "Architekt"
            elif osoba['zawod'] == "literatura":
                e['color'] = "grey"
                e['zawod'] = "Literatura"
            elif osoba['zawod'] == "prezenterka":
                e['color'] = "darkred"
                e['zawod'] = "Prezenterka"
            elif osoba['zawod'] == "informatyka":
                e['color'] = "lightgrey"
                e['zawod'] = "Informatyka"
            elif osoba['zawod'] == "moda":
                e['color'] = "darkyellow"
                e['zawod'] = "Moda"
            elif osoba['zawod'] == "celebrytka":
                e['color'] = "lightpink"
                e['zawod'] = "Celebrytka"
            elif osoba['zawod'] == "reżyseria":
                e['color'] = "darkbrown"
                e['zawod'] = "Reżyseria"
            else:
                e['color'] = "black"
                e['zawod'] = "Niezdefiniowano"

net.show("siec.html")

print("Kliki")
kliki = nx.find_cliques(G)
for elem in kliki:
    print(elem)

# print("\nOsoby i w ilu maksymalnych klikach się znajdują:")
ilosc_maksymalnych_klik = nx.number_of_cliques(G)
ilosc_maksymalnych_klik = dict(sorted(ilosc_maksymalnych_klik.items(), key=lambda item: item[1], reverse=True))
# print(ilosc_maksymalnych_klik)

osoba = "Joe Biden"
# print(f"Osoba {osoba} i jej kliki")
# print(nx.cliques_containing_node(G)[osoba])

liczba_polaczen = dict(G.degree())
# print(liczba_polaczen)
# print(liczba_polaczen["Mia Mottley"])
maksymalna_liczba_polaczen = max(dict(G.degree()).items(), key=lambda x: x[1])[1]


class PDF(FPDF):
    def flag(self, flaga):
        if os.path.isfile(flaga):
            im = Image.open(flaga)
        elif os.path.isfile(flaga.replace("jpg", "gif")):
            flaga = flaga.replace("jpg", "gif")
            im = Image.open(flaga.replace("jpg", "gif"))
        else:
            flaga = flaga.replace("jpg", "png")
            im = Image.open(flaga.replace("jpg", "png"))

        width, height = im.size
        max_height = 10
        self.set_xy(190.0, 5.0)
        self.image(flaga, link='', type='', w=width * (max_height / height), h=height * (max_height / height))

    def imagex(self, zdjecie):
        im = Image.open(zdjecie)
        width, height = im.size
        max_width = 100
        self.set_xy(55.0, 50.0)
        self.image(zdjecie, link='', type='', w=width * (max_width / width), h=height * (max_width / width))

    def titles(self, osoba):
        for elem in dane:
            if elem[0] == osoba:
                kraj = elem[1]
                profesja = elem[2]
        self.set_xy(0.0, 0.0)
        self.set_font('Arial', 'B', 26)
        self.set_text_color(0, 0, 0)
        self.multi_cell(w=210.0, h=20.0, align='C', txt=osoba, border=0)
        self.set_font('Arial', 'B', 12)
        self.multi_cell(w=190.0, h=12.0, align='C', txt=f"Kraj pochodzenia: {kraj}     |     Profesja: {profesja}",
                        border=0)
        if ilosc_maksymalnych_klik[osoba] == 2:
            kliki_info = f"Znajduje sie w dwoch klikach"
        elif ilosc_maksymalnych_klik[osoba] == 1:
            kliki_info = f"Znajduje sie w jednej klice"
        else:
            kliki_info = f"Znajduje sie w wiecej niz dwoch klikach"
        self.multi_cell(w=190.0, h=6.0, align='C', txt=kliki_info,
                        border=0)
        self.multi_cell(w=190.0, h=6.0, align='C', txt=f"Ma {liczba_polaczen[osoba]} polaczen z innymi osobami",
                        border=0)
        if liczba_polaczen[osoba] == maksymalna_liczba_polaczen:
            self.multi_cell(w=190.0, h=6.0, align='C', txt=f"(jest to maksymalna liczba polaczen)",
                            border=0)

    def info(self, osoba, zdjecie):
        im = Image.open(zdjecie)
        width, height = im.size
        max_width = 100
        height = height * (max_width / width)
        text = ""
        for e, elem in enumerate(nx.cliques_containing_node(G)[osoba]):
            text += f"Klika {e + 1}:\n"
            for elems in elem:
                text += "-"
                text += str(elems)
                text += "\n"
            text += "\n"
        for e, elem in enumerate(nx.cliques_containing_node(G)[osoba]):
            plt.clf()
            fig = plt.gcf()
            G_ex = nx.Graph()
            G_ex.add_nodes_from(elem)
            G_ex.add_edges_from(itertools.combinations(elem, 2))
            nx.spring_layout(G_ex)
            nx.draw(G_ex, with_labels=True)
            fig.set_size_inches(18.5, 10.5)
            plt.savefig(f"graphs\Graph{e}.png", format="png")

        self.set_xy(10.0, height + 50)
        self.set_font('Arial', 'B', 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(w=190.0, h=10.0, align='C', txt=f"Kliki w których jest {osoba}", border=0)
        self.image(f"graphs\Graph0.png", link='', type='', w=185, h=105)
        self.multi_cell(w=190.0, h=10.0, align='C', txt=text, border=0)
        if ilosc_maksymalnych_klik[osoba] > 1:
            self.image(f"graphs\Graph1.png", link='', type='', w=185, h=105)


def create_pdf(name):
    if not os.path.isfile(f"images/{name}/Image_1.jpg"):
        downloader.download(name, limit=1, output_dir='images', adult_filter_off=False, force_replace=False, timeout=60,
                            verbose=True)
    for elem in dane:
        if elem[0] == name:
            kraj = elem[1]
    if not os.path.isfile(f"flags/{kraj} flaga/Image_1.jpg"):
        downloader.download(f"{kraj} flaga", limit=1, output_dir='flags', adult_filter_off=False, force_replace=False,
                            timeout=60,
                            verbose=True)
    pdf = PDF()
    pdf.add_page()
    image = f"images/{name}/Image_1.jpg"
    flag = f"flags/{kraj} flaga/Image_1.jpg"
    pdf.flag(flag)
    pdf.imagex(image)
    pdf.titles(name)
    pdf.info(name, image)
    pdf.set_author('Damian Zawolski')
    pdf.output(f"pdf/{name}.pdf")
    print(f"PDF {name} został utworzony")


print(f"\n\n\n\n\n\n\n\n\n\n\n")
for elem in osoby:
    if not os.path.isfile(f"pdf/{elem['imie']}.pdf"):
        create_pdf(elem["imie"])
