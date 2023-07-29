from website import create_app

app = create_app("dev")  # dev 或者 pro

# The following code is for local debugging purposes only and should be removed when deploying on Vercel.
# On Vercel, the function is imported and executed as a module, rather than being directly run as the main program.
# Therefore, the code inside if __name__ == '__main__': will not be executed.
if __name__ == '__main__':
    print("web site starting...")
    app.run(host='127.0.0.1', port=8019, debug=False)
