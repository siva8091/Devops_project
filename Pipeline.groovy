aws ec2 describe-volumes \
 --filters Name=attachment.instance-id,Values=<old_instance_id> \
 --query "Volumes[?Attachments[?Device!='/dev/sda1']].[VolumeId,Attachments[0].Device]" \
 --output table
