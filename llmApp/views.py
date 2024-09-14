import os
# pdf_chatbot_app/views.py
from django.shortcuts import render
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_openai import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
# from langchain.llms import OpenAI
from langchain_community.llms import OpenAI
# from langchain.callbacks import get_openai_callback
from langchain_community.callbacks import get_openai_callback
from .forms import RegistrationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import ChatMessage, PDFDocument
# from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI
from django.contrib.auth.decorators import login_required
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from django.http import HttpResponse, JsonResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from dotenv import load_dotenv


# os.getenv('OPENAI_API_KEY')
#os.environ["OPENAI_API_KEY"] = ""

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Create your views here.
@login_required(login_url="/login/")
def home(request):
    """
    Renders the home page.

    :param request: HTTP request.
    :return: Rendered home page with PDF documents.
    """
    pdf_documents = PDFDocument.objects.filter(user=request.user)
    return render(request, 'home.html', {'pdf_documents': pdf_documents})



def register(request):
    """
    Handles user registration.

    :param request: HTTP request.
    :return: Rendered registration page or redirects to registration page.
    """
    if request.method == 'POST':
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, "username already Taken")
            return redirect("/register/")
        
        user_email = User.objects.filter(email = email)
        
        if user_email.exists():
            messages.info(request, "email already Taken")
            return redirect("/register/")
        
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        
        user.set_password(password)
        user.save()
        
        messages.info(request, "Account created successfully")
        
        return redirect("/register/")
    return render(request, 'register.html')




def user_login(request):
    """
    Handles user login.

    :param request: HTTP request.
    :return: Redirects to the home page or shows an error message.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other desired page
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'login.html')

def user_logout(request):
    """
    Handles user logout.

    :param request: HTTP request.
    :return: Redirects to the login page.
    """
    logout(request)
    return redirect('login')

