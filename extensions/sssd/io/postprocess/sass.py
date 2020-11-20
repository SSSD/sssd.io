
import sass


def process_sass(app, exception):
    if exception is not None or app.builder.name != 'html':
        return

    staticdir = f'{app.builder.outdir}/_static'
    sass.compile(
        dirname=(f'{staticdir}/sass', f'{staticdir}/css'),
        output_style='compressed'
    )

    print("Postprocess: SASS compiled successfuly")
