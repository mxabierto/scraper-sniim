import click
import datetime
from pyfiglet import Figlet
from sniim.scrappers.agriculture import ScrapperMarketAgriculture
from sniim.scrappers.livestock import ScrapperMarketLiveStock
from clint.textui import puts, colored, indent

formater_title = Figlet(font='slant')
print(formater_title.renderText('Precios Abastos'))
puts(colored.magenta("FECHA: {}".format(datetime.datetime.today().strftime('%Y/%m/%d'))))

@click.command()
@click.option('--historial/--no-historial', default=False)
def parse(historial):
    agriculture_scrapper = ScrapperMarketAgriculture(is_historic=historial)
    livestock_scrapper = ScrapperMarketLiveStock(is_historic=historial)

    total_records = 0
    total_inserted = 0

    puts(colored.green("Iniciando scrapeo de Precios de Central de Abastos".upper()))
    with indent(4, quote='>>>>'):
        puts(colored.blue(" Scrapper: Productos Agricolas"))
        agriculture_scrapper.scraping()

        with indent(4, quote='>>>>'):
            puts(colored.green(" Resultados"))
            puts(colored.green(" Registros Totales: {}".format(agriculture_scrapper.total_records)))
            puts(colored.green(" Registros Insertados: {}".format(agriculture_scrapper.inserted_records)))
            puts(colored.red(" Registros Incorrectos:{} ".format(agriculture_scrapper.total_records - agriculture_scrapper.inserted_records)))

        puts(colored.blue(" Scrapper: Productos a base de carne"))
        livestock_scrapper.scraping()
        with indent(4, quote='>>>>'):
            puts(colored.green(" Resultados"))
            puts(colored.green(" Registros Totales: {}".format(livestock_scrapper.total_records)))
            puts(colored.green(" Registros Insertados: {}".format(livestock_scrapper.inserted_records)))
            puts(colored.red(" Registros Incorrectos:{} ".format(livestock_scrapper.total_records - livestock_scrapper.inserted_records)))


if __name__ == "__main__":
    parse()
