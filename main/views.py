from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from main.forms import CustomUserCreationForm, CustomAuthenticationForm

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('login')  # Redirect to the login page after successful registration
        else:
            messages.error(request, 'Please fill in your details correctly.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('portfolio')
            else:
                messages.error(request, 'Invalid login credentials.')
        else:
            messages.error(request, 'Invalid login details.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def portfolio(request):
    return render(request, 'portfolio.html')

def msc_practical(request):
    return render(request, 'practical.html')


from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image
import io
import zipfile

def imagetypeconverter(request):
    if request.method == 'POST':
        try:
            files = request.FILES.getlist('files')  # Get multiple files
            output_format = request.POST.get('format', 'JPEG')  # Get the selected format
            desired_size = int(request.POST.get('size', 0))  # Get the desired size
            size_unit = request.POST.get('size_unit', 'KB')  # Get the size unit

            if size_unit == 'MB':
                desired_size *= 1024  # Convert MB to KB

            if not files:
                raise ValueError("No files uploaded.")

            if len(files) == 1:
                # Process a single file and return it directly
                file = files[0]
                img = Image.open(file)

                # Convert the image to RGB mode if it has an alpha channel and the format doesn't support transparency
                if img.mode == 'RGBA' and output_format in ['JPEG', 'BMP']:
                    img = img.convert('RGB')

                # Adjust image quality to match the desired file size
                img_io = io.BytesIO()
                quality = 85  # Start with high quality
                while True:
                    img_io.seek(0)
                    img.save(img_io, format=output_format, quality=quality)
                    size_kb = img_io.tell() / 1024  # Get the size in KB
                    if size_kb <= desired_size or quality <= 10:
                        break
                    quality -= 5  # Reduce quality if the size is too large

                img_io.seek(0)
                response = HttpResponse(img_io, content_type=f'image/{output_format.lower()}')
                response['Content-Disposition'] = f'attachment; filename={file.name.rsplit(".", 1)[0]}.{output_format.lower()}'

                return response

            else:
                # Process multiple files and return them in a zip archive
                zip_buffer = io.BytesIO()  # Create a buffer to store the zip file

                with zipfile.ZipFile(zip_buffer, 'w') as zf:
                    for file in files:
                        img = Image.open(file)

                        # Convert the image to RGB mode if it has an alpha channel and the format doesn't support transparency
                        if img.mode == 'RGBA' and output_format in ['JPEG', 'BMP']:
                            img = img.convert('RGB')

                        # Adjust image quality to match the desired file size
                        img_io = io.BytesIO()
                        quality = 85  # Start with high quality
                        while True:
                            img_io.seek(0)
                            img.save(img_io, format=output_format, quality=quality)
                            size_kb = img_io.tell() / 1024  # Get the size in KB
                            if size_kb <= desired_size or quality <= 10:
                                break
                            quality -= 5  # Reduce quality if the size is too large

                        img_io.seek(0)

                        # Add the converted image to the zip file with the original file name
                        zf.writestr(f"{file.name.rsplit('.', 1)[0]}.{output_format.lower()}", img_io.getvalue())

                # Prepare the zip file for download
                zip_buffer.seek(0)
                response = HttpResponse(zip_buffer, content_type='application/zip')
                response['Content-Disposition'] = 'attachment; filename=converted_images.zip'

                return response

        except Exception as e:
            error_message = str(e)
            return render(request, 'imagetypeconverter.html', {'error_message': error_message})

    return render(request, 'imagetypeconverter.html')

