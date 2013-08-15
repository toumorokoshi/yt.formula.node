"""
Tests for the node formula
"""
import os
import tempfile
import shutil

from sprinter.testtools import create_mock_environment

source_config = """
[update]
formula = yt.formula.node
version = 0.10.16
packages =
  grunt-cli@0.3.1
"""

target_config = """
[install]
formula = yt.formula.node
version = 0.10.16
packages =
  grunt-cli@~0.4.1

[update]
formula = yt.formula.node
version = 0.10.16
packages =
  grunt-cli@0.4.2
"""


class TestNodeFormula(object):
    """
    Run node.js formula tests
    """

    def setup(self):
        self.temp_dir = tempfile.mkdtemp()
        self.environment = create_mock_environment(source_config=source_config,
                                                   target_config=target_config,
                                                   mock_directory=False,
                                                   root=self.temp_dir)
        self.directory = self.environment.directory

    def teardown(self):
        shutil.rmtree(self.temp_dir)

    def test_install(self):
        self.environment.warmup()
        self.environment.run_feature("install", 'sync')
        assert os.path.exists(self.environment.directory.install_directory('install'))
        assert os.path.exists(os.path.join(self.environment.directory.install_directory('install'), 'bin', 'node'))
        assert os.path.exists(os.path.join(self.environment.directory.install_directory('install'), 'bin', 'npm'))
