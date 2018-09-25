import datetime
import requests
from bs4 import BeautifulSoup
from sniim.parsers.ganado import MeanPriceLiveStock, PackersMeatCuts
from sniim.parsers.chicken import ChickenPartsPackers
from sniim.db.mongo import Mongoclient
from clint.textui import puts, colored, indent


class ScrapperMarketLiveStock:
    total_records = 0
    inserted_records = 0
    init_urls = [
        ['Bovino cortes: Empacadoras y distribuidoras', 'http://www.economia-sniim.gob.mx/SNIIM-Pecuarios-Nacionales/e_Cor.asp', PackersMeatCuts, 'carnes_bovino'],
        ['Pollo por partes: Empacadoras y distribuidoras' ,'http://www.economia-sniim.gob.mx/SNIIM-Pecuarios-Nacionales/e_Pza.asp', ChickenPartsPackers, 'carnes_pollo']
    ]

    def __init__(self, *args, **kwargs):
        self.is_historic = kwargs.get('is_historic', True)

    def read_category(self, category, url, parser, collection):
        from dateutil.relativedelta import relativedelta

        self.mongo = Mongoclient(db_collection=collection)
        delta_day = datetime.timedelta(days=-1)
        delta_month = relativedelta(months=1)

        with indent(4):
            puts(colored.magenta("Categoria: {}".format(str(category))))

        if self.is_historic:
            for year in range(2000, 2019):
                for month in range(1, 13):
                    init_date = datetime.datetime.strptime('01/{0}/{1}'.format(month, year), '%d/%m/%Y')
                    final_date = init_date + delta_month + delta_day

                    payload = {
                        'origen': '0',
                        'destino': '0',
                        'del': '1',
                        'al': final_date.day,
                        'mes': final_date.strftime('%m'),
                        'anio': str(year),
                        'RegPag': '1000',
                        'x': '45',
                        'y': '20',
                        'Var': 'Bov'
                    }

                    html = self.gather_prices(payload, url)

                    if not html:
                        next

                    parser_object = parser(html=html)

                    for row_c in parser_object.parse():
                        with indent(4):
                            puts(colored.yellow("Insertando: {}".format(str(row_c))))
                        if self.mongo.insert_one(row_c):
                            self.inserted_records += 1
                            with indent(4):
                                puts(colored.green("Insertado: {}".format(str(row_c))))
                        else:
                            with indent(4):
                                puts(colored.red("No Insertado: {}".format(str(row_c))))

                        self.total_records += 1
        else:
            payload = {
                'origen': '0',
                'destino': '0',
                'del': datetime.datetime.today().day,
                'al': datetime.datetime.today().day,
                'mes': datetime.datetime.today().strftime('%m'),
                'anio': datetime.datetime.today().year,
                'RegPag': '1000',
                'x': '45',
                'y': '20',
                'Var': 'Bov'
            }

            html = self.gather_prices(payload, url)

            if not html:
                next

            try:
                parser_object = parser(html=html, date=datetime.datetime.today().strftime('%d/%m/%Y'))
            except Exception as error:
                with indent(4):
                    puts(colored.red("Error en el parseo: {}".format(str(error))))

            for row in parser_object.parse():
                with indent(4):
                    puts(colored.yellow("Insertando: {}".format(str(row))))
                if self.mongo.insert_one(row):
                    self.inserted_records += 1
                    with indent(4):
                        puts(colored.green("Insertado: {}".format(str(row))))
                else:
                    with indent(4):
                        puts(colored.red("No Insertado: {}".format(str(row))))

                self.total_records += 1

    def gather_prices(self, payload, url):
        with indent(4):
            puts(colored.blue("Peticion: {}".format(str(payload))))

        response = requests.get(url, params=payload)

        if response.status_code != 200:
            with indent(4):
                puts(colored.red("Error en la peticion HTTP: {}".format(str(response.text))))

            return None

        html_response = BeautifulSoup(response.content, features="html.parser")

        return html_response

    def scraping(self):
        for category, url, parser, collection in self.init_urls:
            self.read_category(category, url, parser, collection)
