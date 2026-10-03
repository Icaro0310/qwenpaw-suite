import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest import mock


MODULE_PATH = Path(__file__).with_name("sync-github.py")
SPEC = importlib.util.spec_from_file_location("sync_github", MODULE_PATH)
sync_github = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(sync_github)


class SyncSafetyTests(unittest.TestCase):
    def test_no_repo_path_fails_without_running_git(self):
        with mock.patch.object(sync_github, "SYNC_REPO_PATH", None), mock.patch.object(
            sync_github, "run_git"
        ) as run_git:
            self.assertFalse(sync_github.sync())
        run_git.assert_not_called()

    def test_default_run_is_read_only_dry_run(self):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
            sync_github, "run_git", return_value=(0, " M file.txt", "")
        ) as run_git:
            self.assertTrue(sync_github.sync(tmp))
        run_git.assert_called_once_with(["status", "--porcelain"], cwd=Path(tmp))

    def test_apply_is_required_for_git_writes(self):
        results = [
            (0, " M file.txt", ""),
            (0, "Already up to date", ""),
            (0, "", ""),
            (0, "[main abc123] auto-sync", ""),
            (0, "main -> main", ""),
        ]
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(
            sync_github, "run_git", side_effect=results
        ) as run_git:
            self.assertTrue(sync_github.sync(tmp, apply=True))
        self.assertEqual(
            [call.args[0][0] for call in run_git.call_args_list],
            ["status", "pull", "add", "commit", "push"],
        )


if __name__ == "__main__":
    unittest.main()
