from flask import Blueprint, render_template


class Common:
    """
    Common class for base template rendering
    """
    def __init__(self):
        self.bp = Blueprint('common', __name__, url_prefix='')

        self.bp.app_errorhandler(404)(self.error_404)
        self.bp.app_errorhandler(500)(self.error_500)

        self.bp.route('/')(self.index)
        self.bp.route('/404')(self.error_404)
        self.bp.route('/500')(self.error_500)

    def index(self):
        """
        Index page
        """
        return render_template(template_name_or_list='index.html')

    def error_404(self, e=None):
        """
        Error 404 page
        """
        return render_template(template_name_or_list='404.html'), 404

    def error_500(self, e=None):
        """
        Error 500 page
        """
        return render_template(template_name_or_list='500.html'), 500
