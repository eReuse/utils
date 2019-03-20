import threading
from time import sleep

import colorama

from ereuse_utils import cli

colorama.init(autoreset=True)
cli.clear()
print('heya!')
l1 = cli.Line(position=0)
l2 = cli.Line(position=1, total=100)


def l1_spin():
    with l1.spin(cli.title('FooING')):
        sleep(4)


def l2_bar():
    l2.set_description_str(cli.title('Bar'))
    sleep(1)
    l2.update(25)
    sleep(1)
    l2.update(25)
    sleep(1)
    l2.update(25)
    sleep(1)
    l2.update(25)


with cli.Line.reserve_lines(2), l1, l2:
    l1.write_at_line(cli.title('Foo'), 'FoING............!!')
    l2.write_at_line(cli.title('Bar'), 'BARING...')
    sleep(2)
    threading.Thread(target=l1_spin).start()
    threading.Thread(target=l2_bar).start()
    sleep(4)
    l1.close_message(cli.title('Foo'), cli.done())
    l1.close()
    l2.close_message(cli.title('Bar'), cli.done())
    l2.close()
print('finished!')
