import sys, os
from pathlib import Path

sys.dont_write_bytecode = True



datastore = []
datastore_iterators = {}
providers = []
options = {}

ROOT_DIR = Path(os.getcwd())
#ROOT_DIR = os.getcwd()

#Path to default scenario.xml file
SCENARIO_XML = Path("scenarios\default_scenario.xml")

# Path to plugins
PluginFolder = Path("./plugins")

# Path to XML schemas
SCENARIO_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/scenario_schema.xsd"
VULNERABILITY_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/vulnerability_metadata_schema.xsd"
SERVICE_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/service_metadata_schema.xsd"
UTILITY_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/utility_metadata_schema.xsd"
GENERATOR_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/generator_metadata_schema.xsd"
ENCODER_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/encoder_metadata_schema.xsd"
NETWORK_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/network_metadata_schema.xsd"
BASE_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/base_metadata_schema.xsd"
BUILDS_SCHEMA_FILE = "#{ROOT_DIR}/lib/schemas/build_metadata_schema.xsd"

# Path to projects directory
PROJECTS_DIR = ("projects")

# Path to modules directories
MODULES_DIR = Path("modules")
VULNERABILITIES_DIR = Path(MODULES_DIR / "vulnerabilities")
SERVICES_DIR = Path(MODULES_DIR / "services")
UTILITIES_DIR = Path(MODULES_DIR / "utilities")
GENERATORS_DIR = Path(MODULES_DIR / "generators")
ENCODERS_DIR = Path(MODULES_DIR / "encoders")
NETWORKS_DIR = Path(MODULES_DIR / "networks")
BASES_DIR = Path(MODULES_DIR / "bases")
BUILDS_DIR = Path(MODULES_DIR / "build")
MODULE_LOCAL_CALC_DIR = Path("secgen_local/local.py")

# Path to resources
WORDLISTS_DIR = os.path.join("lib","resources","wordlists")
LINELISTS_DIR = os.path.join("lib","resources","linelists")
BLACKLISTED_WORDS_FILE = os.path.join("lib","resources","blacklisted_words","blacklist.txt")
IMAGES_DIR = os.path.join("lib","resources","images")
PASSWORDLISTS_DIR = os.path.join("lib","resources","passwordlists")

# Path to cleanup directory
CLEANUP_DIR = os.path.join("modules","build","puppet")

# Retry limits
RETRIES_LIMIT = 5

# Version number of SecGen
# e.g. [release state (0 = alpha, 3 = final release)].[Major bug fix].[Minor bug fix].[Cosmetic or other features]
VERSION_NUMBER = '0.0.0.1'

# Current Provider
cur_provider = ''
