import sys


class LoadingBar:
    @staticmethod
    def loading_bar(iterations, total_iterations):
        percent_complete = (iterations / total_iterations) * 100
        bar_length = 20
        filled_length = int(bar_length * iterations // total_iterations)
        bar = "=" * filled_length + "-" * (bar_length - filled_length)

        sys.stdout.write(f"\r[{bar}] {percent_complete:.2f}% Complete")
        sys.stdout.flush()
