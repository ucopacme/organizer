import json

import yaml
import botocore
import boto3
import pytest
import moto
from moto import mock_organizations, mock_sts

from orgcrawler.mock import MockOrg

@mock_sts
@mock_organizations
def test_mock_org():
    mock_org = MockOrg()
    print(mock_org.__dir__())
    print(mock_org.root_id)
    #org_id, root_id = mock_org.build('simple')
    #org_id, root_id = mock_org.build('complex')
    assert False
