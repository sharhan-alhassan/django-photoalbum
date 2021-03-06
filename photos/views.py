

from django.shortcuts import redirect, render

from .models import Category, Photo

# Create your views here.

def gallery(request):
    
    category = request.GET.get('category')
    if category == None:
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name__icontains=category)

    categories = Category.objects.all()
    context = {'photos': photos, 'categories': categories}
    return render(request, 'photos/gallery.html', context)


def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})

def addPhoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            # if the category is there and selected
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            # if the category is NOT there, then create it. Returns a tuple(object, created)
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            # else you can decide not to choose any category
            category = None

        for image in images:
            photo = Photo.objects.create(
                category=category,
                description = data['description'],
                image = image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)


def deletePhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    photo.delete()

    return redirect('gallery')