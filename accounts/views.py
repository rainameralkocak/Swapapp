import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render, get_object_or_404
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from swapapp import settings
from accounts.models import *


def main_page_view(request):
    main_categories = Category.objects.filter(parent_category__isnull=True)
    all_courses = Course.objects.order_by('?')[:5]
    if request.method == "GET":
        if request.user.is_authenticated:
            notifications = Notification.objects.filter(user=request.user).order_by('-timestamp')[:4]
            return render(request, 'main.html',
                          {'categories': main_categories, 'notifications': notifications, 'all_courses': all_courses})
        return render(request, 'main.html', {'categories': main_categories, 'all_courses': all_courses})
    elif request.method == "POST":
        pass

    return render(request, 'main.html', {'categories': main_categories, 'all_courses': all_courses})


def category_view(request, id):
    category = get_object_or_404(Category, id=id)
    all_courses = category.courses.all()
    subcategories = Category.objects.filter(parent_category=category)

    if request.user.is_authenticated :
        if not request.user.is_staff:
            student = StudentProfile.objects.get(user=request.user)
            purchases = [item.item_id for item in Purchase.objects.filter(student=student)]
            courses = []
            for course in all_courses:
                if course.id not in purchases:
                    courses.append(course)
            return render(request, 'category_details.html',
                          {'category': category, 'subcategories': subcategories, 'courses': courses})
        else:
            return render(request, 'category_details.html',
                          {'category': category, 'subcategories': subcategories, 'courses': all_courses})
    return render(request, 'category_details.html',
                  {'category': category, 'subcategories': subcategories, 'courses': all_courses})


def checkout_view(request, id):
    if not request.user.is_authenticated:
        return redirect("login")

    course = get_object_or_404(Course, id=id)
    if request.method == "GET":
        cards = CreditCard.objects.filter(user=request.user)
        return render(request, 'checkout_page.html', {'course': course, 'cards': cards})
    elif request.method == "POST":
        card_number = request.POST['card_number']
        card_owner = request.POST['card_owner']
        card_expiry = request.POST['card_expiry']
        card_cvc = request.POST['card_cvc']
        instructor_id = request.POST['instructor_id']

        checkbox_value = request.POST.get('save_card') == 'true'

        if card_number == "1111 2222 3333 4444":
            purchase = Purchase()
            purchase.item = course
            student_profile = get_object_or_404(StudentProfile, user=request.user)
            purchase.student = student_profile
            purchase.date = datetime.now()
            purchase.save()

            meeting = Meeting()
            datetime_format = "%Y-%m-%d %H:%M"
            meeting.purchase = purchase
            meeting.save()

            notification = Notification(user=course.instructor.user,
                                        message="Tebrikler.Yeni Bir Görüşme Talebiniz Var.Lütfen 24 Saat İçinde Görüşme Oluşturun.",
                                        meeting=meeting)
            notification.save()

            if checkbox_value:
                card = CreditCard()
                card.card_number = card_number
                card.owner_name = card_owner
                card.card_expiry = card_expiry
                card.card_cvc = card_cvc
                card.user = request.user
                card.card_name = "Kartım"
                card.card_icon_url = "../static/images/ziraatlogo.png"
                card.save()

            return render(request, 'success.html')
        else:
            messages.error(request, "Your credit card information is false. Please try again.")
            return redirect('checkout', id=id)


def my_courses(request):
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    purchases = Purchase.objects.filter(student=student_profile).select_related('item')[::-1]

    meetings = Meeting.objects.filter(purchase__in=purchases)

    purchase_meetings_map = {}

    control = (request.GET.get('target_meeting') == None)
    for meeting in meetings:
        purchase_id = meeting.purchase_id
        if purchase_id not in purchase_meetings_map:
            purchase_meetings_map[purchase_id] = []
        purchase_meetings_map[purchase_id].append(meeting)

    if control :
        return render(request, 'student_courses.html',
                      {"purchases": purchases, 'purchase_meetings_map': purchase_meetings_map})

    else :
        return render(request, 'student_courses.html',
                      {"purchases": purchases, 'purchase_meetings_map': purchase_meetings_map,
                       'target_meeting': request.GET.get('target_meeting')})


def add_new_course(request):
    instr_profile = get_object_or_404(InstructorProfile, user=request.user)
    courses = Course.objects.filter(instructor=instr_profile)
    categories = Category.objects.filter(parent_category__isnull=False)

    course_name = request.POST['courseName']
    course_details = request.POST['courseDetails']
    course_rating = request.POST['courseRating']
    course_price = request.POST['coursePrice']
    course_category_id = request.POST['courseCategory']

    # print(course_name, course_details, course_rating, course_category_id, course_price)

    if 'courseImage' in request.FILES:
        print("\ncourse image is in files\n")
        course_image = request.FILES['courseImage']
        # Assuming 'static/uploads' is the desired upload location
        upload_path = os.path.join('static', 'uploads', course_image.name)
        with open(upload_path, 'wb+') as destination:
            for chunk in course_image.chunks():
                destination.write(chunk)
        uploaded_file_url = upload_path  # Store the uploaded file path

        # Create the course object with the uploaded image path
        category = Category.objects.get(id=course_category_id)
        course = Course()
        course.name = course_name
        course.details = course_details
        course.rating = course_rating
        course.instructor = request.user.instructorprofile
        course.price = course_price
        course.image_path = "/static/uploads/" + course_image.name
        course.save()

        course.categories.add(category)
        course.categories.add(category.parent_category)
        course.save()

        return redirect('instructor_courses')

    return render(request, 'instructor_courses', {"courses": courses, "categories": categories})


def instructor_courses(request):
    instr_profile = get_object_or_404(InstructorProfile, user=request.user)
    courses = Course.objects.filter(instructor=instr_profile)
    categories = Category.objects.filter(parent_category__isnull=False)
    control = (request.GET.get('target_meeting') == None)

    if request.method == 'GET':
        # Get purchases related to the instructor's courses
        purchases_from_instructor = Purchase.objects.filter(item_id__in=courses.values_list('id', flat=True))

        # Get meetings related to these purchases
        meetings = Meeting.objects.filter(purchase__in=purchases_from_instructor)[::-1]

        # Add student names and course names to each meeting object
        meetings_with_students = []
        for meeting in meetings:
            purchase = meeting.purchase
            student_name = purchase.student.user.username
            course_name = purchase.item.name
            meeting_data = {
                'meeting': meeting,
                'student': student_name,
                'course': course_name,
            }
            meetings_with_students.append(meeting_data)

        if control:
            context = {
                'courses': courses,
                'categories': categories,
                'meetings_with_students': meetings_with_students
            }

        else :
            context = {
                'courses': courses,
                'categories': categories,
                'meetings_with_students': meetings_with_students,
                'target_meeting':request.GET.get('target_meeting')
            }
            print(context)


        return render(request, 'instructor_courses.html', context)




def set_meeting_url(request):
    if request.method == 'POST':
        meeting_id = request.POST.get('meeting_id')
        meeting_url = request.POST.get('meeting_url')
        meeting_date = request.POST.get('meeting_date_time')

        try:
            meeting = Meeting.objects.get(id=meeting_id)
            meeting.url = meeting_url  # Assuming the Meeting model has a field named 'url'
            meeting.status = "WaitingForStudent"
            meeting.date = meeting_date
            meeting.save()

            notification = Notification(user=meeting.purchase.student.user,
                                        message="Eğitimi satın aldığınız öğretmeniniz, eğitiminiz için bir toplantı tarihi ve linki gönderdi!",
                                        meeting=meeting)
            notification.save()


        except Meeting.DoesNotExist:
            pass

    return redirect('instructor_courses')

def set_video_url(request):
    if request.method == 'POST':

        meeting_id = request.POST.get('meeting_id_video')
        video_url = request.POST.get('meeting_video_url')
        meeting = get_object_or_404(Meeting, id=meeting_id)

        # Update the video_url field
        meeting.video_url = video_url
        meeting.save()

        notification = Notification(user=meeting.purchase.student.user,
                                    message="Eğitimi satın aldığınız öğretmeniniz, eğitiminiz için bir ders kaydı ekledi!",
                                    meeting=meeting)
        notification.save()

        return redirect('instructor_courses')


def subcategory_view(request, id):
    subcategory = get_object_or_404(Category, id=id)
    all_courses = subcategory.courses.all()

    if request.user.is_authenticated:
        if request.user.is_staff:
            return render(request, 'subcategory_details.html', {'category': subcategory, 'courses': all_courses})
        else:
            student = StudentProfile.objects.get(user=request.user)
            purchases = [item.item_id for item in Purchase.objects.filter(student=student)]

            courses = []
            for course in all_courses:
                if course.id not in purchases:
                    courses.append(course)
            return render(request, 'subcategory_details.html', {'category': subcategory, 'courses': courses})
    return render(request, 'subcategory_details.html', {'category': subcategory, 'courses': all_courses})



def profile_view(request):
    if request.method == 'GET':
        obj, created = UserDetails.objects.get_or_create(user=request.user)
        if created:
            obj.user = request.user
            obj.address = "adres giriniz."
            obj.city = "..."
            obj.country = "..."
            obj.phone = "..."

        return render(request, 'partials/profile.html', {'details': obj})

    elif request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        city = request.POST.get('city')

        detail = get_object_or_404(UserDetails, user=request.user)
        detail.user = request.user
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        detail.address = address
        detail.phone = phone
        detail.country = country
        detail.city = city

        request.user.save()
        detail.save()

        return redirect('main_page')


def authenticated_view(request):
    return render(request, 'authenticated.html')


def unatuhenticated_view(request):
    return render(request, 'unauthenticated.html')


def calender_view(request):
    return render(request, 'calender/calender.html')


def elektrik_view(request):
    return render(request, "categories/elektrik-elektronikcategory.html")


def kişisel_view(request):
    return render(request, "categories/kişiselgelişimcategory.html")


def office_view(request):
    return render(request, "categories/officecategory.html")


def olasılık_view(request):
    return render(request, "categories/olasılıkcategory.html")


def tasarım_view(request):
    return render(request, "categories/tasarımcategory.html")


def yazılım_view(request):
    return render(request, "categories/yazılımcategory.html")


def odeme_view(request):
    return render(request, "partials/odeme.html")


def policy_view(request):
    return render(request, 'policy/policy.html')


def register_instructor_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST['email']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "registration/register.html", {
                    "error": "Username is already taken",
                    "username": username,
                    "email": email
                })
            elif User.objects.filter(email=email).exists():
                return render(request, "registration/register.html", {
                    "error": "Email is already taken",
                    "username": username,
                    "email": email
                })
            elif not email.endswith('@edu.tr'):  # emaili edu olanlar girmesin
                return render(request, 'registration/register_instructor.html', {
                    'error': 'Sadece edu.tr uzantılı e-posta adresleri kabul edilmektedir.',
                    'username': username,
                    'email': email
                })
            else:
                user = User.objects.create_user(username=username, email=email, password=password, is_staff=True)
                user.is_active = False  # Kullanıcıyı hemen aktif hale getirmiyoruz
                user.save()

                instructor = InstructorProfile(user=user, bio="deneme")
                instructor.save()

                # E-posta gönderimi
                current_site = get_current_site(request)
                from_email = settings.EMAIL_HOST_USER
                to_list = (user.email)
                subject = 'Activate Your Account'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(subject, message, from_email, [user.email])

                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return render(request, "registration/register.html", {
                "error": "Passwords do not match",
                "username": username,
                "email": email
            })
    return render(request, "registration/register_instructor.html")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Hesabınız başarıyla aktif edilmiştir. Giriş yapabilirsiniz.')
        return redirect('main_page')
    else:
        return HttpResponse('Aktivasyon linki geçersiz!')


def signout(request):
    logout(request)
    return redirect('main_page')


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST['email']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "registration/register.html", {
                    "error": "Username is already taken",
                    "username": username,
                    "email": email
                })
            elif User.objects.filter(email=email).exists():
                return render(request, "registration/register.html", {
                    "error": "Email is already taken",
                    "username": username,
                    "email": email
                })
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False  # Kullanıcıyı hemen aktif hale getirmiyoruz
                user.save()

                student = StudentProfile(user=user, enrollment_date=datetime.now())
                student.save()

                # E-posta gönderimi
                current_site = get_current_site(request)
                from_email = settings.EMAIL_HOST_USER  # nerden mail atacaksam ordan çektim
                to_list = (user.email)  # kullanıcının maili
                subject = 'Activate Your Account'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(subject, message, from_email, [user.email])

                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return render(request, "registration/register.html", {
                "error": "Passwords do not match",
                "username": username,
                "email": email
            })
    return render(request, "registration/register.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Kullanıcıyı doğrula
        user = authenticate(request, username=username, password=password)

        if user.is_staff:
            instructor = user.instructorprofile
            print(str(instructor.id) + " " + user.username)

        request.session["logged_in"] = True

        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return render(request, "registration/login.html", {
                "error": "Username ya da parola yanlış"
            })

    return render(request, 'registration/login.html')


def mobiluygulama_view(request):
    return render(request, 'lessons/Yazılım Courses/mobiluygulama.html')


def nesneyonelimliprg_view(request):
    return render(request, 'lessons/Yazılım Courses/nesneyonelimliprg.html')


def temelalgoritma_view(request):
    return render(request, 'lessons/Yazılım Courses/temelalgoritma.html')


def webgelistirme_view(request):
    return render(request, 'lessons/Yazılım Courses/webgelistirme.html')


def yazilimtest_view(request):
    return render(request, 'lessons/Yazılım Courses/yazilimtest.html')


def elektrikproje_view(request):
    return render(request, 'lessons/Elektrik - Elektronik Courses/elektrikproje.html')


def temelelektrik_view(request):
    return render(request, 'lessons/Elektrik - Elektronik Courses/temelelektrik.html')


def excell_view(request):
    return render(request, 'lessons/Microsoft365 Courses/excell.html')


def onenote_view(request):
    return render(request, 'lessons/Microsoft365 Courses/onenote.html')


def outlook_view(request):
    return render(request, 'lessons/Microsoft365 Courses/outlook.html')


def powerpoint_view(request):
    return render(request, 'lessons/Microsoft365 Courses/powerpoint.html')


def sharepoint_view(request):
    return render(request, 'lessons/Microsoft365 Courses/sharepoint.html')


def word_view(request):
    return render(request, 'lessons/Microsoft365 Courses/word.html')


def iletisimbecerileri_view(request):
    return render(request, 'lessons/Kişisel Gelişim Courses/iletisimbecerileri.html')


def motivasyon_view(request):
    return render(request, 'lessons/Kişisel Gelişim Courses/motivasyon.html')


def ozguven_view(request):
    return render(request, 'lessons/Kişisel Gelişim Courses/ozguven.html')


def zamanyonetimi_view(request):
    return render(request, 'lessons/Kişisel Gelişim Courses/zamanyonetimi.html')


def ictasarim_view(request):
    return render(request, 'lessons/Tasarım Courses/ictasarim.html')


def mimarlik_view(request):
    return render(request, 'lessons/Tasarım Courses/mimarlik.html')


def modatasarim_view(request):
    return render(request, 'lessons/Tasarım Courses/modatasarim.html')


def oyuntasarim_view(request):
    return render(request, 'lessons/Tasarım Courses/oyuntasarim.html')


def olasilikveistatistik_view(request):
    return render(request, 'lessons/Olasılık Courses/olasilikveistatistik.html')


def calender_view(request):
    return render(request, 'calender/calender.html')
