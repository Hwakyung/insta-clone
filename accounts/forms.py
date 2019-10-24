from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from .models import User
from django.contrib.auth import get_user_model
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta): #내가 사용할 클래스를 넣어야함
        model = get_user_model() #User라는 반환값을 가짐 클래스를 반환
        fields = ('email','first_name','last_name',)