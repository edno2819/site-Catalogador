from buscas.models import Paridade


def my_scheduled_job(string):
    print(f'{string} {Paridade.objects.all()}')