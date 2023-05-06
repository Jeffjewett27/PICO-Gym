import subprocess
import atexit
from .config import host, port

class ProcessManagement:
    instance = None

    @staticmethod
    def get_instance():
        if ProcessManagement.instance is None:
            ProcessManagement.instance = ProcessManagement()
            atexit.register(ProcessManagement.close_instance)
        return ProcessManagement.instance

    @staticmethod
    def close_instance():
        if ProcessManagement.instance is not None:
            ProcessManagement.instance.close()

    def __init__(self) -> None:
        self.processes = []

    def spawn_process(self, *params):
        assert len(params) >= 1
        p = subprocess.Popen(["node", "src/picorunner.js", "-c", *params, "-p", str(port)], cwd='PICO-Node', 
            stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.processes.append(p)

    def close(self):
        for p in self.processes:
            p.kill()
            print(f'Cleaned {p}')
        print('All processes killed')