from app.service.asg_service import AutoScalingService


def main():
    asg_service = AutoScalingService()
    status = asg_service.get_asg_status()
    print("ASG Status:", status)

    # Example usage of start and stop methods
    # asg_service.start_gpu()
    # print("GPU started")

    # asg_service.stop_gpu()
    # print("GPU stopped")


if __name__ == "__main__":
    main()
