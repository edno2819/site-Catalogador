from buscas.models import Paridade


def extractOne_1_minute(string):
    print(f'{string} {Paridade.objects.all()}')

def extractTwo_1_minute(string):
    print(f'{string} {Paridade.objects.all()}')

def extract_5_minute(string):
    print(f'{string} {Paridade.objects.all()}')

def extract_15_minute(string):
    print(f'{string} {Paridade.objects.all()}')