from clint.textui import puts, colored, indent


class MeanPriceLiveStock:
    def __init__(self, *args, **kwargs):
        self.html = kwargs.get('html', None)
        self.collection_name = 'bovino_ganado_en_pie'

    def parse(self):
        labels = [
            'estado',
            'cabezas',
            'peso_promedio_kg',
            'precio_novillo_kg',
            'precio_novillona_kg',
            'precio_vaca_kg',
            'precio_toro_kg'
        ]

        for table in self.html.find_all('table'):
            td_class = table.find_all('td', {'class': 'encabTAB'})

            if len(td_class) == 0:
                continue

            if 'Origen' not in td_class[0].text:
                continue

            rastro = None
            fecha = None
            sacrificio = None
            for tr in table.find_all('tr'):

                row = {
                    'rastro': None,
                    'fecha': None,
                    'volumen_sacrificio': None,
                    'estado': None,
                    'cabezas': None,
                    'peso_promedio_kg': None,
                    'precio_novillo_kg': None,
                    'precio_novillona_kg': None,
                    'precio_vaca_kg': None,
                    'precio_toro_kg': None
                }

                tds = tr.find_all('td')
                if len(tds) == 1:
                    rastro = tds[0].text
                    with indent(4):
                        puts(colored.blue("Empacador: {}".format(str(rastro))))
                    # print(rastro)

                if len(tds) == 2:
                    for td in tds:
                        if 'Fecha' in td.text:
                            fecha = td.text.split(':')[1]

                        if 'Volumen de Sacrificio' in td.text:
                            sacrificio = td.text.split(':')[1]

                if len(tds) == 7:
                    row['fecha'] = fecha
                    row['rastro'] = rastro
                    row['volumen_sacrificio'] = sacrificio
                    for element in range(7):
                        row[labels[element]] = tds[element].text

                    yield row



class PackersMeatCuts:
    def __init__(self, *args, **kwargs):
        self.html = kwargs.get('html', None)
        self.collection_name = 'bovino_cortes_empacadoras'
        self.date = kwargs.get('date')

    def parse(self):
        labels = [
            'origen',
            'corte',
            'precio_minimo',
            'precio_maximo'
        ]
        for table in self.html.find_all('table'):
            td_class = table.find_all('td', {'class': 'encabTAB'})

            if len(td_class) == 0:
                continue

            # print(td_class)
            if 'Origen' not in td_class[0].text:
                continue

            packer = None
            for tr in table.find_all('tr'):
                row = {
                    'fecha': self.date,
                    'origen': None,
                    'corte': None,
                    'precio_minimo': None,
                    'precio_maximo': None,
                    'empacadora': None
                }

                tds = tr.find_all('td')
                if len(tds) == 1:
                    packer = tds[0].text
                    with indent(4):
                        puts(colored.blue("Empacador: {}".format(str(packer))))


                if len(tds) == 4:
                    if packer:

                        row['empacadora'] = packer
                        for element in range(4):
                            row[labels[element]] = tds[element].text

                            if labels[element] == 'corte':
                                row[labels[element]] = row[labels[element]].strip()

                        yield row