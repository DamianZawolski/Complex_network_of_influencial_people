import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

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
