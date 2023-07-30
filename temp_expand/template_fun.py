def reg_temp_expand_fun(app):
    @app.template_global()
    def say_hello(msg: str):
        return f'<h1>你好呀:{msg}</h1>'
