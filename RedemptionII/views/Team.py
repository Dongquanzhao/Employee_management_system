from RedemptionII import models
from RedemptionII.utils.bootstrap import BootstrapModelForm


from django.shortcuts import render, HttpResponse, redirect


def team_list(request):
    queryset = models.BestTeam.objects.all()
    return render(request, 'team_list.html', {'queryset': queryset})


class UpModelForm(BootstrapModelForm):
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.BestTeam
        fields = '__all__'


def team_add(request):
    """新建团队"""

    title = "新建团队"
    if request.method == 'GET':
        form = UpModelForm()
        return render(request, 'upload_form.html', {'form': form, 'title': title})

    form = UpModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/team/list/')
    return render(request, 'upload_form.html', {'form': form, 'title': title})
