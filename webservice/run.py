from app import create_app, db

app = create_app()

# Tạo context để có thể tạo database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)