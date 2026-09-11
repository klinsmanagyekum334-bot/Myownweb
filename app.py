from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from functools import wraps
import firebase_admin
from firebase_admin import credentials, firestore
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ophyser-platform-secret-key')
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Session configuration
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# ===== FIREBASE INITIALIZATION =====
def get_firebase_credentials():
    """Get Firebase credentials from environment or file"""
    cred_json = os.environ.get('FIREBASE_CREDENTIALS')
    if cred_json:
        try:
            return json.loads(cred_json)
        except json.JSONDecodeError as e:
            print(f"⚠️ Invalid JSON in FIREBASE_CREDENTIALS: {e}")
    
    cred_path = os.path.join(os.path.dirname(__file__), 'firebase-credentials.json')
    if os.path.exists(cred_path):
        try:
            with open(cred_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️ Invalid JSON in firebase-credentials.json: {e}")
    
    return None

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        cred_dict = get_firebase_credentials()
        if cred_dict:
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase initialized successfully!")
            return firestore.client()
        else:
            print("⚠️ No Firebase credentials found. Using mock database.")
            return None
    except Exception as e:
        print(f"⚠️ Firebase error: {e}. Using mock database.")
        return None

db = initialize_firebase()

# ===== DATABASE FUNCTIONS =====

def get_site_settings():
    """Fetch site settings from Firestore"""
    if db is None:
        return None
    
    try:
        doc_ref = db.collection('settings').document('site_settings')
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        
        default_settings = {
            'site_title': 'Ophyser Platform',
            'page_title': 'Home',
            'hero_title': 'OPHYSER PLATFORM',
            'hero_subtitle': '2026 / 2027 FEATURES OPEN',
            'hero_text_under': '',
            'hero_image': None,
            'profile_image': None,
            'main_content': 'This is the main content of the website.',
            'about_text': 'This is the official website of Ophyser where your dreams comes true of being featured on a website without you owning your own website. Take control like your boss with your name and all information displayed like your personal website just click on the link to place your request.',
            'contact_phone': '0240044138',
            'contact_email': 'klinsmanagyekum334@gmail.com',
            'appointment_title': 'FEATURED PROFILE',
            'advert_title': 'Business Advert',
            'advert_description': 'Promote your business here',
            'advert_price': 'Price: Contact for details',
            'advert_contact': 'Phone: 0240044138',
            'advert_image': None,
        }
        doc_ref.set(default_settings)
        return default_settings
    except Exception as e:
        print(f"Error fetching settings: {e}")
        return None

def update_site_settings(data):
    """Update site settings in Firestore"""
    if db is None:
        return False
    
    try:
        doc_ref = db.collection('settings').document('site_settings')
        doc_ref.set(data, merge=True)
        return True
    except Exception as e:
        print(f"Error updating settings: {e}")
        return False

def get_profile_cards():
    """Fetch all profile cards from Firestore"""
    if db is None:
        return []
    
    try:
        cards_ref = db.collection('profile_cards').order_by('sort_order')
        docs = cards_ref.stream()
        cards = []
        for doc in docs:
            card = doc.to_dict()
            card['id'] = doc.id
            cards.append(card)
        return cards
    except Exception as e:
        print(f"Error fetching cards: {e}")
        return []

def add_profile_card(image, text):
    """Add a new profile card to Firestore"""
    if db is None:
        return None
    
    try:
        cards = get_profile_cards()
        sort_order = len(cards)
        
        data = {
            'image': image,
            'text': text,
            'sort_order': sort_order,
            'created_at': datetime.now().isoformat()
        }
        doc_ref = db.collection('profile_cards').add(data)
        return doc_ref
    except Exception as e:
        print(f"Error adding card: {e}")
        return None

def update_profile_card(card_id, image=None, text=None):
    """Update a profile card in Firestore"""
    if db is None:
        return False
    
    try:
        data = {}
        if image is not None:
            data['image'] = image
        if text is not None:
            data['text'] = text
        
        if not data:
            return False
        
        doc_ref = db.collection('profile_cards').document(card_id)
        doc_ref.update(data)
        return True
    except Exception as e:
        print(f"Error updating card: {e}")
        return False

def delete_profile_card(card_id):
    """Delete a profile card from Firestore"""
    if db is None:
        return False
    
    try:
        doc_ref = db.collection('profile_cards').document(card_id)
        doc_ref.delete()
        return True
    except Exception as e:
        print(f"Error deleting card: {e}")
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ===== ADMIN AUTHENTICATION DECORATOR =====
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login to access the admin panel.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ===== CONTEXT PROCESSOR =====
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

# ===== ROUTES =====

@app.route('/')
def index():
    settings = get_site_settings() or {}
    cards = get_profile_cards()
    
    return render_template('index.html',
                         site_title=settings.get('site_title', 'Ophyser Platform'),
                         page_title=settings.get('page_title', 'Home'),
                         hero_title=settings.get('hero_title', 'OPHYSER PLATFORM'),
                         hero_subtitle=settings.get('hero_subtitle', '2026 / 2027 FEATURES OPEN'),
                         hero_text_under=settings.get('hero_text_under', ''),
                         hero_image=settings.get('hero_image'),
                         profile_image=settings.get('profile_image'),
                         main_content=settings.get('main_content', ''),
                         about_text=settings.get('about_text', ''),
                         contact_phone=settings.get('contact_phone', '0240044138'),
                         contact_email=settings.get('contact_email', 'klinsmanagyekum334@gmail.com'),
                         appointment_title=settings.get('appointment_title', 'FEATURED PROFILE'),
                         advert_title=settings.get('advert_title', 'Business Advert'),
                         advert_description=settings.get('advert_description', ''),
                         advert_price=settings.get('advert_price', 'Price: Contact for details'),
                         advert_contact=settings.get('advert_contact', 'Phone: 0240044138'),
                         advert_image=settings.get('advert_image'),
                         profile_cards=cards)

# ===== ADMIN ROUTES =====

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
        ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Klinsman@ophyser1')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            session.permanent = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password!', 'error')
    
    settings = get_site_settings() or {}
    return render_template('admin/login.html', site_title=settings.get('site_title', 'Ophyser Platform'))

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    settings = get_site_settings() or {}
    cards = get_profile_cards()
    
    return render_template('admin/dashboard.html',
                         site_title=settings.get('site_title', 'Ophyser Platform'),
                         data=settings,
                         profile_cards=cards)

@app.route('/admin/update', methods=['POST'])
@admin_required
def admin_update():
    text_keys = ['site_title', 'page_title', 'hero_title', 'hero_subtitle',
                 'hero_text_under', 'main_content', 'about_text', 'contact_phone',
                 'contact_email', 'appointment_title', 'advert_title',
                 'advert_description', 'advert_price', 'advert_contact']
    
    update_data = {}
    for key in text_keys:
        if key in request.form:
            update_data[key] = request.form.get(key)
    
    # Handle hero image upload
    if 'hero_image' in request.files:
        file = request.files['hero_image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            update_data['hero_image'] = filename
            flash('Hero image uploaded successfully!', 'success')
    
    # Handle profile image upload
    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            update_data['profile_image'] = filename
            flash('Profile image uploaded successfully!', 'success')
    
    # Handle advert image upload
    if 'advert_image' in request.files:
        file = request.files['advert_image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            update_data['advert_image'] = filename
            flash('Advert image uploaded successfully!', 'success')
    
    if update_data:
        if update_site_settings(update_data):
            flash('Content updated successfully!', 'success')
        else:
            flash('Error updating content. Please try again.', 'error')
    
    return redirect(url_for('admin_dashboard'))

# ===== PROFILE CARDS MANAGEMENT =====

@app.route('/admin/cards/add', methods=['GET', 'POST'])
@admin_required
def add_card():
    if request.method == 'POST':
        text = request.form.get('card_text', '')
        image_filename = None
        
        if 'card_image' in request.files:
            file = request.files['card_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_filename = filename
        
        result = add_profile_card(image_filename, text)
        if result:
            flash('Card added successfully!', 'success')
        else:
            flash('Error adding card. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    settings = get_site_settings() or {}
    return render_template('admin/add_card.html', site_title=settings.get('site_title', 'Ophyser Platform'))

@app.route('/admin/cards/edit/<card_id>', methods=['GET', 'POST'])
@admin_required
def edit_card(card_id):
    cards = get_profile_cards()
    card = next((c for c in cards if c.get('id') == card_id), None)
    
    if not card:
        flash('Card not found!', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        text = request.form.get('card_text', '')
        image_filename = card.get('image')
        
        if 'card_image' in request.files:
            file = request.files['card_image']
            if file and file.filename and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                image_filename = filename
        
        if update_profile_card(card_id, image_filename, text):
            flash('Card updated successfully!', 'success')
        else:
            flash('Error updating card. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    settings = get_site_settings() or {}
    return render_template('admin/edit_card.html',
                         site_title=settings.get('site_title', 'Ophyser Platform'),
                         card=card,
                         card_id=card_id)

@app.route('/admin/cards/delete/<card_id>')
@admin_required
def delete_card(card_id):
    if delete_profile_card(card_id):
        flash('Card deleted successfully!', 'success')
    else:
        flash('Error deleting card. Please try again.', 'error')
    return redirect(url_for('admin_dashboard'))

# ===== RUN APP =====
if __name__ == '__main__':
    app.run(
        debug=False,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )
