from setuptools import setup, find_packages

setup(
    name = 'simp_le2certbot',
    version = '0',
    url = 'https://github.com/meeuw/simp_le2certbot.git',
    author = 'Dick Marinus',
    author_email = 'dick@mrns.nl',
    description = 'Convert simp_le to certbot configuration',
    packages = find_packages(),    
    install_requires = ["acme>=0.26,<0.27", "josepy"],
    entry_points={
        'console_scripts': [
            'external-helper = simp_le2certbot.external_helper:main',
            'getaccount = simp_le2certbot.getaccount:main',
            'rsapem2json = simp_le2certbot.rsapem2json:main',
            'simp_le2certbot = simp_le2certbot.simp_le2certbot:main',
        ],
    }
)
