from django.shortcuts import render
from hug.forms import UserForm, UserProfileForm, PhotoForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from hug.models import Tree, UserProfile, FoodTree, Park, Photo, Tag
from django.shortcuts import get_object_or_404


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {}
    context_dict['trees'] = Tree.objects.filter(neighbourhood='RENFREW - COLLINGWOOD')
    result = []
    usedtree=Tree.objects.values_list('commonName', flat=True).distinct()
    for tree1 in usedtree:
        result.append(tree1)
    treelis=set(result)
    treelist=list(treelis)
    treelists=sorted(treelist)
    context_dict['gms']=treelists
    context_dict['food_trees'] = FoodTree.objects.all()
    context_dict['parks'] = Park.objects.all()
    if request.user.is_authenticated():
       context_dict['treess'] = request.user.userprofile.tree.all()
       context_dict['parkss'] = request.user.userprofile.park.all()
       context_dict['foodtreess'] = request.user.userprofile.foodtree.all()
    else:
       context_dict['trees'] = Tree.objects.filter(neighbourhood='RENFREW - COLLINGWOOD')
       context_dict['parks'] = Park.objects.all()
       context_dict['food_trees'] = FoodTree.objects.all()

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request, 'hug/index.html', context_dict)

#http://stackoverflow.com/questions/24789149/django-manytomanyfield-in-action
@login_required
def add_fav(request, entry_pk):
     entry = get_object_or_404(Tree, pk=entry_pk)
     try:
            favorite = UserProfile.objects.get(user=request.user)
     except UserProfile.DoesNotExist:
          #If not we create a new favorite object
            favorite = UserProfile.objects.create(user=request.user)
     favorite.tree.add(entry)
     favorite.save()
     return HttpResponseRedirect(reverse('favourites'))

@login_required
def add_favp(request, entry_pk):
     entry = get_object_or_404(Park, pk=entry_pk)
     try:
            favorite = UserProfile.objects.get(user=request.user)
     except UserProfile.DoesNotExist:
          #If not we create a new favorite object
            favorite = UserProfile.objects.create(user=request.user)
     favorite.park.add(entry)
     favorite.save()
     return HttpResponseRedirect(reverse('favourites'))

@login_required
def add_favf(request, entry_pk):
     entry = get_object_or_404(FoodTree, pk=entry_pk)
     try:
            favorite = UserProfile.objects.get(user=request.user)
     except UserProfile.DoesNotExist:
          #If not we create a new favorite object
            favorite = UserProfile.objects.create(user=request.user)
     favorite.foodtree.add(entry)
     favorite.save()
     return HttpResponseRedirect(reverse('favourites'))

@login_required
def delete_fav(request, entry_pk):
     entry = get_object_or_404(Tree, pk=entry_pk)
     try:
            favorite = UserProfile.objects.get(user=request.user)
     except UserProfile.DoesNotExist:
          #If not we create a new favorite object
            favorite = UserProfile.objects.create(user=request.user)
     favorite.tree.remove(entry)
     favorite.save()
     return HttpResponseRedirect(reverse('favourites'))

@login_required
def delete_favp(request, entry_pk):
     entry = get_object_or_404(Park, pk=entry_pk)
     try:
            favorite = UserProfile.objects.get(user=request.user)
     except UserProfile.DoesNotExist:
          #If not we create a new favorite object
            favorite = UserProfile.objects.create(user=request.user)
     favorite.park.remove(entry)
     favorite.save()
     return HttpResponseRedirect(reverse('favourites'))

@login_required
def delete_favf(request, entry_pk):
     entry = get_object_or_404(FoodTree, pk=entry_pk)
     try:
            favorite = UserProfile.objects.get(user=request.user)
     except UserProfile.DoesNotExist:
          #If not we create a new favorite object
            favorite = UserProfile.objects.create(user=request.user)
     favorite.foodtree.remove(entry)
     favorite.save()
     return HttpResponseRedirect(reverse('favourites'))


def about(request):
    return render(request, 'hug/about.html')


def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'hug/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/hug/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your hug account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'hug/login.html', {})


@login_required
def restricted(request):
    return render(request, 'hug/restricted.html')


    # Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/hug/')

@login_required
def profile(request):
    return render(request, 'hug/profile.html')

@login_required
def favourites(request):
    context_dict = {}
    context_dict['trees'] = request.user.userprofile.tree.all()
    context_dict['foodtrees'] = request.user.userprofile.foodtree.all()
    context_dict['parks'] = request.user.userprofile.park.all()
    return render(request, 'hug/favourites.html', context_dict)

def tree(request, treeId):
    context_dict = {}
    photos = Photo.objects.all()
    res =[]
    try:
        tree = Tree.objects.get(treeId=treeId)
        photot = tree.photo.all()
        context_dict['neighbourhood'] = tree.neighbourhood
        context_dict['treeId'] = tree.treeId
        context_dict['commonName'] = tree.commonName
        context_dict['diameter'] = tree.diameter
        context_dict['streetNumber'] = tree.streetNumber
        context_dict['street'] = tree.street
        context_dict['photot'] = tree.photo.all()
        context_dict['tree'] = tree
        context_dict['photos'] = Photo.objects.all()
        context_dict['tags'] = Tag.objects.all()
        for photo in photos:
            ptags = photo.tags.all()
            res.append(ptags)
            context_dict['ptags'] = res
        if request.user.is_authenticated():
            context_dict['treess'] = request.user.userprofile.tree.all()

        else:
            context_dict['tree'] = tree
    except Tree.DoesNotExist:
        pass
    return render(request, 'hug/tree.html', context_dict)

def foodtree(request, foodtree_name_slug):
    context_dict = {}
    la = []
    try:
        ft = FoodTree.objects.get(slug=foodtree_name_slug)
        context_dict['name'] = ft.name
        context_dict['address'] = ft.address
        context_dict['lat'] = ft.lat
        context_dict['lon'] = ft.lon
        context_dict['numOfFT'] = ft.numOfFT
        context_dict['typesOfFT'] = ft.typesOfFT
        context_dict['neighbourhood'] = ft.neighbourhood
        context_dict['ft'] = ft
        context_dict['foodtree_name_slug'] = foodtree_name_slug
        context_dict['photoft'] = ft.photo.all()
        context_dict['photos'] = Photo.objects.all()
        context_dict['tags'] = Tag.objects.all()
        context_dict['foodtrees'] = FoodTree.objects.all()
        if request.user.is_authenticated():
            foodtreess = request.user.userprofile.foodtree.all()
            context_dict['foodtreess'] = request.user.userprofile.foodtree.all()
            for foodtree in foodtreess:
                la.append(foodtree.name)
            context_dict['foodtreest'] = la
        else:
            context_dict['ft'] = la

    except FoodTree.DoesNotExist:
        pass
    return render(request, 'hug/foodtree.html', context_dict)

def park(request, parkId):
    context_dict = {}
    try:
        park = Park.objects.get(parkId=parkId)
        context_dict['parkId'] = park.parkId
        context_dict['name'] = park.name
        context_dict['address'] = park.address
        context_dict['lat'] = park.lat
        context_dict['lon'] = park.lon
        context_dict['neighbourhood'] = park.neighbourhood
        context_dict['park'] = park
        context_dict['photop'] = park.photo.all()
        context_dict['photos'] = Photo.objects.all()
        context_dict['tags'] = Tag.objects.all()
        if request.user.is_authenticated():
            context_dict['parkss'] = request.user.userprofile.park.all()
        else:
            context_dict['park'] = park

    except Park.DoesNotExist:
        pass
    return render(request, 'hug/park.html', context_dict)



def add_photot(request, treeId):
    added = False
    try:
        tree = Tree.objects.get(treeId=treeId)
    except Tree.DoesNotExist:
        tree = None

    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid() and tree:
            photo = form.save(commit=False)
            photo.id = id(photo)
            photo.approved = False
            photo.comm = request.POST.get('comm')
            if 'picture' in request.FILES:
                photo.picture = request.FILES['picture']
            photo.save()
            if 'tags' in request.POST:
                tags = request.POST.get('tags')
                tag = tags.split()
                for each in tag:
                    newtag = Tag.objects.get_or_create(tag=each)[0]
                    newtag.save()
                    photo.tags.add(newtag)
            tree.photo.add(photo)
            added = True
        else:
            print(form.errors)
    else:
        form = PhotoForm()

    context_dict = {'form': form, 'tree': tree, 'treeId': treeId, 'added': added}

    return render(request, 'hug/add_photot.html', context_dict)


def add_photoft(request, foodtree_name_slug):
    added = False
    try:
        ft = FoodTree.objects.get(slug=foodtree_name_slug)
    except FoodTree.DoesNotExist:
        ft = None

    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid() and ft:
            photo = form.save(commit=False)
            photo.id = id(photo)
            photo.approved = False
            photo.comm = request.POST.get('comm')
            if 'picture' in request.FILES:
                photo.picture = request.FILES['picture']
            photo.save()
            if 'tags' in request.POST:
                tags = request.POST.get('tags')
                tag = tags.split()
                for each in tag:
                    newtag = Tag.objects.get_or_create(tag=each)[0]
                    newtag.save()
                    photo.tags.add(newtag)
            ft.photo.add(photo)
            added = True
        else:
            print(form.errors)
    else:
        form = PhotoForm()

    context_dict = {'form': form, 'ft': ft, 'slug': foodtree_name_slug, 'added': added}

    return render(request, 'hug/add_photoft.html', context_dict)


def add_photop(request, parkId):
    added = False
    try:
        park = Park.objects.get(parkId=parkId)
    except Park.DoesNotExist:
        park = None

    if request.method == 'POST':
        form = PhotoForm(request.POST)
        if form.is_valid() and park:
            photo = form.save(commit=False)
            photo.id = id(photo)
            photo.approved = False
            photo.comm = request.POST.get('comm')
            if 'picture' in request.FILES:
                photo.picture = request.FILES['picture']
            photo.save()
            if 'tags' in request.POST:
                tags = request.POST.get('tags')
                tag = tags.split()
                for each in tag:
                    newtag = Tag.objects.get_or_create(tag=each)[0]
                    newtag.save()
                    photo.tags.add(newtag)
            park.photo.add(photo)
            added = True
        else:
            print(form.errors)
    else:
        form = PhotoForm()

    context_dict = {'form': form, 'park': park, 'parkId': parkId, 'added': added}

    return render(request, 'hug/add_photop.html', context_dict)

def tag(request, tag_slug):
    context_dict = {}
    try:
        photos = Photo.objects.all()
        photolist = []
        for photo in photos:
            tags = photo.tags.all()
            if any(tag.slug == tag_slug for tag in tags):
                photolist.append(photo)
        context_dict['tag_slug'] = tag_slug
        context_dict['photos'] = photolist

    except Tag.DoesNotExist:
        pass
    return render(request, 'hug/tag.html', context_dict)
