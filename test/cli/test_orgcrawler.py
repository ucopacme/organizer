import pytest
from click.testing import CliRunner
from moto import (
    mock_organizations,
    mock_sts,
    mock_iam,
)

import orgcrawler
from orgcrawler import payloads
from orgcrawler.cli import orgcrawler
from orgcrawler.mock import (
    MockOrganization,
    MASTER_ACCOUNT_ID,
    ORG_ACCESS_ROLE,
)


@mock_sts
@mock_organizations
@mock_iam
@pytest.mark.parametrize('options_list', [
    (['--help']),
    (['--version']),
    (['--master-role', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases']),
    (['-r', ORG_ACCESS_ROLE, '--accounts', 'account01,account02', 'orgcrawler.payloads.get_account_aliases']),
    (['-r', ORG_ACCESS_ROLE, '--regions', 'us-west-2', 'orgcrawler.payloads.get_account_aliases']),
    (['-r', ORG_ACCESS_ROLE, '--service', 'iam', 'orgcrawler.payloads.get_account_aliases']),
    (['-r', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases', '--account-role', ORG_ACCESS_ROLE]),
    (['-r', ORG_ACCESS_ROLE, 'get_account_aliases', '--payload-file', payloads.__file__]),
])
def test_orgcrawler_success(options_list):
    MockOrganization().simple()
    runner = CliRunner()
    result = runner.invoke(
        orgcrawler.main,
        options_list,
    )
    assert result.exit_code == 0


@mock_sts
@mock_organizations
@mock_iam
@pytest.mark.parametrize('options_list', [
    (['--blee']),
    (['--master-role']),
    (['--master-role', 'blee']),
    (['--master-role', ORG_ACCESS_ROLE, 'orgcrawler.payloads.blee']),
    (['-r', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases', '--accounts']),
    (['-r', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases', '--accounts', 'blee']),
    (['-r', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases', '--regions']),
    (['-r', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases', '--regions', 'blee']),
    (['-r', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases', '--service']),
    (['-r', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases', '--service', 'blee']),
    (['-r', ORG_ACCESS_ROLE, 'orgcrawler.payloads.get_account_aliases', '--account-role']),
    (['-r', ORG_ACCESS_ROLE, '--payload-file', '/no/such/file', 'get_account_aliases']),
    (['-r', ORG_ACCESS_ROLE, '--payload-file', payloads.__file__, 'blee']),
])
def test_orgcrawler_failure(options_list):
    MockOrganization().simple()
    runner = CliRunner()
    result = runner.invoke(
        orgcrawler.main,
        options_list,
    )
    assert result.exit_code != 0
