from django import forms

from shop.models import Critery


class PodborForm(forms.Form):
    # CHOICES= Critery.objects.all().order_by('pora_goda').distinct('pora_goda')
    CHOICES = Critery.objects.all()
    print(CHOICES)
    lang_choise=((str(value),str(value) )for elem,value in enumerate(set([elem.pora_goda for elem in CHOICES])))
    vrem_list=((str(value),str(value) )for elem,value in enumerate(set([elem.vremya_sutok for elem in CHOICES])))
    vid_list=((str(value),str(value) )for elem,value in enumerate(set([elem.vid_meropriatia for elem in CHOICES])))
    print(lang_choise)
    # languages = forms.CharField(max_length=200, )
    languages = forms.ChoiceField(choices=lang_choise,label="Пора года:")
    vrem = forms.ChoiceField(choices=vrem_list,label="Время суток:")
    vid = forms.ChoiceField(choices=vid_list,label="Вид мероприятия:")




