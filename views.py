from django.shortcuts import render , redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login , logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def index(request):
    notices = Notice.objects.all().order_by('-posting_date')
    return render(request, 'index.html', {'notices': notices})

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, pk=notice_id)
    return render(request, 'notice_detail.html', {'notice': notice})

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')  

    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            error = "Invalid credentials or not authorized."

    return render(request, 'admin_login.html', {'error': error})

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_students': Student.objects.count(),
        'total_subjects': Subject.objects.count(),
        'total_classes': Class.objects.count(),
        'total_results': Result.objects.values('student').distinct().count(),
    }
    return render(request, 'admin_dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def create_class(request):
    if request.method == 'POST':
        class_name = request.POST.get('classname')
        class_numeric = request.POST.get('classnamenumeric')
        section = request.POST.get('section')

        if class_name and class_numeric and section:
            Class.objects.create(
                class_name=class_name,
                class_numeric=class_numeric,
                section=section
            )
            messages.success(request, "Class Created Successfully")
            return redirect('create_class')
        else:
            messages.error(request, "Something went wrong. Please try again.")

    return render(request, 'create_class.html')


@login_required
@user_passes_test(is_admin)
def manage_classes(request):
    classes = Class.objects.all().order_by('-id')

    if request.GET.get('delete'):
        class_id = request.GET.get('delete')
        class_obj = get_object_or_404(Class, pk=class_id)
        class_obj.delete()
        messages.success(request, "Class deleted successfully.")
        return redirect('manage_classes')

    return render(request, 'manage_classes.html', {'classes': classes})

@login_required
@user_passes_test(is_admin)
def edit_class(request, class_id):
    class_obj = get_object_or_404(Class, pk=class_id)

    if request.method == 'POST':
        class_name = request.POST.get('classname')
        class_numeric = request.POST.get('classnamenumeric')
        section = request.POST.get('section')

        if class_name and class_numeric and section:
            class_obj.class_name = class_name
            class_obj.class_numeric = class_numeric
            class_obj.section = section
            class_obj.save()
            messages.success(request, "Class updated successfully.")
            return redirect('manage_classes')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'edit_class.html', {'class_obj': class_obj})


@login_required
@user_passes_test(is_admin)
def create_subject(request):
    if request.method == 'POST':
        subject_name = request.POST.get('subjectname')
        subject_code = request.POST.get('subjectcode')

        if subject_name and subject_code:
            Subject.objects.create(
                subject_name=subject_name,
                subject_code=subject_code
            )
            messages.success(request, "Subject created successfully.")
            return redirect('create_subject')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'create_subject.html')


@login_required
@user_passes_test(is_admin)
def manage_subjects(request):
    if 'id' in request.GET:
        subject_id = request.GET.get('id')
        subject = get_object_or_404(Subject, id=subject_id)
        subject.delete()
        messages.success(request, "Subject deleted successfully.")
        return redirect('manage_subjects')

    subjects = Subject.objects.all().order_by('-id')
    return render(request, 'manage_subjects.html', {'subjects': subjects})

@login_required
@user_passes_test(is_admin)
def edit_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == 'POST':
        subject.subject_name = request.POST.get('subjectname')
        subject.subject_code = request.POST.get('subjectcode')
        subject.save()
        messages.success(request, "Subject updated successfully.")
        return redirect('manage_subjects')

    return render(request, 'edit_subject.html', {'subject': subject})

@login_required
@user_passes_test(is_admin)
def add_subject_combination(request):
    classes = Class.objects.all()
    subjects = Subject.objects.all()

    if request.method == 'POST':
        class_id = request.POST.get('class')
        subject_id = request.POST.get('subject')

        if class_id and subject_id:
            SubjectCombination.objects.create(
                student_class_id=class_id,
                subject_id=subject_id,
                status=1
            )
            messages.success(request, "Subject combination added successfully.")
            return redirect('add_subject_combination')
        else:
            messages.error(request, "Both Class and Subject are required.")

    return render(request, 'add_subject_combination.html', {
        'classes': classes,
        'subjects': subjects,
    })



@login_required
@user_passes_test(is_admin)
def manage_subject_combination(request):
    # Activate Subject
    acid = request.GET.get('acid')
    if acid:
        SubjectCombination.objects.filter(id=acid).update(status=1)
        messages.success(request, "Subject activated successfully.")
        return redirect('manage_subject_combination')

    # Deactivate Subject
    did = request.GET.get('did')
    if did:
        SubjectCombination.objects.filter(id=did).update(status=0)
        messages.success(request, "Subject deactivated successfully.")
        return redirect('manage_subject_combination')

    combinations = SubjectCombination.objects.select_related('student_class', 'subject').all()

    return render(request, 'manage_subject_combination.html', {
        'combinations': combinations,
    })


@login_required
@user_passes_test(is_admin)
def add_student(request):
    classes = Class.objects.all()

    if request.method == 'POST':
        name = request.POST.get('fullanme')
        roll_id = request.POST.get('rollid')
        email = request.POST.get('emailid')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        class_id = request.POST.get('class')

        try:
            student_class = Class.objects.get(id=class_id)
            Student.objects.create(
                name=name,
                roll_id=roll_id,
                email=email,
                gender=gender,
                dob=dob,
                student_class=student_class
            )
            messages.success(request, 'Student info added successfully.')
        except Exception as e:
            messages.error(request, 'Something went wrong. Please try again.')

        return redirect('add_student')

    return render(request, 'add_student.html', {'classes': classes})


@login_required
@user_passes_test(is_admin)
def manage_students(request):
    students = Student.objects.select_related('student_class').all()
    return render(request, 'manage_students.html', {'students': students})


@login_required
@user_passes_test(is_admin)
def edit_student(request, stid):
    student = get_object_or_404(Student, id=stid)

    if request.method == 'POST':
        student.name = request.POST.get('fullanme')
        student.roll_id = request.POST.get('rollid')
        student.email = request.POST.get('emailid')
        student.gender = request.POST.get('gender')
        student.dob = request.POST.get('dob')
        student.status = int(request.POST.get('status'))
        student.save()
        msg = "Student info updated successfully"
        return render(request, 'edit_student.html', {'student': student, 'msg': msg})

    return render(request, 'edit_student.html', {'student': student})

from django.http import JsonResponse

@login_required
@user_passes_test(is_admin)
def delete_student(request, stid):
    student = get_object_or_404(Student, id=stid)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")

    return redirect('manage_students')

def add_result(request):
    classes = Class.objects.all()

    if request.method == 'POST' and 'submit_result' in request.POST:
        class_id = request.POST.get('class')
        student_id = request.POST.get('studentid')
        marks_data = {key.split('_')[1]: value for key, value in request.POST.items() if key.startswith('marks_')}

        if marks_data:
            for subject_id, mark in marks_data.items():
                Result.objects.create(
                    student_id=student_id,
                    student_class_id=class_id,
                    subject_id=subject_id,
                    marks=mark
                )
            messages.success(request, 'Result info added successfully')
            return redirect('add_result')
        else:
            messages.error(request, 'Something went wrong. Please try again')

    return render(request, 'add_result.html', {
        'classes': classes,
    })


def get_students_subjects(request):
    class_id = request.GET.get('class_id')
    if class_id:
        students = list(Student.objects.filter(student_class_id=class_id).values('id', 'name', 'roll_id'))
        subject_combinations = SubjectCombination.objects.filter(student_class_id=class_id,status=1).select_related('subject')
        subjects = [{'id': sc.subject.id, 'name': sc.subject.subject_name} for sc in subject_combinations]
        return JsonResponse({'students': students, 'subjects': subjects})
    return JsonResponse({'students': [], 'subjects': []})

def manage_result(request):
    results = Result.objects.select_related('student', 'student_class').order_by('-id')
    students = {}

    for res in results:
        stu_id = res.student.id
        if stu_id not in students:
            students[stu_id] = {
                'student': res.student,
                'class': res.student_class,
                'reg_date': res.student.reg_date,
                'status': res.student.status,
            }

    return render(request, 'manage_result.html', {
        'results': students.values()  
    })


def edit_result(request, stid):
    student = get_object_or_404(Student, id=stid)
    results = Result.objects.filter(student=student).select_related('subject')

    if request.method == 'POST':
        marks_list = request.POST.getlist('marks[]')
        ids = request.POST.getlist('id[]')
        
        for i in range(len(ids)):
            result_obj = get_object_or_404(Result, id=ids[i])
            result_obj.marks = marks_list[i]
            result_obj.save()

        messages.success(request, 'Result updated successfully')
        return redirect('manage_result')

    return render(request, 'edit_result.html', {
        'student': student,
        'results': results,
    })


def add_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        details = request.POST.get('details')

        Notice.objects.create(title=title, details=details)
        messages.success(request, 'Notice added successfully!')
        return redirect('manage_notice')

    return render(request, 'add_notice.html')

def manage_notice(request):
    notices = Notice.objects.all().order_by('-posting_date')
    return render(request, 'manage_notice.html', {'notices': notices})

def delete_notice(request, id):
    notice = get_object_or_404(Notice, id=id)
    notice.delete()
    messages.success(request, 'Notice deleted successfully.')
    return redirect('manage_notice')

def admin_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')  

from django.contrib.auth import update_session_auth_hash

@login_required
def change_admin_password(request):
    if request.method == 'POST':
        old = request.POST['old_password']
        new = request.POST['new_password']
        confirm = request.POST['confirm_password']

        if new != confirm:
            messages.error(request, 'New password and confirm password do not match.')
            return redirect('admin_change_password')

        user = authenticate(username=request.user.username, password=old)
        if user:
            user.set_password(new)
            user.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Password updated successfully.')
            return redirect('admin_change_password')
        else:
            messages.error(request, 'Old password is incorrect.')
            return redirect('admin_change_password')

    return render(request, 'admin_change_password.html')


def search_result(request):
    classes = Class.objects.all()
    return render(request, 'search_result.html', {'classes': classes})


def check_result(request):
    if request.method == 'POST':
        rollid = request.POST.get('rollid')
        class_id = request.POST.get('class_id')

        try:
            student = Student.objects.get(roll_id=rollid, student_class_id=class_id)
            results = Result.objects.filter(student=student)

            total_marks = sum([r.marks for r in results])
            subject_count = results.count()
            max_total = subject_count * 100  
            percentage = (total_marks / max_total) * 100 if max_total > 0 else 0

            context = {
                'student': student,
                'results': results,
                'total_marks': total_marks,
                'max_total': max_total,
                'percentage': round(percentage, 2)
            }
            return render(request, 'result_page.html', context)

        except Student.DoesNotExist:
            messages.error(request, "No result found for given Roll ID and Class.")
            return redirect('search_result')




