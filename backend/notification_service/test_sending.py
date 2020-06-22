import multiprocessing as mp
from mailing import async_send_mail_with_callback


def give_it_a_try():
    for i in range(1, 15):
        async_send_mail_with_callback('celery1234@agilekz.com',
                                      'Greettings %d' % i,
                                      'This is my greetings %d to you. '
                                      'Have a good day! Regards,' % i
                                      )


if __name__ == '__main__':
    mp.freeze_support()
    give_it_a_try()