import abc


class Zviratko(abc.ABC):
    def __init__(self, jmeno):
        self.jmeno = jmeno

    def snez(self, jidlo):
        print(f"{self.jmeno}: {jidlo} mi chutná!")

    @abc.abstractmethod
    def udelej_zvuk(self):
        pass


class Kotatko(Zviratko):
    def __init__(self, jmeno, pocet_zivotu=9):
        super().__init__(jmeno)
        self.pocet_zivotu = pocet_zivotu

    def udelej_zvuk(self):
        print(f"{self.jmeno}: Mňau!")

    def snez(self, jidlo):
        print(f"({self.jmeno} na {jidlo} chvíli fascinovaně kouká)")
        super().snez(jidlo)


class Stenatko(Zviratko):
    def udelej_zvuk(self):
        print(f"{self.jmeno}: Haf!")


class Hadatko(Zviratko):
    def __init__(self, jmeno):
        jmeno = jmeno.replace('s', 'sss')
        jmeno = jmeno.replace('S', 'Sss')
        super().__init__(jmeno)

    def udelej_zvuk(self):
        print(f"{self.jmeno}: Sss!")


standa = Hadatko('Stanislav')
standa.snez('myš')

micka = Kotatko('Micka', 9)
azorek = Stenatko('Azorek')
micka.snez("mys")
azorek.snez('kost')

zviratka = [Kotatko('Micka'), Stenatko('Azorek')]

for zviratko in zviratka:
    zviratko.udelej_zvuk()
    zviratko.snez('flákota')
