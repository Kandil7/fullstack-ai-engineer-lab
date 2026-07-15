# =============================================================================
# Django Forms - Reference Guide
# =============================================================================
# Django forms handle HTML form rendering, validation, and data processing.
# They save you from writing repetitive HTML and validation code.
#
# W3chools Django Tutorial: https://www.w3schools.com/django/django_forms.php
# =============================================================================

# ---------------------------------------------------------------------------
# 1. What are Django Forms?
# ---------------------------------------------------------------------------
# Django forms are Python classes that:
# 1. Render HTML form elements
# 2. Validate user input
# 3. Display error messages
# 4. Convert data to Python types
#
# Two types:
#   - django.forms.Form       → Plain forms (manual field definition)
#   - django.forms.ModelForm  → Forms tied to a model (auto-generates fields)

# ---------------------------------------------------------------------------
# 2. Creating a Form
# ---------------------------------------------------------------------------

from django import forms


# --- Regular Form ---
class ContactForm(forms.Form):
    """A simple contact form (not tied to a model)."""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        }),
        help_text='Enter your full name.',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your@email.com'
        })
    )
    subject = forms.CharField(max_length=200)
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'class': 'form-control'
        })
    )
    subscribe = forms.BooleanField(
        required=False,
        initial=True,
        label='Subscribe to newsletter'
    )

# --- ModelForm ---
class PostForm(forms.ModelForm):
    """A form automatically generated from the Post model."""

    class Meta:
        model = Post  # Replace with your actual Post model
        fields = ['title', 'content', 'category', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Post title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 10
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'title': 'Post Title',
            'content': 'Post Content',
        }
        help_texts = {
            'title': 'Choose a descriptive title.',
        }

    # Custom validation
    def clean_title(self):
        """Validate title field."""
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters.")
        return title

    def clean(self):
        """Validate the entire form."""
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        content = cleaned_data.get('content')

        if title and content and title.lower() in content.lower():
            raise forms.ValidationError(
                "Content should not contain the title."
            )
        return cleaned_data

# ---------------------------------------------------------------------------
# 3. Form Fields
# ---------------------------------------------------------------------------
# Django provides many field types:

# Text fields:
# forms.CharField(max_length=100)         # Single line text
# forms.CharField(widget=forms.Textarea)  # Multi-line text
# forms.EmailField()                      # Email validation
# forms.URLField()                        # URL validation
# forms.SlugField()                       # Slug (letters, numbers, -)
# forms.UUIDField()                       # UUID input
# forms.IPAddressField()                  # IP address

# Number fields:
# forms.IntegerField(min_value=0, max_value=100)
# forms.FloatField()
# forms.DecimalField(max_digits=10, decimal_places=2)

# Date/Time fields:
# forms.DateField()                       # Date picker
# forms.TimeField()                       # Time picker
# forms.DateTimeField()                   # Date + time picker

# Boolean:
# forms.BooleanField()                    # Checkbox
# forms.NullBooleanField()                # None/True/False

# Choice fields:
# forms.ChoiceField(choices=[('a', 'Option A'), ('b', 'Option B')])
# forms.MultipleChoiceField(choices=[...])  # Multiple selection

# File fields:
# forms.FileField()                       # Any file
# forms.ImageField()                      # Image only (with validation)

# Other:
# forms.RegexField(regex=r'^\d{3}$')      # Custom regex
# forms.TypedChoiceField(choices=[...], coerce=int)  # Coerce type
# forms.JSONField()                       # JSON input (Django 4.0+)

# ---------------------------------------------------------------------------
# 4. Widgets
# ---------------------------------------------------------------------------
# Widgets control how fields are rendered in HTML.

# Common widgets:
# forms.TextInput()                        # <input type="text">
# forms.PasswordInput()                    # <input type="password">
# forms.EmailInput()                       # <input type="email">
# forms.URLInput()                         # <input type="url">
# forms.NumberInput()                      # <input type="number">
# forms.DateInput(attrs={'type': 'date'}) # Date picker
# forms.TimeInput(attrs={'type': 'time'}) # Time picker
# forms.DateTimeInput()                    # Date + time
# forms.Textarea()                         # <textarea>
# forms.Select()                           # <select> dropdown
# forms.SelectMultiple()                   # <select multiple>
# forms.RadioSelect()                      # Radio buttons
# forms.CheckboxSelectMultiple()           # Checkboxes
# forms.FileInput()                        # <input type="file">
# forms.HiddenInput()                      # <input type="hidden">
# forms.ClearableFileInput()               # File input with clear

# Custom widget with attrs:
# forms.TextInput(attrs={
#     'class': 'form-control',           # CSS class
#     'id': 'post-title',                # HTML id
#     'placeholder': 'Enter title',      # Placeholder text
#     'autofocus': True,                 # Auto-focus
#     'required': True,                  # HTML5 required
# })

# ---------------------------------------------------------------------------
# 5. Form Validation
# ---------------------------------------------------------------------------
# Django forms have built-in and custom validation.

class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField(min_value=13, max_value=120, required=False)

    # Field-level validation (clean_<fieldname>)
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already taken.")
        # You could also check for reserved words, profanity, etc.
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered.")
        return email

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age is not None and age < 18:
            raise forms.ValidationError("Must be 18 or older.")
        return age

    # Form-level validation (clean)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

# Validation flow:
# 1. to_python()     → Convert to Python type
# 2. validate()      → Field-level validation
# 3. clean_<field>() → Field-level custom validation
# 4. clean()         → Form-level custom validation
# 5. is_valid()      → Triggers all above, returns True/False

# ---------------------------------------------------------------------------
# 6. Using Forms in Views
# ---------------------------------------------------------------------------

from django.shortcuts import render, redirect


def contact_view(request):
    """Handle contact form display and submission."""

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Access cleaned data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Process the form (send email, save to DB, etc.)
            # send_mail(subject, message, email, ['admin@example.com'])

            return redirect('contact_success')
    else:
        # GET request - show empty form
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


def post_create_view(request):
    """Create a new blog post using ModelForm."""

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Include FILES for uploads
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to DB yet
            post.author = request.user       # Set additional fields
            post.save()                      # Now save
            form.save_m2m()                  # Save many-to-many relationships
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_form.html', {'form': form})


def post_edit_view(request, pk):
    """Edit an existing blog post."""
    # post = Post.objects.get(pk=pk)
    # form = PostForm(instance=post, data=request.POST or None)

    # if request.method == 'POST' and form.is_valid():
    #     form.save()
    #     return redirect('post_detail', pk=pk)

    # return render(request, 'blog/post_form.html', {'form': form})
    pass

# ---------------------------------------------------------------------------
# 7. Rendering Forms in Templates
# ---------------------------------------------------------------------------

# --- Manual rendering (each field) ---
# <form method="post">
#     {% csrf_token %}
#     {{ form.as_p }}        {# Render all fields wrapped in <p> tags #}
#     {{ form.as_table }}    {# Render all fields as table rows #}
#     {{ form.as_ul }}       {# Render all fields as list items #}
#     <button type="submit">Submit</button>
# </form>

# --- Custom rendering (each field individually) ---
# <form method="post">
#     {% csrf_token %}
#
#     <div class="form-group">
#         <label for="{{ form.title.id_for_label }}">Title:</label>
#         {{ form.title }}
#         {% if form.title.errors %}
#             <div class="error">{{ form.title.errors }}</div>
#         {% endif %}
#         {% if form.title.help_text %}
#             <small class="help">{{ form.title.help_text }}</small>
#         {% endif %}
#     </div>
#
#     <div class="form-group">
#         <label for="{{ form.content.id_for_label }}">Content:</label>
#         {{ form.content }}
#         {{ form.content.errors }}
#     </div>
#
#     {{ form.non_field_errors }}  {# Form-level errors #}
#
#     <button type="submit">Submit</button>
# </form>

# ---------------------------------------------------------------------------
# 8. Form Styles with Bootstrap
# ---------------------------------------------------------------------------
# Add Bootstrap classes to form fields for styling:

class BootstrapPostForm(forms.ModelForm):
    class Meta:
        model = Post  # Your Post model
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your content...'
            }),
        }

# Or use django-crispy-forms for automatic styling:
# pip install django-crispy-forms crispy-bootstrap5
#
# INSTALLED_APPS = [..., 'crispy_forms', 'crispy_bootstrap5']
# CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
# CRISPY_TEMPLATE_PACK = "bootstrap5"
#
# In templates: {% load crispy_forms_tags %}
#   {{ form|crispy }}

# ---------------------------------------------------------------------------
# 9. Formset (Multiple Forms)
# ---------------------------------------------------------------------------
# Formsets handle multiple forms on one page (e.g., inline editing).

# from django.forms import formset_factory
#
# ItemFormSet = formset_factory(ItemForm, extra=3)  # 3 empty forms
#
# def manage_items(request):
#     if request.method == 'POST':
#         formset = ItemFormSet(request.POST)
#         if formset.is_valid():
#             for form in formset:
#                 if form.cleaned_data:  # Skip empty forms
#                     form.save()
#             return redirect('items_list')
#     else:
#         formset = ItemFormSet()
#
#     return render(request, 'items.html', {'formset': formset})

# ModelFormset:
# from django.forms import modelformset_factory
# ItemFormSet = modelformset_factory(Item, form=ItemForm, extra=2)

# ---------------------------------------------------------------------------
# 10. Form Best Practices
# ---------------------------------------------------------------------------
# 1. Use ModelForm when the form maps directly to a model
# 2. Use Form for complex forms not tied to a model
# 3. Always use {% csrf_token %} in forms
# 4. Validate on both client AND server side
# 5. Use clean_<fieldname>() for field-level validation
# 6. Use clean() for form-level validation
# 7. Access cleaned_data (not raw POST data) after validation
# 8. Use commit=False to modify objects before saving
# 9. Use formsets for editing related objects inline
# 10. Add CSS classes via widgets for Bootstrap/Tailwind styling
