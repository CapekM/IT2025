print('Slyšela jsem tuto básničku:')
print()

with open('basnicka.txt', encoding='utf-8') as soubor:
    for radek in soubor:
        radek = radek.rstrip()
        print('    ' + radek)

print()
print('Jak se ti líbí?')