# aws_stop_all_servers

This lambda script can be used to stop all EC2 instances and scale down the instances in ASG.

Also if a "skip_stop" tag is set as true the script will skip those resources from stopping/scaling down.

Schedule can be setup using cloudwatch eventbridge rule
