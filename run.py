from blueprints.app import  create_app,db

flask_app = create_app()

with flask_app.app_context():
    db.create_all()

if __name__ == "__main__":
    flask_app.run(debug=True)