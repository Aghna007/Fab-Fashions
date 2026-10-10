from django.shortcuts import render,redirect
from django.http import HttpResponse
from.import models
import re

# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
            
        if models.Register.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exists');window.history.back();</script>")
        # Name
        if not re.fullmatch(r"[A-Za-z ]+", name):
            return HttpResponse("<script>alert('Name should contain only letters');window.history.back();</script>")

# Phone
        if not phone.isdigit():
            return HttpResponse("<script>alert('Phone should contain only numbers');window.history.back();</script>")

        if len(phone) != 10:
            return HttpResponse("<script>alert('Phone number should be 10 digits');window.history.back();</script>")

# Password
        if len(password) < 8:
            return HttpResponse("<script>alert('Password should be at least 8 characters');window.history.back();</script>")
        
        user = models.Register.objects.create(
            name=name,
            email=email,
            address=address,
            gender=gender,
            phone=phone,
            password=password,
            image=image
            )
        user.save()
        return redirect('Login')

    return render(request, 'register.html')



def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user=models.Register.objects.get(email=email)
            if user.password == password:
                request.session ['email']=email
                return redirect('home')
            else:
                return HttpResponse('Invalid Password')
        except models.Register.DoesNotExist:
            return HttpResponse('User Not Found')
    else:
        return render(request,'Login.html')




def home(request):
    if 'email' not in request.session:
        return redirect('Login')
    else:
        return render(request,'home.html')


def logout(request):
    request.session.flush()
    return redirect('index')


def profile(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user=models.Register.objects.get(email=email)
        return render(request,'profile.html',{'user':user})
    return redirect('Login')



def editprofile(request):
    if 'email' not in request.session:
        return redirect('Login')

    email = request.session.get('email')

    try:
        user = models.Register.objects.get(email=email)

        if request.method == "POST":

            name = request.POST.get('name')
            address = request.POST.get('address')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')

            # Name Validation
            if not re.fullmatch(r"[A-Za-z ]+", name):
                return HttpResponse("<script>alert('Name should contain only letters.');window.history.back();</script>")

            # Phone Validation
            if not phone.isdigit():
                return HttpResponse("<script>alert('Phone number should contain only digits.');window.history.back();</script>")

            if len(phone) != 10:
                return HttpResponse("<script>alert('Phone number must be exactly 10 digits.');window.history.back();</script>")

            # Image Validation
            if 'image' in request.FILES:
                image = request.FILES['image']

                if not image.content_type.startswith('image'):
                    return HttpResponse("<script>alert('Upload only image files.');window.history.back();</script>")

                user.image = image

            user.name = name
            user.address = address
            user.gender = gender
            user.phone = phone

            user.save()

            return redirect('Profile')

        return render(request, 'editprofile.html', {'user': user})

    except models.Register.DoesNotExist:
        return redirect('Login')




def productlist_user(request):
    product = models.dress.objects.all()
    return render(request,'productlist_user.html',{'product':product})

    


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "admin":
            if password == "admin123":
                return redirect('adminhome')
            else:
                return HttpResponse('Invalid Password')
        else:
            return HttpResponse('Invalid Username')
       
    else:
        return render(request,'adminlogin.html')
    


def adminhome(request):
    return render(request,'adminhome.html')



def productlist_admin(request):
    product = models.dress.objects.all()
    return render(request,'productlist_admin.html',{'product':product})



def userlist_admin(request):
    user=models.Register.objects.all()
    return render(request,'userlist_admin.html',{'user':user})


def editproduct(request,id):
    product=models.dress.objects.get(id=id)
    if request.method=="POST":
        product.name=request.POST.get('name')
        product.price=request.POST.get('price')
        product.brand=request.POST.get('brand')
        product.size=request.POST.get('size')
        product.material=request.POST.get('material')
        product.neckline=request.POST.get('neckline')
        product.sleeve_length=request.POST.get('sleeve_length')
        product.length=request.POST.get('length')
        product.color=request.POST.get('color')
        product.pattern=request.POST.get('pattern')
        if request.FILES:
            product.image=request.FILES.get('image')
        product.description =request.POST.get('description ')
        product.save()
        return redirect ('productlist_admin')
    return render(request,'editproduct.html',{'product':product})
    

def deleteproduct(request,id):
    product=models.dress.objects.get(id=id)
    product.delete()
    return redirect('productlist_admin')




def addproducts(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        price = request.POST.get('price')
        brand = request.POST.get('brand')
        size = request.POST.get('size')
        material = request.POST.get('material')
        neckline = request.POST.get('neckline')
        sleeve_length = request.POST.get('sleeve_length')
        length = request.POST.get('length')
        color = request.POST.get('color')
        pattern = request.POST.get('pattern')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        # -----------------------------
        # Product Name Validation
        # -----------------------------
        if not name:
            return HttpResponse("<script>alert('Product name is required.');window.history.back();</script>")

        if not re.fullmatch(r"[A-Za-z0-9 ]+", name):
            return HttpResponse("<script>alert('Product name should contain only letters and numbers.');window.history.back();</script>")

        # -----------------------------
        # Price Validation
        # -----------------------------
        if not price:
            return HttpResponse("<script>alert('Price is required.');window.history.back();</script>")

        try:
            price = float(price)

            if price <= 0:
                return HttpResponse("<script>alert('Price must be greater than zero.');window.history.back();</script>")

        except ValueError:
            return HttpResponse("<script>alert('Enter a valid price.');window.history.back();</script>")

        # -----------------------------
        # Brand Validation
        # -----------------------------
        if brand:

            if not re.fullmatch(r"[A-Za-z0-9 ]+", brand):
                return HttpResponse("<script>alert('Brand should contain only letters and numbers.');window.history.back();</script>")

        # -----------------------------
        # Size Validation
        # -----------------------------
        if size:

            if not re.fullmatch(r"[A-Za-z0-9,+ ]+", size):
                return HttpResponse("<script>alert('Enter a valid size.');window.history.back();</script>")

        # -----------------------------
        # Material Validation
        # -----------------------------
        if material:

            if not re.fullmatch(r"[A-Za-z ]+", material):
                return HttpResponse("<script>alert('Material should contain only letters.');window.history.back();</script>")

        # -----------------------------
        # Neckline Validation
        # -----------------------------
        if neckline:

            if not re.fullmatch(r"[A-Za-z ]+", neckline):
                return HttpResponse("<script>alert('Neckline should contain only letters.');window.history.back();</script>")

        # -----------------------------
        # Sleeve Validation
        # -----------------------------
        if sleeve_length:

            if not re.fullmatch(r"[A-Za-z ]+", sleeve_length):
                return HttpResponse("<script>alert('Sleeve length should contain only letters.');window.history.back();</script>")

        # -----------------------------
        # Length Validation
        # -----------------------------
        if length:

            if not re.fullmatch(r"[A-Za-z ]+", length):
                return HttpResponse("<script>alert('Length should contain only letters.');window.history.back();</script>")

        # -----------------------------
        # Color Validation
        # -----------------------------
        if color:

            if not re.fullmatch(r"[A-Za-z ]+", color):
                return HttpResponse("<script>alert('Color should contain only letters.');window.history.back();</script>")

        # -----------------------------
        # Pattern Validation
        # -----------------------------
        if pattern:

            if not re.fullmatch(r"[A-Za-z ]+", pattern):
                return HttpResponse("<script>alert('Pattern should contain only letters.');window.history.back();</script>")

        # -----------------------------
        # Description Validation
        # -----------------------------
        if not description:

            return HttpResponse("<script>alert('Description is required.');window.history.back();</script>")

        if len(description) < 10:

            return HttpResponse("<script>alert('Description should contain at least 10 characters.');window.history.back();</script>")

        # -----------------------------
        # Image Validation
        # -----------------------------
        if not image:

            return HttpResponse("<script>alert('Please upload an image.');window.history.back();</script>")

        if not image.content_type.startswith("image"):

            return HttpResponse("<script>alert('Upload only image files.');window.history.back();</script>")

        # -----------------------------
        # Save Product
        # -----------------------------
        models.dress.objects.create(

            name=name,
            price=price,
            brand=brand,
            size=size,
            material=material,
            neckline=neckline,
            sleeve_length=sleeve_length,
            length=length,
            color=color,
            pattern=pattern,
            image=image,

            # If your model field is named "discription",
            # keep this line.
            discription=description

            # If you renamed the model field to "description",
            # use:
            # description=description
        )

        return redirect('productlist_admin')

    return render(request, 'addproducts.html')



def shopowner_register(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        shop_name = request.POST.get('shop_name')
        shop_address = request.POST.get('shop_address')
        place = request.POST.get('place')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')

        # Name validation
        if not re.fullmatch(r"[A-Za-z ]+", name):
            return HttpResponse("<script>alert('Owner name should contain only letters.');window.history.back();</script>")

        # Shop Name validation
        if not re.fullmatch(r"[A-Za-z0-9 ]+", shop_name):
            return HttpResponse("<script>alert('Shop name should contain only letters and numbers.');window.history.back();</script>")

        # Place validation
        if not re.fullmatch(r"[A-Za-z ]+", place):
            return HttpResponse("<script>alert('Place should contain only letters.');window.history.back();</script>")

        # Phone validation
        if not phone.isdigit():
            return HttpResponse("<script>alert('Phone number should contain only digits.');window.history.back();</script>")

        if len(phone) != 10:
            return HttpResponse("<script>alert('Phone number must be exactly 10 digits.');window.history.back();</script>")

        # Password validation
        if len(password) < 8:
            return HttpResponse("<script>alert('Password must be at least 8 characters.');window.history.back();</script>")

        # Email validation
        if models.shopowner_register.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exists.');window.history.back();</script>")

        # Image validation
        if image and not image.content_type.startswith("image"):
            return HttpResponse("<script>alert('Upload only image files.');window.history.back();</script>")

        models.shopowner_register.objects.create(
            name=name,
            shop_name=shop_name,
            shop_address=shop_address,
            place=place,
            phone=phone,
            email=email,
            password=password,
            image=image
        )

        return redirect('owner_login')

    return render(request, 'shopowner_register.html')



def owner_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user=models.shopowner_register.objects.get(email=email)
            if user.password == password:
                request.session ['email']=email
                return redirect('owner_home')
            else:
                return HttpResponse('Invalid Password')
        except models.shopowner_register.DoesNotExist:
            return HttpResponse('User Not Found')
    else:
        return render(request,'owner_login.html')
    

def owner_home(request):
    if 'email' not in request.session:
        return redirect('owner_login')
    else:
        return render(request,'owner_home.html')



def owner_profile(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user=models.shopowner_register.objects.get(email=email)
        return render(request,'owner_profile.html',{'user':user})
    return redirect('owner_login')


def owner_editprofile(request):

    if 'email' not in request.session:
        return redirect('owner_login')

    email = request.session.get('email')

    try:
        user = models.shopowner_register.objects.get(email=email)

        if request.method == "POST":

            name = request.POST.get('name')
            shop_name = request.POST.get('shop_name')
            shop_address = request.POST.get('shop_address')
            place = request.POST.get('place')
            phone = request.POST.get('phone')

            # Owner Name
            if not re.fullmatch(r"[A-Za-z ]+", name):
                return HttpResponse("<script>alert('Owner name should contain only letters.');window.history.back();</script>")

            # Shop Name
            if not re.fullmatch(r"[A-Za-z0-9 ]+", shop_name):
                return HttpResponse("<script>alert('Shop name should contain only letters and numbers.');window.history.back();</script>")

            # Place
            if not re.fullmatch(r"[A-Za-z ]+", place):
                return HttpResponse("<script>alert('Place should contain only letters.');window.history.back();</script>")

            # Phone
            if not phone.isdigit():
                return HttpResponse("<script>alert('Phone number should contain only digits.');window.history.back();</script>")

            if len(phone) != 10:
                return HttpResponse("<script>alert('Phone number must be exactly 10 digits.');window.history.back();</script>")

            # Image Validation
            if 'image' in request.FILES:

                image = request.FILES['image']

                if not image.content_type.startswith("image"):
                    return HttpResponse("<script>alert('Upload only image files.');window.history.back();</script>")

                user.image = image

            user.name = name
            user.shop_name = shop_name
            user.shop_address = shop_address
            user.place = place
            user.phone = phone

            user.save()

            return redirect('owner_profile')

        return render(request, 'owner_editprofile.html', {'user': user})

    except models.shopowner_register.DoesNotExist:
        return redirect('owner_login')


def addproducts_owner(request):
    
    if 'email' in request.session:
        email=request.session.get('email')
        user=models.shopowner_register.objects.get(email=email)

        if request.method == 'POST':
            name = request.POST.get('name')
            price = request.POST.get('price')
            brand = request.POST.get('brand')
            size = request.POST.get('size')
            material = request.POST.get('material')
            neckline = request.POST.get('neckline')
            sleeve_length = request.POST.get('sleeve_length')
            color = request.POST.get('color')
            pattern = request.POST.get('pattern')
            image = request.FILES.get('image')
            discription = request.POST.get('discription')
        

            product=models.dress.objects.create(
                name=name,
                user=user,
                price=price,
                brand=brand,
                size=size,
                material=material,
                neckline=neckline,
                sleeve_length=sleeve_length,
                color=color,
                pattern=pattern,
                image=image,
                discription=discription
                )
            product.save()
            return redirect('owner_home')
        return render(request, 'addproducts_owner.html')
    return redirect(owner_login)


def productlist_shop(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user = models.shopowner_register.objects.get(email=email)
        product = models.dress.objects.filter(user=user)
        return render(request,'productlist_shop.html',{'products':product})
    return redirect('Login')



def editproduct_owner(request,id):
    product=models.dress.objects.get(id=id)
    if request.method=="POST":
        product.name=request.POST.get('name')
        product.price=request.POST.get('price')
        product.brand=request.POST.get('brand')
        product.size=request.POST.get('size')
        product.material=request.POST.get('material')
        product.neckline=request.POST.get('neckline')
        product.sleeve_length=request.POST.get('sleeve_length')
        product.length=request.POST.get('length')
        product.color=request.POST.get('color')
        product.pattern=request.POST.get('pattern')
        if request.FILES:
            product.image=request.FILES.get('image')
        product.description =request.POST.get('description ')
        product.save()
        return redirect ('productlist_shop')
    return render(request,'editproduct_owner.html',{'product':product})

 

def add_to_cart(request,id):
    if 'email' not in request.session:
        return redirect('Login')
    email=request.session.get('email')
    try:
        p = models.dress.objects.get(id=id)
        u = models.Register.objects.get(email=email)
        cart_item = models.cart.objects.filter(user = u,products= p).first()
        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            models.cart.objects.create(user = u,products=p, quantity = 1)
        return redirect('cart_list')
    except models.dress.DoesNotExist:
        return HttpResponse('product not added')
    


def cart_list(request):
    if 'email' not in request.session:
        return redirect('Login')

    email = request.session.get('email')
    user = models.Register.objects.get(email=email)

    cart_items = models.cart.objects.filter(user=user)

    total_price = 0

    for item in cart_items:
        item.item_total = item.quantity * item.products.price
        total_price += item.item_total

    return render(
        request,
        'cart_items.html',
        {
            'cart_items': cart_items,
            'total_price': total_price,
            'user': user
        }
    )



def remove_from_cart(request, id):
    if 'email' not in request.session:
        return redirect('Login')

    email = request.session.get('email')
    user = models.Register.objects.get(email=email)

    models.cart.objects.filter(id=id, user=user).delete()

    return redirect('cart_list')


def product_detail(request,id):
    p=models.dress.objects.get(id=id)
    return render(request,'product_detail.html',{'product':p})


def buy_now(request,id):
    if request.method!='POST':
        return redirect('product_detail',id=id)
    if 'email' not in request.session:
        return redirect('Login')
    qty=request.POST.get('quantity','1')
    try:
        qty=int(qty)
        if qty<1:
            qty=1
    except ValueError:
        qty=1
    p = models.dress.objects.get(id=id)
    u = models.Register.objects.get(email=request.session['email'])
    total = qty*p.price
    models.order.objects.create(user=u,products=p,quantity=qty,total_price=total)

    p.quantity=p.quantity-qty
    p.save()
    return render(request,'checkout_success.html',{'user':u})


def checkout(request):
    if'email' not in request.session:
        return redirect('Login')

    u=models.Register.objects.get(email=request.session['email'])
    cart_items=models.cart.objects.filter(user=u)

    if not cart_items:
        return redirect('cart_list')

    for item in cart_items:
        total=item.quantity*item.products.price
        models.order.objects.create(user=u,products=item.products,quantity=item.quantity,total_price=total)
        p=item.products
        try:
            p.quantity=p.quantity-item.quantity
            p.save()
        except Exception:
            pass
    cart_items.delete()
    return render(request,'checkout_success.html',{'user':u})


def orderlist_user(request):
    if'email' not in request.session:
        return redirect('Login')
    email=request.session['email']
    user=models.Register.objects.get(email=email)
    order=models.order.objects.filter(user=user)
    return render(request,'orderlist_user.html',{'orders':order})


def feedback(request):
    if 'email' not in request.session:
        return redirect('Login')

    email = request.session.get('email')
    user = models.Register.objects.get(email=email)

    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')

        models.feedback.objects.create(
            user=user,
            feedback=feedback_text
        )

        return redirect('home')

    return render(request, 'feedback.html')


def feedback_list(request):
    feedbacks = models.feedback.objects.all()
    return render(request,'feedback_list.html',{'feedbacks' : feedbacks})


def feedback_user(request):
    if 'email' not in request.session:
        return redirect('Login')

    email = request.session.get('email')
    user = models.Register.objects.get(email=email)

    feedbacks = models.feedback.objects.filter(user=user)

    return render(request, 'feedback_user.html', {'feedbacks': feedbacks})



def wishlist(request, id):
    if 'email' not in request.session:
        return redirect('login')

    email = request.session.get('email')
    user = models.Register.objects.get(email=email)

    product = models.dress.objects.get(id=id)

    models.wishlist.objects.get_or_create(
        user=user,
        product = product
    )

    return redirect('productlist_user')




def wishlist_user(request):
    if'email'not in request.session:
        return redirect('Login')
    email=request.session.get('email')
    user=models.Register.objects.get(email=email)
    wishlist=models.wishlist.objects.filter(user=user)
    return render(request,'wishlist_user.html',{'wishlist':wishlist})



def add_feedback(request, id):
    if 'email' not in request.session:
        return redirect('login')

    email = request.session.get('email')
    user = models.Register.objects.get(email=email)

    product = models.dress.objects.get(id=id)

    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        rating = request.POST.get('rating')

        models.feedback.objects.create(
            user=user,
            product=product,
            feedback=feedback,
            rating=rating

        )

        return render(request,'product_detail.html',{'product':product})

    return render(request, 'add_feedback.html', {'product': product})



def orderlist_owner(request):

    if 'email' not in request.session:
        return redirect('owner_login')

    email = request.session['email']

    owner = models.shopowner_register.objects.get(email=email)

    orders = models.order.objects.filter(
        products__user=owner
    ).order_by('-ordered_date')

    return render(request, 'orderlist_owner.html', {
        'user': owner,
        'orders': orders,
    })



def order_list(request):
    order = models.order.objects.all()
    return render(request,'order_list.html',{'order' : order})



def add_designer_owner(request):

    if 'email' not in request.session:
        return redirect('owner_home')

    owner_email = request.session.get('email')
    user = models.shopowner_register.objects.get(email=owner_email)

    if request.method == "POST":

        name = request.POST.get('name')
        age = request.POST.get('age')
        qualification = request.POST.get('qualification')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # -----------------------------
        # Name Validation
        # -----------------------------
        if not re.fullmatch(r"[A-Za-z ]+", name):
            return HttpResponse("<script>alert('Designer name should contain only letters.');window.history.back();</script>")

        # -----------------------------
        # Age Validation
        # -----------------------------
        if not age.isdigit():
            return HttpResponse("<script>alert('Age should contain only numbers.');window.history.back();</script>")

        age = int(age)

        if age < 18 or age > 60:
            return HttpResponse("<script>alert('Age must be between 18 and 60 years.');window.history.back();</script>")

        # -----------------------------
        # Qualification Validation
        # -----------------------------
        if not re.fullmatch(r"[A-Za-z .]+", qualification):
            return HttpResponse("<script>alert('Qualification should contain only letters.');window.history.back();</script>")

        # -----------------------------
        # Phone Validation
        # -----------------------------
        if not phone.isdigit():
            return HttpResponse("<script>alert('Phone number should contain only digits.');window.history.back();</script>")

        if len(phone) != 10:
            return HttpResponse("<script>alert('Phone number must be exactly 10 digits.');window.history.back();</script>")

        # -----------------------------
        # Email Validation
        # -----------------------------
        if models.designer.objects.filter(email=email).exists():
            return HttpResponse("<script>alert('Email already exists.');window.history.back();</script>")

        # -----------------------------
        # Password Validation
        # -----------------------------
        if len(password) < 8:
            return HttpResponse("<script>alert('Password must contain at least 8 characters.');window.history.back();</script>")

        models.designer.objects.create(

            user=user,
            name=name,
            age=age,
            qualification=qualification,
            gender=gender,
            phone=phone,
            email=email,
            password=password

        )

        return redirect('designer_login')

    return render(request, "add_designer_owner.html")



def designer_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user=models.designer.objects.get(email=email)
            if user.password == password:
                request.session ['email']=email
                return redirect('designer_home')
            else:
                return HttpResponse('Invalid Password')
        except models.designer.DoesNotExist:
            return HttpResponse('User Not Found')
    else:
        return render(request,'designer_login.html')



def designer_home(request):
    if 'email' not in request.session:
        return redirect('designer_login')
    else:
        return render(request,'designer_home.html')


def designer_list(request):

    if 'email' not in request.session:
        return redirect('owner_login')

    email = request.session['email']

    owner = models.shopowner_register.objects.get(email=email)

    designers = models.designer.objects.filter(user=owner)

    return render(request, 'designer_list.html', {
        'user': owner,
        'designers': designers,
    })



def designer_list_admin(request):
    designer = models.designer.objects.all()
    return render(request,'designer_list_admin.html',{'designer' : designer})



def designer_profile(request):
    if 'email' in request.session:
        email=request.session.get('email')
        user=models.designer.objects.get(email=email)
        return render(request,'designer_profile.html',{'user':user})
    return redirect('designer_login')



def designer_editprofile(request):

    if 'email' not in request.session:
        return redirect('designer_login')

    email = request.session.get('email')

    try:
        user = models.designer.objects.get(email=email)

        if request.method == "POST":

            name = request.POST.get('name')
            age = request.POST.get('age')
            gender = request.POST.get('gender')
            phone = request.POST.get('phone')
            qualification = request.POST.get('qualification')

            # Name Validation
            if not re.fullmatch(r"[A-Za-z ]+", name):
                return HttpResponse("<script>alert('Name should contain only letters.');window.history.back();</script>")

            # Age Validation
            if not age.isdigit():
                return HttpResponse("<script>alert('Age should contain only numbers.');window.history.back();</script>")

            age = int(age)

            if age < 18 or age > 60:
                return HttpResponse("<script>alert('Age must be between 18 and 60 years.');window.history.back();</script>")

            # Qualification Validation
            if not re.fullmatch(r"[A-Za-z .]+", qualification):
                return HttpResponse("<script>alert('Qualification should contain only letters.');window.history.back();</script>")

            # Phone Validation
            if not phone.isdigit():
                return HttpResponse("<script>alert('Phone number should contain only digits.');window.history.back();</script>")

            if len(phone) != 10:
                return HttpResponse("<script>alert('Phone number must be exactly 10 digits.');window.history.back();</script>")

            user.name = name
            user.age = age
            user.gender = gender
            user.phone = phone
            user.qualification = qualification

            user.save()

            return redirect('designer_profile')

        return render(request, 'designer_editprofile.html', {'user': user})

    except models.designer.DoesNotExist:
        return redirect('designer_login')




#user add custom
def addcustomization(request):
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = models.Register.objects.get(email=email)
        except models.Register.DoesNotExist:
            return redirect('Login')

        designers = models.designer.objects.all()

        if request.method == 'POST':
            employee_id = request.POST.get('employee')
            messege = request.POST.get('messege')

            if not employee_id or not messege:
                return HttpResponse("<script>alert('Please fill out all fields.'); window.history.back();</script>")

            try:
                employee = models.designer.objects.get(id=employee_id)
                models.Customization.objects.create(
                    user=user,
                    employee=employee,
                    messege=messege,
                )
                return HttpResponse(
                    "<script>alert('Customization request submitted successfully.');"
                    "window.location.href='/mycustomizationlist/';</script>"
                )
            except models.designer.DoesNotExist:
                return HttpResponse("<script>alert('Selected designer does not exist.'); window.history.back();</script>")

        return render(request, 'addcustomization.html', {
            'designers': designers,
            'user': user,
        })

    return redirect('Login')


def mycustomizationlist(request):
    if 'email' not in request.session:
        return redirect('Login')

    email = request.session.get('email')
    try:
        user = models.Register.objects.get(email=email)
    except models.Register.DoesNotExist:
        return redirect('Login')
        
    # FIX: Added filter(user=user) to fetch only this specific client's submissions
    customize = models.Customization.objects.filter(user=user).order_by('-created_at')

    return render(request, 'mycustomizationlist.html', {
        'user': user,
        'customize': customize,
    })


def customization_list_admin(request):
    customize = models.Customization.objects.all().order_by('-created_at')

    return render(
        request,
        'customization_list_admin.html',
        {'customize': customize}
    )




def customlist_owner(request):

    if 'email' not in request.session:
        return redirect('owner_login')

    email = request.session['email']

    owner = models.shopowner_register.objects.get(email=email)

    designers = models.designer.objects.filter(user=owner)

    custom = models.Customization.objects.filter(
        employee__in=designers
    ).order_by('-created_at')

    return render(request, 'customlist_owner.html', {
        'user': owner,
        'custom': custom,
    })


#designer side
def customlist_designer(request):

    if 'email' not in request.session:
        return redirect('designer_login')

    email = request.session['email']

    designer_obj = models.designer.objects.get(email=email)

    custom = models.Customization.objects.filter(
        employee=designer_obj
    ).order_by('-created_at')

    return render(request, 'customlist_designer.html', {
        'user': designer_obj,
        'custom': custom,
    })


def approve_customization_designer(request, id):
    if 'email' not in request.session:
        return redirect('designer_login')
    
    customization = models.Customization.objects.get(id=id)
    customization.approved_at = True
    customization.rejected_at = False
    customization.save()
    return HttpResponse("<script>alert('Customization Approved Successfully');window.location='/customlist_designer/';</script>")


def reject_customization_designer(request, id):
    if 'email' not in request.session:
        return redirect('designer_login')

    customization = models.Customization.objects.get(id=id)
    customization.rejected_at = True
    customization.approved_at = False
    customization.save()
    return HttpResponse("<script>alert('Customization Rejected Successfully');window.location='/customlist_designer/';</script>")