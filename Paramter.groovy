WORKSPACE = os.environ.get("WORKSPACE", ".")

INPUT_FILE = os.environ.get("INPUT_FILE", os.path.join(WORKSPACE, "jenkins_jobs.txt"))
OUTPUT_CSV = os.environ.get("OUTPUT_CSV", os.path.join(WORKSPACE, "output.csv"))
PROGRESS_FILE = os.path.join(WORKSPACE, "progress.json")

WORKSPACE = os.environ.get("WORKSPACE", ".")

INPUT_FILE = os.environ.get("INPUT_FILE")
OUTPUT_CSV = os.path.join(WORKSPACE, os.environ.get("OUTPUT_CSV", "output.csv"))
PROGRESS_FILE = os.path.join(WORKSPACE, "progress.json")

