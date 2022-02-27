from buscas.models import Paridade, Configuraçõe
from buscas.extrator_iq.extract import Extrator
import logging



class CronExtract:
    def __inti__(self):
        self.log = logging.getLogger(__name__)
        self.log.debug("Cron started")
        self.config = Configuraçõe.objects.filter()[0]
        self.ex = Extrator(self.config.login, self.config.senha)

    def extractOne_1_minute(self):
        for par in Paridade.objects.filter():
            self.ex.pipeline('1 1', par.name)


    def extractTwo_1_minute(self):
        print(f'2 {Paridade.objects.all()}')

    def extract_5_minute(self):
        print(f'3 {Paridade.objects.all()}')

    def extract_15_minute(self):
        print(f'4 {Paridade.objects.all()}')
    
    def exclude_one_day_all(self):...


Agend = CronExtract()

def teste():
    print('asdsa')