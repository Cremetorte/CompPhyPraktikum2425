import csv

#Dateiname ohne Endung
name = "1kbody"

#Stammpfad
path = "Thema 1 - N-Body Problem/Input/"

# Eingabedatei
input_file = path + name + ".dat"
# Ausgabedatei
output_file = path + name + ".csv"

# Öffne die Eingabedatei und die Ausgabedatei
with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    # Leser mit Leerzeichen als Trennzeichen
    reader = csv.reader(infile, delimiter=' ')
    # Schreibe in die CSV-Datei
    writer = csv.writer(outfile)

    for row in reader:
        # Filtere leere Strings
        filtered_row = [value for value in row if value]
        writer.writerow(filtered_row)