import requests, urllib3, urllib.parse, csv, os, argparse, sys, time, json, re
urllib3.disable_warnings()

# ---------------- ARGUMENTS ----------------
parser = argparse.ArgumentParser()
parser.add_argument("--input")
parser.add_argument("--output")
parser.add_argument("--jenkins_base")
parser.add_argument("--token")

args = parser.parse_args()

# ---------------- CONFIG (DEFAULTS) ----------------
J_USER = 'SVC-jenkinsadmin'
J_TOKEN = 'your_default_token_here'
GL_TOKEN = 'your_gitlab_token'
GITLAB_URL = 'https://gitlab.verizon.com'
JENKINS_BASE = 'https://jenkins-gts.vpc.verizon.com/gts'

KEYWORDS = [
    'updateGitLabCommitStatus',
    'gitlabCommitStatus',
    'addGitLabMRComment',
    'acceptGitLabMR',
    'deleteGitLabBranch',
    'createGitLabTag'
]

# ---------------- WORKSPACE ----------------
WORKSPACE = os.environ.get("WORKSPACE", ".")

# ---------------- FINAL VALUES (PIPELINE OVERRIDE) ----------------
INPUT_FILE = args.input if args.input else os.path.join(WORKSPACE, "jenkins_jobs.txt")
OUTPUT_CSV = args.output if args.output else os.path.join(WORKSPACE, "output.csv")
PROGRESS_FILE = os.path.join(WORKSPACE, "progress.json")

JENKINS_BASE = args.jenkins_base if args.jenkins_base else JENKINS_BASE
J_TOKEN = args.token if args.token else J_TOKEN

# ---------------- DEBUG ----------------
print("INPUT_FILE:", INPUT_FILE)
print("OUTPUT_CSV:", OUTPUT_CSV)
print("JENKINS_BASE:", JENKINS_BASE)

# ---------------- VALIDATION ----------------
if not os.path.exists(INPUT_FILE):
    print(f"ERROR: Input file not found: {INPUT_FILE}")
    sys.exit(1)
