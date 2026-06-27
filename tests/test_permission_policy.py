import unittest

from mantis.permission_policy import PermissionPolicy
from mantis.permissions import SkillPermission, UserPermission


class PermissionPolicyTest(unittest.TestCase):
    def setUp(self):
        self.policy = PermissionPolicy()

    def test_user_can_run_public_skill(self):
        decision = self.policy.check(
            user_permission=UserPermission.USER,
            skill_permission=SkillPermission.PUBLIC,
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "permission_granted")

    def test_user_can_run_system_skill(self):
        decision = self.policy.check(
            user_permission=UserPermission.USER,
            skill_permission=SkillPermission.SYSTEM,
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "permission_granted")

    def test_user_cannot_run_admin_skill(self):
        decision = self.policy.check(
            user_permission=UserPermission.USER,
            skill_permission=SkillPermission.ADMIN,
        )

        self.assertFalse(decision.allowed)
        self.assertEqual(decision.reason, "insufficient_permission")
        self.assertTrue(decision.override_possible)

    def test_admin_can_run_admin_skill(self):
        decision = self.policy.check(
            user_permission=UserPermission.ADMIN,
            skill_permission=SkillPermission.ADMIN,
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(decision.reason, "permission_granted")


if __name__ == "__main__":
    unittest.main()