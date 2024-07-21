from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from users.forms import UserRegisterForm, GetKeyForm, RepeatKeyForm
from users.models import User
from users.services import get_key, send_key, create_sessions


class RegisterView(CreateView):
    """
    Регистрация пользователя.
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('publications:list')
    template_name = 'users/register.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if self.model.objects.filter(phone=form.data['phone']).exists():
            return render(self.request, "users/register.html", {'form': form, 'butt_add': True})
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        phone = self.object.phone
        key = get_key()
        self.object.key = key
        self.object.save()

        send_key(phone=phone, key=key)

        return redirect('users:confirm_phone')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    Изменение данных пользователя.
    """
    model = UserRegisterForm,
    success_url = reverse_lazy('publications:list')
    form_class = UserRegisterForm

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def pay_sub(request):
    """
    Оплата подписки.
    """
    user = request.user
    pay_id = create_sessions()["id"]
    user.pay_id = pay_id
    user.save()
    link = create_sessions()["url"]
    context_data = {'link': link}
    return render(request, 'users/pay_sub.html', context_data)


def get_key_user(request):
    """
    Получение и проверка ключа от пользователя.
    """
    if request.method == "POST":
        form = GetKeyForm(request.POST)
        if form.is_valid():
            phone = form.data["phone"]
            key = form.data["key"]
            user = get_object_or_404(User, phone=phone)
            if str(user.key) == str(key) and str(user.phone) == str(phone):
                user.is_active = True
                user.key = None
                user.save()
                return redirect(reverse('users:login'))
            else:
                return render(request, "users/confirm_phone.html", {'form': form, 'butt_add': True})

    return render(request, 'users/confirm_phone.html', {'form': GetKeyForm})


def repeat_key(request):
    """
    Повторная отправка ключа пользователю.
    """
    if request.method == "POST":
        form = RepeatKeyForm(request.POST)
        if form.is_valid():
            phone = form.data["phone"]
            user = User.objects.get(phone=phone)
            token = get_key()
            user.token = token
            user.save()
            send_key(phone, token)

            return redirect(reverse('users:confirm_phone'))

    return render(request, 'users/confirm_phone.html', {'form': RepeatKeyForm})
