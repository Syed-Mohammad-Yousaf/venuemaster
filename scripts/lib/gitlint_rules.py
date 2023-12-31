import re
import sys
from typing import List, Text

from gitlint.git import GitCommit
from gitlint.rules import (
    CommitMessageTitle,
    CommitRule,
    LineRule,
    RuleViolation,
)

# Word list from https://github.com/m1foley/fit-commit
# Copyright (c) 2015 Mike Foley
# License: MIT
# Ref: fit_commit/validators/tense.rb
# This list contains the non-imperative-to-imperative word mapping. The
# value must always be a capitalized word which sets the imperative mood.
WHITELISTED_RULES = {
    "accepted": "Accept",
    "accepting": "Accept",
    "accepts": "Accept",
    "accessed": "Access",
    "accesses": "Access",
    "accessing": "Access",
    "activated": "Activate",
    "activates": "Activate",
    "activating": "Activate",
    "added": "Add",
    "adding": "Add",
    "adds": "Add",
    "adjusted": "Adjust",
    "adjusting": "Adjust",
    "adjusts": "Adjust",
    "aligned": "Align",
    "aligning": "Align",
    "aligns": "Align",
    "allowed": "Allow",
    "allowing": "Allow",
    "allows": "Allow",
    "amended": "Amend",
    "amending": "Amend",
    "amends": "Amend",
    "applied": "Apply",
    "applies": "Apply",
    "applying": "Apply",
    "assigned": "Assign",
    "assigning": "Assign",
    "assigns": "Assign",
    "breaking": "Break",
    "breaks": "Break",
    "bringing": "Bring",
    "brings": "Bring",
    "broke": "Break",
    "brought": "Bring",
    "bumped": "Bump",
    "bumping": "Bump",
    "bumps": "Bump",
    "calculated": "Calculate",
    "calculates": "Calculate",
    "calculating": "Calculate",
    "called": "Call",
    "calling": "Call",
    "calls": "Call",
    "changed": "Change",
    "changes": "Change",
    "changing": "Change",
    "checked": "Check",
    "checking": "Check",
    "checks": "Check",
    "clarified": "Clarify",
    "clarified": "Clarify",
    "clarifying": "Clarify",
    "cleaned": "Clean",
    "cleaning": "Clean",
    "cleans": "Clean",
    "commits": "Commit",
    "committed": "Commit",
    "committing": "Commit",
    "converted": "Convert",
    "converting": "Convert",
    "converts": "Convert",
    "copied": "Copy",
    "copies": "Copy",
    "copying": "Copy",
    "corrected": "Correct",
    "correcting": "Correct",
    "corrects": "Correct",
    "counted": "Count",
    "counting": "Count",
    "counts": "Count",
    "created": "Create",
    "creates": "Create",
    "creating": "Create",
    "darkened": "Darken",
    "darkening": "Darken",
    "darkens": "Darken",
    "decrypted": "Decrypt",
    "decrypting": "Decrypt",
    "decrypts": "Decrypt",
    "deleted": "Delete",
    "deletes": "Delete",
    "deleting": "Delete",
    "derivation": "Derive",
    "derived": "Derive",
    "derives": "Derive",
    "did": "Do",
    "disabled": "Disable",
    "disables": "Disable",
    "disabling": "Disable",
    "disallowed": "Disallow",
    "disallowing": "Disallow",
    "disallows": "Disallow",
    "displayed": "Display",
    "displaying": "Display",
    "displays": "Display",
    "documented": "Document",
    "documenting": "Document",
    "documents": "Document",
    "doing": "Do",
    "don't": "Don't",
    "done": "Do",
    "downloaded": "Download",
    "downloading": "Download",
    "downloads": "Download",
    "dropped": "Drop",
    "dropping": "Drop",
    "drops": "Drop",
    "dryed": "Dry",
    "drying": "Dry",
    "drys": "Dry",
    "enabled": "Enable",
    "enables": "Enable",
    "enabling": "Enable",
    "encrypted": "Encrypt",
    "encrypting": "Encrypt",
    "encrypts": "Encrypt",
    "ended": "End",
    "ending": "End",
    "ends": "End",
    "enforced": "Enforce",
    "enforces": "Enforce",
    "enforcing": "Enforce",
    "enqueued": "Enqueue",
    "enqueues": "Enqueue",
    "enqueuing": "Enqueue",
    "ensured": "Ensure",
    "ensures": "Ensure",
    "ensuring": "Ensure",
    "excluded": "Exclude",
    "excludes": "Exclude",
    "excluding": "Exclude",
    "exposed": "Expose",
    "exposes": "Expose",
    "exposing": "Expose",
    "extended": "Extend",
    "extending": "Extend",
    "extends": "Extend",
    "extracted": "Extract",
    "extracting": "Extract",
    "extracts": "Extract",
    "failed": "Fail",
    "failing": "Fail",
    "fails": "Fail",
    "fetched": "Fetch",
    "fetches": "Fetch",
    "fetching": "Fetch",
    "filtered": "Filter",
    "filtering": "Filter",
    "filters": "Filter",
    "finished": "Finish",
    "finishes": "Finish",
    "finishing": "Finish",
    "fixed": "Fix",
    "fixes": "Fix",
    "fixing": "Fix",
    "forked": "Fork",
    "forking": "Fork",
    "forks": "Fork",
    "formats": "Format",
    "formatted": "Format",
    "formatting": "Format",
    "gets": "Get",
    "getting": "Get",
    "given": "Give",
    "gives": "Give",
    "giving": "Give",
    "got": "Get",
    "grouped": "Group",
    "grouping": "Group",
    "groups": "Group",
    "guarded": "Guard",
    "guarding": "Guard",
    "guards": "Guard",
    "handled": "Handle",
    "handles": "Handle",
    "handling": "Handle",
    "hid": "Hide",
    "hides": "Hide",
    "hiding": "Hide",
    "ignored": "Ignore",
    "ignores": "Ignore",
    "ignoring": "Ignore",
    "implemented": "Implement",
    "implementing": "Implement",
    "implements": "Implement",
    "imported": "Import",
    "importing": "Import",
    "imports": "Import",
    "improved": "Improve",
    "improves": "Improve",
    "improving": "Improve",
    "included": "Include",
    "includes": "Include",
    "including": "Include",
    "increased": "Increase",
    "increases": "Increase",
    "increasing": "Increase",
    "inherited": "Inherit",
    "inheriting": "Inherit",
    "inherits": "Inherit",
    "inserted": "Insert",
    "inserting": "Insert",
    "inserts": "Insert",
    "installed": "Install",
    "installing": "Install",
    "installs": "Install",
    "integrated": "Integrate",
    "integrates": "Integrate",
    "integrating": "Integrate",
    "keeping": "Keep",
    "keeps": "Keep",
    "kept": "Keep",
    "killed": "Kill",
    "killing": "Kill",
    "kills": "Kill",
    "limited": "Limit",
    "limiting": "Limit",
    "limits": "Limit",
    "linked": "Link",
    "linking": "Link",
    "links": "Link",
    "loaded": "Load",
    "loading": "Load",
    "loads": "Load",
    "looked": "Look",
    "looking": "Look",
    "looks": "Look",
    "loses": "Lose",
    "losing": "Lose",
    "lost": "Lose",
    "made": "Make",
    "makes": "Make",
    "making": "Make",
    "managed": "Manage",
    "manages": "Manage",
    "managing": "Manage",
    "mapped": "Map",
    "mapping": "Map",
    "maps": "Map",
    "marked": "Mark",
    "marking": "Mark",
    "marks": "Mark",
    "matched": "Match",
    "matches": "Match",
    "matching": "Match",
    "merged": "Merge",
    "merges": "Merge",
    "merging": "Merge",
    "migrated": "Migrate",
    "migrates": "Migrate",
    "migrating": "Migrate",
    "mocked": "Mock",
    "mocking": "Mock",
    "mocks": "Mock",
    "modified": "Modify",
    "modifies": "Modify",
    "modifying": "Modify",
    "moved": "Move",
    "moves": "Move",
    "moving": "Move",
    "normalized": "Normalize",
    "normalizes": "Normalize",
    "normalizing": "Normalize",
    "ordered": "Order",
    "ordering": "Order",
    "orders": "Order",
    "organized": "Organize",
    "organizes": "Organize",
    "organizing": "Organize",
    "overridden": "Override",
    "overrides": "Override",
    "overriding": "Override",
    "passed": "Pass",
    "passes": "Pass",
    "passing": "Pass",
    "patched": "Patch",
    "patches": "Patch",
    "patching": "Patch",
    "permits": "Permit",
    "permitted": "Permit",
    "permitting": "Permit",
    "populated": "Populate",
    "populating": "Populate",
    "populating": "Populate",
    "prepared": "Prepare",
    "prepares": "Prepare",
    "preparing": "Prepare",
    "prevented": "Prevent",
    "preventing": "Prevent",
    "prevents": "Prevent",
    "processed": "Process",
    "processes": "Process",
    "processing": "Process",
    "pushed": "Push",
    "pushes": "Push",
    "pushing": "Push",
    "raised": "Raise",
    "raises": "Raise",
    "raising": "Raise",
    "ran": "Run",
    "reading": "Read",
    "reads": "Read",
    "rearranged": "Rearrange",
    "rearranges": "Rearrange",
    "rearranging": "Rearrange",
    "rebased": "Rebase",
    "rebases": "Rebase",
    "rebasing": "Rebase",
    "recognised": "Recognise",
    "recognises": "Recognise",
    "recognising": "Recognise",
    "redirected": "Redirect",
    "redirecting": "Redirect",
    "redirects": "Redirect",
    "reduced": "Reduce",
    "reduces": "Reduce",
    "reducing": "Reduce",
    "refactored": "Refactor",
    "refactoring": "Refactor",
    "refactors": "Refactor",
    "rejected": "Reject",
    "rejecting": "Reject",
    "rejects": "Reject",
    "removed": "Remove",
    "removes": "Remove",
    "removing": "Remove",
    "renamed": "Rename",
    "renames": "Rename",
    "renaming": "Rename",
    "reordered": "Reorder",
    "reordering": "Reorder",
    "reorders": "Reorder",
    "reorganised": "Reorganise",
    "reorganises": "Reorganise",
    "reorganising": "Reorganise",
    "replaced": "Replace",
    "replaces": "Replace",
    "replacing": "Replace",
    "required": "Require",
    "requires": "Require",
    "requiring": "Require",
    "resets": "Reset",
    "resetted": "Reset",
    "resetting": "Reset",
    "resolved": "Resolve",
    "resolves":  "Resolve",
    "resolving": "Resolve",
    "restarted": "Restart",
    "restarting": "Restart",
    "restarts": "Restart",
    "restored": "Restore",
    "restores": "Restore",
    "restoring": "Restore",
    "restricted": "Restrict",
    "restricting": "Restrict",
    "restricts": "Restrict",
    "retried": "Retry",
    "retries": "Retry",
    "retrieved": "Retrieve",
    "retrieves": "Retrieve",
    "retrieving": "Retrieve",
    "retrying": "Retry",
    "returned": "Return",
    "returning": "Return",
    "returns": "Return",
    "reverted": "Revert",
    "reverting": "Revert",
    "reverts": "Revert",
    "running": "Run",
    "runs": "Run",
    "saved": "Save",
    "saves": "Save",
    "saving": "Save",
    "searched": "Search",
    "searches": "Search",
    "searching": "Search",
    "selected": "Select",
    "selecting": "Select",
    "selects": "Select",
    "sending": "Send",
    "sends": "Send",
    "sent": "Send",
    "separated": "Separate",
    "separates": "Separate",
    "separating": "Separate",
    "served": "Serve",
    "serves": "Serve",
    "serving": "Serve",
    "sets": "Set",
    "setting": "Set",
    "setup": "Setup",
    "shifted": "Shift",
    "shifted": "Shift",
    "shifting": "Shift",
    "showed": "Show",
    "showing": "Show",
    "shows": "Show",
    "simplified": "Simplify",
    "simplifies": "Simplify",
    "simplifying": "Simplify",
    "skipped": "Skip",
    "skipping": "Skip",
    "skips": "Skip",
    "sorting": "Sort",
    "sorts": "Sort",
    "specified": "Specify",
    "specifies": "Specify",
    "specifying": "Specify",
    "sped": "Speed",
    "speeding": "Speed",
    "speeds": "Speed",
    "splits": "Split",
    "splitted": "Split",
    "splitting": "Split",
    "standardised": "Standardise",
    "standardises": "Standardise",
    "standardising": "Standardise",
    "standardized": "Standardize",
    "standardizes": "Standardize",
    "standardizing": "Standardize",
    "started": "Start",
    "starting": "Start",
    "starts": "Start",
    "stopped": "Stop",
    "stopping": "Stop",
    "stops": "Stop",
    "supported": "Support",
    "supporting": "Support",
    "supports": "Support",
    "suppressed": "Suppress",
    "suppresses": "Suppress",
    "suppressing": "Suppress",
    "switched": "Switch",
    "switches": "Switch",
    "switching": "Switch",
    "synced": "Sync",
    "syncing": "Sync",
    "syncs": "Sync",
    "takes": "Take",
    "taking": "Take",
    "telling": "Tell",
    "tells": "Tell",
    "tested": "Test",
    "testing": "Test",
    "tests": "Test",
    "told": "Tell",
    "took": "Take",
    "truncated": "Truncate",
    "truncates": "Truncate",
    "truncating": "Truncate",
    "turned": "Turn",
    "turning": "Turn",
    "turns": "Turn",
    "updated": "Update",
    "updates": "Update",
    "updating": "Update",
    "upgraded": "Upgrade",
    "upgraded": "Upgrade",
    "upgrading": "Upgrade",
    "uploaded": "Upload",
    "uploading": "Upload",
    "uploads": "Upload",
    "used": "Use",
    "uses": "Use",
    "using": "Use",
    "validated": "Validate",
    "validates": "Validate",
    "validating": "Validate",
    "verified": "Verify",
    "verifies": "Verify",
    "verifying": "Verify",
}

with open(__file__) as f:
    data = f.read()
    result = re.search('WHITELISTED_RULES = {(.*?)}', data, flags=re.DOTALL)
    if not result:
        print("WHITELISTED_RULES list not found through regex")
        sys.exit(1)

    lines = result.group(1).split(',')
    lines = [l.strip() for l in lines if l.strip()]
    for left, right in zip(lines, sorted(lines)):
        if left != right:
            print("Expected {}, found {}. WHITELISTED_RULES list not "
                  "sorted.".format(right, left))
            sys.exit(1)

        for word in right.split(':'):
            word = word.strip()
            if word.startswith("'"):
                print("Change {} to {}.".format(word, word.replace("'", '"')))
                sys.exit(1)

# To update WHITELISTED_WORDS list update WHITELISTED_RULES list.
WHITELISTED_WORDS = set(WHITELISTED_RULES.values())
for word in WHITELISTED_WORDS:
    if not word[0].isupper():
        print("Issue with WHITELISTED_WORDS list. "
              "{} not capitalized.".format(word))
        sys.exit(1)


def get_first_word(line: str) -> str:
    # Ignore the section tag (ie `<section tag>: <message body>.`)
    words = line.split(': ', 1)[-1].split()
    return words[0]


class ImperativeMood(LineRule):
    """ Check for imperative mode.

    This rule will enforce that the commit message title uses imperative
    mood.  This is done by checking if the lowercased first word is in
    `WHITELISTED_RULES`, if so show the word in the correct mood.
    """

    name = "title-imperative-mood"
    id = "DRZ1"
    target = CommitMessageTitle

    error_msg = ('The commit title "{title}" not in imperative mood. '
                 'Change "{word}" to "{imperative}".')

    def validate(self,
                 line: Text,
                 commit: GitCommit) -> List[RuleViolation]:
        violations = []  # type: List[RuleViolation]
        first_word = get_first_word(line)
        first_word_lowered = first_word.lower()
        if first_word_lowered in WHITELISTED_RULES:
            imperative = WHITELISTED_RULES[first_word_lowered]
            if imperative.lower() == first_word_lowered:
                # The keys in whitelisted_rules show the non-imperative mood
                # versions of the words. We can have an item which won't follow
                # this rule, e.g. {"don't": "Don't"}, which will have same word
                # as both key and value. If this is the case, there is no need
                # to raise the error.
                return violations

            violation = RuleViolation(self.id, self.error_msg.format(
                word=first_word,
                imperative=imperative,
                title=commit.message.title
            ))

            violations.append(violation)

        return violations


class IsFirstWordWhiteListed(LineRule):
    """ Check first word is whitelisted.

    This rule will enforce that the first word in commit title message
    is in whitelisted words.
    """

    name = "title-first-word-whitelisted"
    id = "DRZ2"
    target = CommitMessageTitle

    error_msg = ('Word "{word}" in commit title "{title}" not whitelisted. '
                 'Update scripts.lib.gitlint_rules.WHITELISTED_WORDS list '
                 'to fix this.')

    def validate(self,
                 line: Text,
                 commit: GitCommit) -> List[RuleViolation]:
        violations = []
        first_word = get_first_word(line)
        first_word_lowered = first_word.lower()
        if (first_word not in WHITELISTED_WORDS and
                first_word_lowered not in WHITELISTED_RULES):
            violation = RuleViolation(self.id, self.error_msg.format(
                word=first_word,
                title=commit.message.title
            ))

            violations.append(violation)

        return violations


class ContainsIssueRef(CommitRule):
    """ The commit should contain a reference to issue.

    The commit body should contain either an RT #123 or Fixes #123. RT means
    related to.
    """

    name = "issue-reference"
    id = "DRZ3"

    error_msg = ('Word "{word}" in commit title "{title}" not whitelisted. '
                 'Update scripts.lib.gitlint_rules.WHITELISTED_WORDS list '
                 'to fix this.')

    def validate(self, commit):
        if commit.message.title.startswith('version:'):
            return []

        body = commit.message.body

        for line in body:
            if line.startswith("RT #") or line.startswith("Fixes #"):
                return []

        error = """
            The commit body is missing an RT #123 or Fixes #123. Please refer
            the issue number this commit is resolving. Here are examples of a
            valid commit message:

            ### Example 1
            gitlint: Add new rule to check issue reference.

            Fixes #391

            ### Example 2
            gitlint: Add new rule to check issue reference.

            RT #391
        """

        return [RuleViolation(self.id, error)]
