sh '''
echo "Workspace: $WORKSPACE"
echo "Input file actual path: $INPUT_FILE"
ls -l

python3 jenkins/scripts/jenkins_prod/gitlab_svc_removal.py \
  --input "$INPUT_FILE" \
  --output "$OUTPUT_CSV"
'''
