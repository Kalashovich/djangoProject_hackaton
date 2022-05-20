from django.core.mail import send_mail


def confirmation_email(user):
    code = user.activation_code
    link = f'http://localhost:8000/api/v1/account/activate/{code}/'
    to_email = user.email
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке: {link}',
        'from@exmaple.com',
        [to_email],
        fail_silently=False,
    )


def reset_password(user):
    code = user.activation_code
    to_email = user.email
    send_mail(
        'Восстановление пароля',
        f'Ваш личный код: {code}',
        'Не передавайте его НИКОМУ',
        'from@example.com',
        [to_email,],
        fail_silently=False,
    )









































