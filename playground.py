def napis_hlasku(nazev, skore):
    """Popíše skóre. Název má být přivlastňovací přídavné jméno."""

    print(nazev, 'skóre je', skore)
    if skore > 1000:
        print('Světový rekord!')
        return
    elif skore > 100:
        print('Skvělé!')
        return
    elif skore > 10:
        print('Ucházející.')
        return
    elif skore > 1:
        print('Aspoň něco')
        return

    print('Snad příště.')

napis_hlasku('Tvoje', 256)
napis_hlasku('Protivníkovo', 5)
