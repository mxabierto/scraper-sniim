from clint.textui import puts, colored, indent


class ChickenPartsPackers:
    def __init__(self, *args, **kwargs):
        self.html = kwargs.get('html', None)
        self.collection_name = 'aves_partes_empacadores'
        self.date = kwargs.get('date')

    def parse(self):
        labels = [
            'precio_minimo_kg',
            'precio_maximo_kg',
            'frecuencia_kg'
        ]

        if self.html:
            for table in self.html.find_all('table'):
                headers = table.find_all('td', {'class': 'encabTAB'})

                if len(headers) == 0:
                    continue

                if 'Precios' in headers[0].text == False:
                    continue

                packer = None
                for tr in table.find_all('tr'):
                    tds = tr.find_all('td')

                    if len(tds) == 1 and 'Precios' not in tds[0].text:
                        packer = tds[0].text
                        with indent(4):
                            puts(colored.blue("Empacador: {}".format(str(packer))))
                        # print(packer)

                    if len(tds) == 12:
                        if packer:
                            row = {
                                'fecha': self.date,
                                'pieza': None,
                                'precio_minimo_kg': None,
                                'precio_maximo_kg': None,
                                'frecuencia_kg': None,
                                'empacadora': None
                            }

                            for element in range(1, 12):
                                if element == 0:
                                    continue

                                if element > 0 and element < 4:
                                    row['pieza'] = 'pechuga'
                                    row[labels[element - 1]] = tds[element].text.replace('$', '')

                                if element > 3 and element < 7:
                                    row['pieza'] = 'pierna/muslo'
                                    row[labels[element - 4]] = tds[element].text.replace('$', '')

                                if element > 6 and element < 10:
                                    row['pieza'] = 'retazo'
                                    row[labels[element - 7]] = tds[element].text.replace('$', '')

                                if element > 9:
                                    row['pieza'] = 'visceras'
                                    row[labels[element - 10]] = tds[element].text.replace('$', '')

                                if element == 3 or element == 6 or element == 9 or element == 11:
                                    row['empacadora'] = packer
                                    yield row
                                    row = {
                                        'fecha': self.date,
                                        'pieza': None,
                                        'precio_minimo_kg': None,
                                        'precio_maximo_kg': None,
                                        'frecuencia_kg': None,
                                        'empacadora': None
                                    }
