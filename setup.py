from setuptools import setup

setup(
    name="basil-dump-api",
    version="0.1.0.dev",
    py_modules=['storage', 'api', 'server'],

    description="API serving content from Eve Online data dump.",
    install_requires=["Cython==0.23.4",
                      "falcon==0.3.0",
                      "gevent==1.0.2",
                      "gunicorn==19.4.1",
                      "SQLAlchemy==1.0.10"],
)

