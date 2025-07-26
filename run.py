from app import create_app  # ✅ matches folder name # 👈 fix this line

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
