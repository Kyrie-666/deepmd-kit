import os
import subprocess as sp
import unittest

from deepmd.cluster.local import get_gpus

from common import tests_path


class TestSingleMachine(unittest.TestCase):
    def setUp(self):
        try:
            import horovod
        except ImportError:
            raise unittest.SkipTest("Package horovod is required for parallel-training tests.")
        self.input_file = str(tests_path / "model_compression" / "input.json")

    def test_two_workers(self):
        command = 'horovodrun -np 2 dp train -m workers ' + self.input_file
        penv = os.environ.copy()
        if len(get_gpus() or []) > 1:
            penv['CUDA_VISIBLE_DEVICES'] = '0,1'
        popen = sp.Popen(command, shell=True, env=penv, stdout=sp.PIPE, stderr=sp.STDOUT)
        for line in iter(popen.stdout.readline, b''):
            if hasattr(line, 'decode'):
                line = line.decode('utf-8')
            line = line.rstrip()
            print(line)
        popen.wait()
        self.assertEqual(0, popen.returncode, 'Parallel training failed!')


if __name__ == '__main__':
    unittest.main()