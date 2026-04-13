try:
    from pytest_astropy_header.display import (PYTEST_HEADER_MODULES,
                                               TESTED_VERSIONS)
except ImportError:
    PYTEST_HEADER_MODULES = {}
    TESTED_VERSIONS = {}

try:
    from peaker import __version__ as version
except ImportError:
    version = 'unknown'

# Uncomment and customize the following lines to add/remove entries
# from the list of packages for which version numbers are displayed
# when running the tests.
PYTEST_HEADER_MODULES['astropy'] = 'astropy'
PYTEST_HEADER_MODULES['Matplotlib'] = 'Matplotlib'
PYTEST_HEADER_MODULES['fpdf2'] = 'fpdf2'
PYTEST_HEADER_MODULES['pyartifactory'] = 'pyartifactory'

TESTED_VERSIONS['peaker'] = version
