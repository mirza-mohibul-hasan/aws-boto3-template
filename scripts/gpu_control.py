import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from app.services.asg_service import AutoScalingService

asg = AutoScalingService()

if len(sys.argv) < 2:
    print("Usage: start | stop | status")
    exit(1)

cmd = sys.argv[1]

if cmd == "start":
    asg.start_gpu()
    print("GPU ASG starting...")
elif cmd == "stop":
    asg.stop_gpu()
    print("GPU ASG stopping...")
elif cmd == "status":
    print(asg.get_asg_status())
else:
    print("Unknown command")
