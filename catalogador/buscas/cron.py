from buscas.models import Paridade, Configuraçõe
from buscas.extrator_iq.extract import Extrator
import logging



class CronExtract:
    def __inti__(self):
        self.log = logging.getLogger(__name__)
        self.log.debug("MainOperation started")
        self.login = Configuraçõe
        self.ex = Extrator('edno28@hotmail.com', '99730755ed')

    def extractOne_1_minute(self):
        for par in Paridade:
            self.ex.pipeline('1 1', par)


    def extractTwo_1_minute(self):
        print(f'2 {Paridade.objects.all()}')

    def extract_5_minute(self):
        print(f'3 {Paridade.objects.all()}')

    def extract_15_minute(self):
        print(f'4 {Paridade.objects.all()}')
    
    def exclude_one_day_all(self):...
