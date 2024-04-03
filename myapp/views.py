from django.shortcuts import render, redirect
from myapp.models import Immobile, ImmobileImage
from myapp.forms import ClientForm, ImmobileForm, RegisterLocationForm
from django.db.models import Q


def list_location(request):
    immobiles = Immobile.objects.filter(is_locate=False)
    context = {
        'immobiles': immobiles
    }
    return render(request, 'list-location.html', context)

def form_client(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-location')
    return render(request, 'form-client.html', {'form':form})


def form_immobile(request):
    form = ImmobileForm()
    if request.method == 'POST':
        form = ImmobileForm(request.POST, request.FILES)
        if form.is_valid():
            immobile = form.save()
            files = request.FILES.getlist('immobile') ## pega todas as imagens
            if files:
                for f in files:
                    ImmobileImage.objects.create( # Cria instancias para imagens
                        immobile=immobile,
                        image=f
                    )
            return redirect('list-location')
    return render(request, 'form-immobile.html', {'form': form})


def form_location(request, id):
    get_locate = Immobile.objects.get(id=id)
    form = RegisterLocationForm()
    if request.method == 'POST':
        form = RegisterLocationForm(request.POST)
        if form.is_valid():
            location_form = form.save(commit=False)
            location_form.immobile = get_locate ## salva id do imovel
            location_form.save()
            ## muda status do imovel para "Alugado"
            immo = Immobile.objects.get(id=id)
            immo.is_locate = True ## passa a ser true
            immo.save()
            
            return redirect('list-location') ##retorna para lista
    context = {'form':form, 'location': get_locate}
    return render(request, 'form-location.html', context)


def reports(request): # Relatorio
    immobile = Immobile.objects.all()
    get_client = request.GET.get('client')
    get_dt_start = request.GET.get('dt_start')
    get_dt_end = request.GET.get('dt_end')
    type_item = request.GET.get('type_item')
    get_locate = request.GET.get('is_locate')
    
    if get_client: ## filtra por nome e email do client
        immobile = Immobile.objects.filter(
            Q(reg_location__client__name__icontains=get_client) |
            Q(reg_location__client__email__icontains=get_client)
        )
    
    if get_dt_start and get_dt_end: ## Por data
        immobile = Immobile.objects.filter(
            reg_location__create_at__range=[get_dt_start, get_dt_end]
        )
    
    if type_item: ## Tipo de Imóvel
        immobile = Immobile.objects.filter(type_item=type_item)
        
    if get_locate:
        immobile = Immobile.objects.filter(is_locate=get_locate)
    return render(request, 'reports.html', {'immobiles':immobile})

