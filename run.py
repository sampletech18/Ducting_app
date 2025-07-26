from ducting_app import create_app  # 👈 fix this line

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
