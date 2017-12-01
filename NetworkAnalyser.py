import sys
import subprocess
import re
import matplotlib.pyplot as plt

//D�claration des variables globales

tab224F = []
tab21AA = []
tab2168 = []
tab59C6 = []
x224F = []
y224F = []
x21AA = []
y21AA = []
x2168 = []
y2168 = []
x59C6 = []
y59C6 = []
add_mac = {}
latency = {}
received_time = {}
send_time = {}
last_send = 0

//Appel du script UNIT.js, sa sortie est stock�e dans un //fichier temporaire "stdout.log"
	
def usePostProcessing():
	with open ("stdout.log","w") as outputFile:
		p = subprocess.call(["nodejs", "UNIT.js", "-f", sys.argv[1], "-p", sys.argv[2]], stdout = outputFile)	
	parsing()
	
//Fonction servant au parsing et � l'affichage du graphique
	
def parsing():
	with open ("stdout.log","r") as parsedFiled:
		i = 0
		received_time = 0
		for line in parsedFiled: 
//recherche des infos ligne par ligne
//a l'aide des expressions r�guliere
			m = re.search(r"\[(?P<add_mac>\w{4})\]", line)
			if m is not None:
				add_mac = m.group("add_mac")
				continue
			m = re.search(r"Message latency#Min/Avg/Max: (?P<latency>\d{1,6})", line)
			if m is not None:
				latency  = int(m.group("latency"))
				continue
			m = re.search(r"Time elapsed since beginning: (?P<received_time>\d{1,6})",line)
			if m is not None:
				i = 1
				received_time = int(m.group("received_time"))
				send_time = received_time - latency
//creation des tableaux avec les valeurs -1/1
				if add_mac == "224F":
					tab224F.append((send_time,1))
					tab224F.append((received_time,-1))
					continue
				if add_mac == "21AA":
					tab21AA.append((send_time,1))
					tab21AA.append((received_time,-1))
					continue
				if add_mac == "2168":
					tab2168.append((send_time,1))
					tab2168.append((received_time,-1))
					continue
				if add_mac == "59C6":
					tab59C6.append((send_time,1))
					tab59C6.append((received_time,-1))
					continue

//Trie des tableaux par temps croissant
	tab224F.sort()
	tab21AA.sort()
	tab2168.sort()
	tab59C6.sort()

	

	mini224F=8000000
	mini21AA=8000000
	mini2168=8000000
	mini59C6=8000000
	sommeCumul = 0
//creation des courbes pour chaque NUC
	for i in tab224Fsorted:
		mini224F = i[-0]
		sommeCumul += i[1]
		x224F.append(i[0])
		y224F.append(sommeCumul)
	sommeCumul = 0
	for i in tab21AA:
		mini21AA = i[-0]
		sommeCumul += i[1]
		x21AA.append(i[0])
		y21AA.append(sommeCumul)
	sommeCumul = 0
	for i in tab2168:
		mini2168 = i[-0]
		sommeCumul += i[1]
		x2168.append(i[0])
		y2168.append(sommeCumul)
	sommeCumul = 0
	for i in tab59C6:
		mini59C6 = i[-0]
		sommeCumul += i[1]
		x59C6.append(i[0])
		y59C6.append(sommeCumul)
	
	last_send = findMinimumFor4(mini224F,mini21AA,mini2168,mini59C6)

//implementation des graphiques � l'aide de matplotlib

	plt.plot(x224F,y224F, label="NUC_1")
	plt.plot(x59C6,y59C6, label="NUC_4")
	plt.plot(x2168,y2168, label="NUC_7")
	plt.plot(x21AA,y21AA, label="NUC_10")	
	plt.axvline(x=last_send, color="black")
	plt.annotate("Dernier paquet envoye", xy=(last_send,0), xytext=(last_send-110000, -1), arrowprops=dict(arrowstyle="-|>", connectionstyle="arc3",facecolor="black"), fontsize=15)
	plt.title("Nb de paquets en transit sur le reseau")
	plt.xlabel("Temps (ms)", fontsize=20)
	plt.ylabel("Nb paquets", fontsize=20)
	plt.legend()
	plt.show()

//fonction pour trouver le minimum de 4 parametres
def findMinimumFor4(a,b,c,d):
	mini = b
	if a < mini:
		mini = a
	if c < mini:
		mini = c
	if d < mini:
		mini = d
	return mini
			
if __name__ == "__main__":
	usePostProcessing()	
