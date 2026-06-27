import time
import unittest

from mantis.kernel import Kernel
from mantis.permissions import UserPermission


class KernelOverrideTest(unittest.TestCase):
    def setUp(self):
        self.kernel = Kernel()

    def test_base_permission_is_returned_without_override(self):
        permission = self.kernel.get_effective_user_permission(UserPermission.USER)

        self.assertEqual(permission, UserPermission.USER)

    def test_override_replaces_base_permission(self):
        self.kernel.enable_override(
            permission=UserPermission.ADMIN,
            duration_seconds=60,
        )

        permission = self.kernel.get_effective_user_permission(UserPermission.USER)

        self.assertEqual(permission, UserPermission.ADMIN)

    def test_expired_override_is_cleared(self):
        self.kernel.enable_override(
            permission=UserPermission.ADMIN,
            duration_seconds=1,
        )

        self.kernel.override_until = time.time() - 1

        permission = self.kernel.get_effective_user_permission(UserPermission.USER)

        self.assertEqual(permission, UserPermission.USER)
        self.assertIsNone(self.kernel.override_permission)
        self.assertIsNone(self.kernel.override_until)


if __name__ == "__main__":
    unittest.main()