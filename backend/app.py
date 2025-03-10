from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from config import Config
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from datetime import datetime
import bcrypt

# Initialize Sentry
if os.environ.get('SENTRY_DSN'):
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )

# Initialize Flask app
app = Flask(__name__, 
    static_folder='../frontend',
    static_url_path=''
)
app.config.from_object(Config)
Config.init_app(app)

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(64))
    birth_date = db.Column(db.Date)
    gender = db.Column(db.String(20))
    bio = db.Column(db.Text)
    location = db.Column(db.String(120))
    profile_photo = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'gender': self.gender,
            'bio': self.bio,
            'location': self.location,
            'profile_photo': self.profile_photo,
            'created_at': self.created_at.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(120))
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviewed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    is_anonymous = db.Column(db.Boolean, default=False)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f'Page not found: {request.url}')
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.error(f'Server Error: {error}')
    return jsonify({'error': 'Internal server error'}), 500

# Routes
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Проверка обязательных полей
        required_fields = ['email', 'password', 'name']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing {field}'}), 400

        # Проверка существования пользователя
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        # Создание нового пользователя
        user = User(
            email=data['email'],
            name=data['name'],
            birth_date=datetime.strptime(data.get('birth_date'), '%Y-%m-%d').date() if data.get('birth_date') else None,
            gender=data.get('gender'),
            bio=data.get('bio'),
            location=data.get('location')
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        # Создание токена
        access_token = create_access_token(identity=user.id)
        
        app.logger.info(f'New user registered: {user.email}')
        return jsonify({
            'message': 'Registration successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        app.logger.error(f'Registration error: {str(e)}')
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Проверка обязательных полей
        if not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password are required'}), 400

        # Поиск пользователя
        user = User.query.filter_by(email=data['email']).first()
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Обновление времени последнего входа
        user.last_login = datetime.utcnow()
        db.session.commit()

        # Создание токена
        access_token = create_access_token(identity=user.id)
        
        app.logger.info(f'User logged in: {user.email}')
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        app.logger.error(f'Login error: {str(e)}')
        return jsonify({'error': str(e)}), 400

@app.route('/api/events', methods=['GET'])
def get_events():
    try:
        # TODO: Implement events listing
        app.logger.info('Events list requested')
        return jsonify({'message': 'Events endpoint'}), 200
    except Exception as e:
        app.logger.error(f'Events error: {str(e)}')
        return jsonify({'error': str(e)}), 400

@app.route('/api/reviews', methods=['GET', 'POST'])
def reviews():
    try:
        if request.method == 'POST':
            # TODO: Implement review creation
            app.logger.info('New review creation attempt')
            return jsonify({'message': 'Review created'}), 201
        # TODO: Implement reviews listing
        app.logger.info('Reviews list requested')
        return jsonify({'message': 'Reviews endpoint'}), 200
    except Exception as e:
        app.logger.error(f'Reviews error: {str(e)}')
        return jsonify({'error': str(e)}), 400

@app.route('/api/profile/<int:user_id>', methods=['GET', 'PUT'])
@jwt_required()
def profile(user_id):
    try:
        # Проверка прав доступа
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        user = User.query.get_or_404(user_id)

        if request.method == 'PUT':
            data = request.get_json()
            
            # Обновление полей профиля
            for field in ['name', 'birth_date', 'gender', 'bio', 'location']:
                if field in data:
                    if field == 'birth_date' and data[field]:
                        setattr(user, field, datetime.strptime(data[field], '%Y-%m-%d').date())
                    else:
                        setattr(user, field, data[field])

            db.session.commit()
            app.logger.info(f'Profile updated for user {user_id}')
            return jsonify({'message': 'Profile updated', 'user': user.to_dict()}), 200

        return jsonify(user.to_dict()), 200

    except Exception as e:
        app.logger.error(f'Profile error: {str(e)}')
        return jsonify({'error': str(e)}), 400

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected' if db.engine.execute('SELECT 1').scalar() else 'disconnected'
    })

if __name__ == '__main__':
    # Create database tables
    with app.app_context():
        db.create_all()
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=True)
