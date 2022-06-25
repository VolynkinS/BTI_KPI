from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from kpi.models import Criteria, Indicator, UserAnswer
from kpi.forms import UserLoginForm, UserAnswerForm, NumberStudentsForm, AmountEventForm


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('kpi:home_new_1', pk=1)
    else:
        form = UserLoginForm()
    return render(request, 'kpi/user_login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('kpi:home_new_1', pk=1)


def create_forms(indicators, indicators_len, initial, entries, *, post=None):
    """
    Create GET or POST request forms for each indicator on the page
    """

    forms = {}
    for indicator, x, init_entry in zip(indicators, range(indicators_len), initial):
        if indicator in [entry.indicator for entry in entries]:
            forms[indicator.id] = UserAnswerForm(post, prefix=str(x), instance=entries.get(indicator=indicator))
        else:
            forms[indicator.id] = UserAnswerForm(post, prefix=str(x), initial=init_entry)
    return forms


# def home(request, pk=1):
#     criteria_on_page = Criteria.objects.filter(kpi__pk=pk).prefetch_related('indicator_set', 'indicator_set__category')
#
#     context = {
#         'criteria': criteria_on_page,
#     }
#     return render(request, 'kpi/home.html', context=context)


# https://collingrady.wordpress.com/2008/02/18/editing-multiple-objects-in-django-with-newforms/
def home_2(request, pk=1):
    criteria_on_page = Criteria.objects.filter(kpi__pk=pk).prefetch_related('indicator_set', 'indicator_set__category')
    context = {'criteria': criteria_on_page}

    if request.user.is_authenticated:
        indicators_on_page = Indicator.objects.filter(criteria__kpi__pk=pk)
        indicators_count = indicators_on_page.count()
        entries_user = UserAnswer.objects.filter(user_id=request.user.pk, indicator__in=indicators_on_page)

        initial_list = []
        for indicator in indicators_on_page:
            d = {'indicator': indicator.pk}
            initial_list.append(d)

        # TODO обработать формы, сравнить с категорями индикатора и сохраненить информацию
        if request.method == "POST":
            forms = create_forms(indicators=indicators_on_page, indicators_len=indicators_count, initial=initial_list,
                                 entries=entries_user, post=request.POST)
            if all([form.is_valid() for form in forms.values()]):
                for form in forms.values():
                    new_entry = form.save(commit=False)
                    new_entry.user_id = request.user.pk
                    new_entry.save()

                # Recalculate user's total points
                request.user.total_points = request.user.get_amount_points()
                request.user.save()
                return redirect('kpi:home')
        else:
            if entries_user.exists():
                forms = create_forms(indicators=indicators_on_page, indicators_len=indicators_count,
                                     initial=initial_list, entries=entries_user, post=None)
            else:
                forms = {}
                for indicator, x, init_entry in zip(indicators_on_page, range(indicators_count), initial_list):
                    forms[indicator.id] = UserAnswerForm(prefix=str(x), initial=init_entry)
        context['forms'] = forms

    return render(request, 'kpi/home_2.html', context=context)


def create_forms_new(indicators, form, indicators_len, initial, entries, *, post=None):
    """
    Create GET or POST request forms for each indicator on the page
    """

    # {indicator.id_1: {'form_1': form_1, 'form_2': form_2}, indicator.id_2: {'form_1': form_1, 'form_2': form_2}}
    forms = {}
    if entries:
        for indicator, x, init_entry in zip(indicators, range(indicators_len), initial):
            if indicator in [entry.indicator for entry in entries]:
                form_1 = UserAnswerForm(post, prefix=str(x), instance=entries.get(indicator=indicator))
                form_2 = form(post, prefix=str(x))
                forms[indicator] = {'form_1': form_1, 'form_2': form_2}
            else:
                form_1 = UserAnswerForm(post, prefix=str(x), initial=init_entry)
                form_2 = form(post, prefix=str(x))
                forms[indicator] = {'form_1': form_1, 'form_2': form_2}
    else:
        for indicator, x, init_entry in zip(indicators, range(indicators_len), initial):
            form_1 = UserAnswerForm(post, prefix=str(x), initial=init_entry)
            form_2 = form(post, prefix=str(x))
            forms[indicator] = {'form_1': form_1, 'form_2': form_2}
    return forms


def valid_conditions_1(indicator_current, new_answer, form2_current, request):
    point = None
    percent = form2_current.cleaned_data['students_ok'] / form2_current.cleaned_data['students_all'] * 100

    for category in indicator_current.category.all():
        if category.condition.percent_min <= percent <= category.condition.percent_max:
            point = category.point

    new_answer.user_id = request.user.pk
    new_answer.point = point
    new_answer.text = f'Всего воспитанников: {form2_current.cleaned_data["students_all"]}\n' \
                      f'Кол-во воспитанников подходящих к показателю: {form2_current.cleaned_data["students_ok"]}\n' \
                      f'Процент: {round(percent)}'

    return new_answer


def valid_conditions_3(indicator_current, new_answer, form2_current, request):
    content_text = form2_current.cleaned_data['content']
    content_list = content_text.split('\r\n')
    print(content_list)
    len_text = len(content_text)
    len_list = len(content_list)

    point = None
    if len_text:
        for category in indicator_current.category.all():
            if category.condition3.amount_min <= len_list <= category.condition3.amount_max:
                point = category.point
                # print(len_list, point, category)
    else:
        point = 0

    new_answer.user_id = request.user.pk
    new_answer.point = point
    new_answer.text = f'Количество: {len_list if len_text else len_text}\n' \
                      f'Все названия: {"; ".join(content_list)}\n'
    return new_answer


def valid_conditions_4(indicator_current, new_answer, form2_current, request):
    content_text = form2_current.cleaned_data['content']
    content_list = content_text.split('\r\n')
    len_text = len(content_text)
    len_list = len(content_list)

    point = None
    if len_text:
        for category in indicator_current.category.all():
            if len_text:
                point = category.point
    else:
        point = 0

    new_answer.user_id = request.user.pk
    new_answer.point = point
    new_answer.text = f'Количество: {len_list if len_text else len_text}\n' \
                      f'Все названия: {"; ".join(content_list)}\n'
    return new_answer


def home_new_1(request, pk):
    if pk == 2:
        return redirect('kpi:home_2', pk=2)

    forms_pk = {1: NumberStudentsForm, 2: None, 3: AmountEventForm, 4: AmountEventForm}
    criteria_on_page = Criteria.objects.filter(kpi__pk=pk).prefetch_related('indicator_set', 'indicator_set__category',
                                                                            'indicator_set__category__condition')
    context = {'criteria': criteria_on_page}

    if request.user.is_authenticated:
        indicators_on_page = Indicator.objects.filter(criteria__kpi__pk=pk).\
            prefetch_related('category', 'category__condition')
        indicators_count = indicators_on_page.count()
        entries_user = UserAnswer.objects.filter(user_id=request.user.pk, indicator__in=indicators_on_page)

        # To initialize with default form data
        initial_list = []
        for indicator in indicators_on_page:
            d = {'indicator': indicator.pk}
            initial_list.append(d)

        if request.method == "POST":
            forms = create_forms_new(indicators=indicators_on_page, form=forms_pk[pk],
                                     indicators_len=indicators_count, initial=initial_list,
                                     entries=entries_user, post=request.POST)

            # Validation of all forms
            print('before if form.valid')
            if all([form.is_valid() for i in forms.values() for form in i.values()]):
                for indicator, forms_dict in forms.items():
                    # Get data
                    # form_1, form_2 = UserAnswerForm, NoModelForm=(example: NumberStudentsForm)
                    form_1, form_2 = forms_dict.values()
                    new_answer = form_1.save(commit=False)
                    if pk == 1:
                        new_answer = valid_conditions_1(indicator, new_answer, form_2, request)
                    if pk == 3:
                        new_answer = valid_conditions_3(indicator, new_answer, form_2, request)
                    if pk == 4:
                        new_answer = valid_conditions_4(indicator, new_answer, form_2, request)
                    new_answer.save()

                # Recalculate user's total points
                request.user.total_points = request.user.get_amount_points()
                request.user.save()
                return redirect('kpi:home_2', pk=pk)
        else:
            if entries_user.exists():
                forms = create_forms_new(indicators=indicators_on_page, form=forms_pk[pk],
                                         indicators_len=indicators_count,
                                         initial=initial_list, entries=entries_user, post=None)
            else:
                forms = create_forms_new(indicators=indicators_on_page, form=forms_pk[pk],
                                         indicators_len=indicators_count,
                                         initial=initial_list, entries=False, post=None)
        context['forms'] = forms

    if pk == 1:
        return render(request, 'kpi/home_new_1.html', context=context)
    if pk == 3 or pk == 4:
        return render(request, 'kpi/home_new_3.html', context=context)
