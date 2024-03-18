from flask_assets import Bundle, Environment


def register_assets_for(app):
    bundles = {
        'bundle_js':
            Bundle(
                'js/axios-0.21.1.min.js',
                'js/main.js',
                filters='jsmin',
                output='gen/bundle.min.js'
            ),

        'bundle_css':
            Bundle(
                'styles/main.scss',
                depends='styles/*.scss',
                filters=['libsass','cssmin'],
                output='gen/styles.min.css'
            ),
    }

    assets = Environment(app)
    assets.register(bundles)
