from users.models import User


class UserService:

    @staticmethod
    def user_create(phone, first_name, last_name, tg_user_id):
        new_user = User(phone=phone,
                        first_name=first_name,
                        last_name=last_name,
                        tg_user_id=tg_user_id,
                        password=hash(phone))
        new_user.save()

    @staticmethod
    def check_user_is_registered(phone):
        return User.objects.filter(phone=phone).exists()
