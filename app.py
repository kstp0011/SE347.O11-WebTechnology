from musicapp import create_app
# import threading

app = create_app()

if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
    # threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()
