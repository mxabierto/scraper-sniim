# encode: utf-8
class PackersMeatCutsLamb:
    def __init__(self, *args, **kwargs):
        self.html = kwargs.get('html', None)
        self.collection_name = 'becerro_cortes_empacadoras'
        self.date = kwargs.get('date')

    def parse(self):
        labels = [
            'fecha',
            'origen',
            'no_canales',
            'precio_minimo',
            'precio_maximo'
        ]

        for table in self.html.find_all('table'):
            td_class = table.find_all('td', {'class': 'encabTAB'})

            if len(td_class) == 0:
                continue

            if 'Fecha' not in td_class[0].text:
                continue

            packer = None
            for tr in table.find_all('tr'):
                row = {
                    'fecha': self.date,
                    'origen': None,
                    'no_canales': None,
                    'precio_minimo': None,
                    'precio_maximo': None,
                    'empacadora': None
                }

                tds = tr.find_all('td')
                if len(tds) == 1:
                    packer = tds[0].text
                    # print(packer)


                if len(tds) == 5:
                    row['empacadora'] = packer
                    for element in range(5):
                        row[labels[element]] = tds[element].text
                        if labels[element] == 'no_canales':
                            row[labels[element]] = row[labels[element]].strip()
                    yield row