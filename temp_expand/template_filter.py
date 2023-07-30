def reg_temp_expand_filter(app):
    @app.template_filter()
    def to_str(value):
        return str(value)
