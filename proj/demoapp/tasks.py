# Create your tasks here
from time import sleep

# from demoapp.models import Widget

from celery import shared_task, chain
from celery.contrib import rdb
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@shared_task(
    name="soma",
    bind=True,
    max_retry=5,                            # tentará 5 vezes
    default_retry_delay=20,                 # tempo entre as tentativas
    autoretry_for=(TypeError, Exception),   # Caso algum erro na tupla aconteça
    retry_backoff=True,                     # Vai prolongando o tempo de tentativas. A primeira em 1 segundo,
                                            # a segunda em 2s, a terceira em 4s, a quarta em 8s, depois 16, 32...
    # retry_backoff=3                       # O mesmo que acima porém iniciando em 3s, depois 6, 12, 24, 48...
)
def add(self, x, y, count=0):
    logger.info('Fazendo a soma...')
    sleep(3)
    if count > 3:
        return x + y
    raise Exception("Deu erro")


@shared_task(name="multiplica")
def mul(x, y):
    sleep(5)
    return x * y


@shared_task(name="soma_lista")
def xsum(*numbers):
    sleep(5)
    return sum(numbers)

@shared_task
def task_para_debugar():
    # Só em localhost
    rdb.set_trace()     # remote debugger, nativo do celery

    """
    No shell_plus
    from demoapp.tasks import task_para_debugar
    In [3]: task_para_debugar.delay()
    Out[3]: <AsyncResult: 5f1f93ef-fbcc-497e-a1d1-59613db779c9>

    No console do celery veremos:
    Remote Debugger:6908: Ready to connect: telnet 127.0.0.1 6908
    Type `exit` in session to continue.
    Remote Debugger:6908: Waiting for client...
    
    Abrimos outro terminal e fazemos:
    telnet 127.0.0.1 6908
    
    E estamos dentro do debugger do celery:
    Trying 127.0.0.1...
    Connected to 127.0.0.1.
    Escape character is '^]'.
    --Return--
    > /home/amauri/django_celery/proj/demoapp/tasks.py(45)task_para_debugar()->None
    -> rdb.set_trace()     # remote debugger, nativo do celery
    (Pdb) 
    
    Exemplos:
    (Pdb) ll
    42  	@shared_task
    43  	def task_para_debugar():
    44  	    # Só em localhost
    45  ->	    rdb.set_trace()     # remote debugger, nativo do celery
    46 ...
    
    (Pdb) response
    (Pdb) dir(self)
    (Pdb) dir(self.request)
    """


@shared_task(name='Função A')
def a(x):
    return x * 4


@shared_task(name='Função B')
def b(x, y):
    return x + y


chain(a.s(1), b.s(2))()
# b(a(1), 2)
