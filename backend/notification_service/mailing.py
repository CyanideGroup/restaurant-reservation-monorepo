import multiprocessing as mp
import smtplib
import traceback

def log_message(message):
    # This is called whenever send_mail(...) succeed and return successful message.
    print (message)

def send_mail (to: str, subject: str, message: str):
    try:
        # Setting up parameters for mailing
        EMAIL_HOST_USER = 'quechi8933@gmail.com'
        EMAIL_HOST_PASSWORD = 'q8u9e3c3hi'
        SERVER = smtplib.SMTP('smtp.gmail.com:587')

        SERVER.ehlo()
        SERVER.starttls()
        SERVER.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        build_msg = "\r\n".join([
            "From: %s" % EMAIL_HOST_USER,
            "To: %s" % to,
            "Subject: %s" % subject,
            "",
            "%s" % message
        ])
        SERVER.sendmail(EMAIL_HOST_USER, to, build_msg)
        SERVER.quit()

    except Exception as e:
        return 'Failed to send email to %s. Details: %' % (to , traceback.format_exc())

    return ('Successful sent email to %s' % to)

def async_send_mail_with_callback(to: str, subject: str, message: str):
    pool = mp.Pool()
    pool.apply_async(send_mail, args = (to, subject, message), callback = log_message)
    pool.close()
    pool.join()

if __name__ == '__main__':
    async_send_mail_with_callback('celery1234@agilekz.com', 'Greetings', "This just a message!")