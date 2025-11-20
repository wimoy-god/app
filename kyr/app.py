from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "db.sqlite3")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Masterclass(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    instructor = db.Column(db.String(120), nullable=True)
    date = db.Column(db.DateTime, nullable=True)
    seats = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Masterclass {self.title}>"

# Ensure database tables exist at startup (avoid relying on removed/changed decorators)
with app.app_context():
    db.create_all()
    # Seed sample data if DB is empty (useful for first run / demo)
    if Masterclass.query.count() == 0:
        sample = [
            Masterclass(title="Основы керамики", description="Введение в работу с глиной", instructor="Анна Петрова", date=datetime(2025,12,5,18,0), seats=20),
            Masterclass(title="Фотография для начинающих", description="Композиция и свет", instructor="Иван Иванов", date=datetime(2025,11,30,14,0), seats=12),
            Masterclass(title="Рисунок акварелью", description="Техники и практика", instructor="Мария С.", date=None, seats=10),
        ]
        db.session.bulk_save_objects(sample)
        db.session.commit()

@app.route('/')
def index():
    q = request.args.get('q', '')
    if q:
        masters = Masterclass.query.filter(Masterclass.title.contains(q)).order_by(Masterclass.date.asc()).all()
    else:
        masters = Masterclass.query.order_by(Masterclass.date.asc()).all()
    return render_template('index.html', masters=masters, q=q)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        instructor = request.form.get('instructor', '').strip()
        date_raw = request.form.get('date', '').strip()
        seats_raw = request.form.get('seats', '0').strip()

        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('create'))

        try:
            date = datetime.fromisoformat(date_raw) if date_raw else None
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD or full ISO format.', 'error')
            return redirect(url_for('create'))

        try:
            seats = int(seats_raw)
            if seats < 0:
                raise ValueError()
        except ValueError:
            flash('Seats must be a non-negative integer', 'error')
            return redirect(url_for('create'))

        mc = Masterclass(title=title, description=description, instructor=instructor, date=date, seats=seats)
        db.session.add(mc)
        db.session.commit()
        flash('Masterclass created', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', action='Create', master=None)

@app.route('/edit/<int:mc_id>', methods=['GET', 'POST'])
def edit(mc_id):
    mc = Masterclass.query.get_or_404(mc_id)
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        instructor = request.form.get('instructor', '').strip()
        date_raw = request.form.get('date', '').strip()
        seats_raw = request.form.get('seats', '0').strip()

        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('edit', mc_id=mc_id))

        try:
            date = datetime.fromisoformat(date_raw) if date_raw else None
        except ValueError:
            flash('Invalid date format. Use YYYY-MM-DD or full ISO format.', 'error')
            return redirect(url_for('edit', mc_id=mc_id))

        try:
            seats = int(seats_raw)
            if seats < 0:
                raise ValueError()
        except ValueError:
            flash('Seats must be a non-negative integer', 'error')
            return redirect(url_for('edit', mc_id=mc_id))

        mc.title = title
        mc.description = description
        mc.instructor = instructor
        mc.date = date
        mc.seats = seats
        db.session.commit()
        flash('Masterclass updated', 'success')
        return redirect(url_for('index'))

    return render_template('form.html', action='Edit', master=mc)

@app.route('/delete/<int:mc_id>', methods=['POST'])
def delete(mc_id):
    mc = Masterclass.query.get_or_404(mc_id)
    db.session.delete(mc)
    db.session.commit()
    flash('Masterclass deleted', 'success')
    return redirect(url_for('index'))

@app.route('/detail/<int:mc_id>')
def detail(mc_id):
    mc = Masterclass.query.get_or_404(mc_id)
    return render_template('detail.html', master=mc)

if __name__ == '__main__':
    app.run(debug=True)
