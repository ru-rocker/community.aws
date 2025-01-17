#!/usr/bin/python
# Copyright: Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: ec2_vpc_peer
short_description: create, delete, accept, and reject VPC peering connections between two VPCs.
version_added: 1.0.0
description:
  - Read the AWS documentation for VPC Peering Connections
    U(https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpc-peering.html).
options:
  vpc_id:
    description:
      - VPC id of the requesting VPC.
    required: false
    type: str
  peering_id:
    description:
      - Peering connection id.
    required: false
    type: str
  peer_region:
    description:
      - Region of the accepting VPC.
    required: false
    type: str
  peer_vpc_id:
    description:
      - VPC id of the accepting VPC.
    required: false
    type: str
  peer_owner_id:
    description:
      - The AWS account number for cross account peering.
    required: false
    type: str
  tags:
    description:
      - Dictionary of tags to look for and apply when creating a Peering Connection.
    required: false
    type: dict
  state:
    description:
      - Create, delete, accept, reject a peering connection.
    required: false
    default: present
    choices: ['present', 'absent', 'accept', 'reject']
    type: str
  wait:
    description:
      - Wait for peering state changes to complete.
    required: false
    default: false
    type: bool
author: Mike Mochan (@mmochan)
extends_documentation_fragment:
- amazon.aws.aws
- amazon.aws.ec2

requirements: [ botocore, boto3, json ]
'''

EXAMPLES = '''
# Complete example to create and accept a local peering connection.
- name: Create local account VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    vpc_id: vpc-12345678
    peer_vpc_id: vpc-87654321
    state: present
    tags:
      Name: Peering connection for VPC 21 to VPC 22
      CostCode: CC1234
      Project: phoenix
  register: vpc_peer

- name: Accept local VPC peering request
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    peering_id: "{{ vpc_peer.peering_id }}"
    state: accept
  register: action_peer

# Complete example to delete a local peering connection.
- name: Create local account VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    vpc_id: vpc-12345678
    peer_vpc_id: vpc-87654321
    state: present
    tags:
      Name: Peering connection for VPC 21 to VPC 22
      CostCode: CC1234
      Project: phoenix
  register: vpc_peer

- name: delete a local VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    peering_id: "{{ vpc_peer.peering_id }}"
    state: absent
  register: vpc_peer

  # Complete example to create and accept a cross account peering connection.
- name: Create cross account VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    vpc_id: vpc-12345678
    peer_vpc_id: vpc-12345678
    peer_owner_id: 123456789102
    state: present
    tags:
      Name: Peering connection for VPC 21 to VPC 22
      CostCode: CC1234
      Project: phoenix
  register: vpc_peer

- name: Accept peering connection from remote account
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    peering_id: "{{ vpc_peer.peering_id }}"
    profile: bot03_profile_for_cross_account
    state: accept
  register: vpc_peer

# Complete example to create and accept an intra-region peering connection.
- name: Create intra-region VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: us-east-1
    vpc_id: vpc-12345678
    peer_vpc_id: vpc-87654321
    peer_region: us-west-2
    state: present
    tags:
      Name: Peering connection for us-east-1 VPC to us-west-2 VPC
      CostCode: CC1234
      Project: phoenix
  register: vpc_peer

- name: Accept peering connection from peer region
  community.aws.ec2_vpc_peer:
    region: us-west-2
    peering_id: "{{ vpc_peer.peering_id }}"
    state: accept
  register: vpc_peer

# Complete example to create and reject a local peering connection.
- name: Create local account VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    vpc_id: vpc-12345678
    peer_vpc_id: vpc-87654321
    state: present
    tags:
      Name: Peering connection for VPC 21 to VPC 22
      CostCode: CC1234
      Project: phoenix
  register: vpc_peer

- name: Reject a local VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    peering_id: "{{ vpc_peer.peering_id }}"
    state: reject

# Complete example to create and accept a cross account peering connection.
- name: Create cross account VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    vpc_id: vpc-12345678
    peer_vpc_id: vpc-12345678
    peer_owner_id: 123456789102
    state: present
    tags:
      Name: Peering connection for VPC 21 to VPC 22
      CostCode: CC1234
      Project: phoenix
  register: vpc_peer

- name: Accept a cross account VPC peering connection request
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    peering_id: "{{ vpc_peer.peering_id }}"
    profile: bot03_profile_for_cross_account
    state: accept
    tags:
      Name: Peering connection for VPC 21 to VPC 22
      CostCode: CC1234
      Project: phoenix

# Complete example to create and reject a cross account peering connection.
- name: Create cross account VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    vpc_id: vpc-12345678
    peer_vpc_id: vpc-12345678
    peer_owner_id: 123456789102
    state: present
    tags:
      Name: Peering connection for VPC 21 to VPC 22
      CostCode: CC1234
      Project: phoenix
  register: vpc_peer

- name: Reject a cross account VPC peering Connection
  community.aws.ec2_vpc_peer:
    region: ap-southeast-2
    peering_id: "{{ vpc_peer.peering_id }}"
    profile: bot03_profile_for_cross_account
    state: reject

'''
RETURN = '''
task:
  description: The result of the create, accept, reject or delete action.
  returned: success
  type: dict
'''

try:
    import botocore
except ImportError:
    pass  # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.core import is_boto3_error_code
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import ansible_dict_to_boto3_filter_list


def wait_for_state(client, module, state, pcx_id):
    waiter = client.get_waiter('vpc_peering_connection_exists')
    peer_filter = {
        'vpc-peering-connection-id': pcx_id,
        'status-code': state,
    }
    try:
        waiter.wait(
            Filters=ansible_dict_to_boto3_filter_list(peer_filter)
        )
    except botocore.exceptions.WaiterError as e:
        module.fail_json_aws(e, "Failed to wait for state change")
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, "Enable to describe Peerig Connection while waiting for state to change")


def tags_changed(pcx_id, client, module):
    changed = False
    tags = dict()
    if module.params.get('tags'):
        tags = module.params.get('tags')
    pcx = find_pcx_by_id(pcx_id, client, module)
    if pcx['VpcPeeringConnections']:
        pcx_values = [t.values() for t in pcx['VpcPeeringConnections'][0]['Tags']]
        pcx_tags = [item for sublist in pcx_values for item in sublist]
        tag_values = [[key, str(value)] for key, value in tags.items()]
        tags = [item for sublist in tag_values for item in sublist]
        if sorted(pcx_tags) == sorted(tags):
            changed = False
        elif tags:
            delete_tags(pcx_id, client, module)
            create_tags(pcx_id, client, module)
            changed = True
    return changed


def describe_peering_connections(params, client):
    peer_filter = {
        'requester-vpc-info.vpc-id': params['VpcId'],
        'accepter-vpc-info.vpc-id': params['PeerVpcId'],
    }
    result = client.describe_vpc_peering_connections(
        aws_retry=True,
        Filters=ansible_dict_to_boto3_filter_list(peer_filter),
    )
    if result['VpcPeeringConnections'] == []:
        result = client.describe_vpc_peering_connections(
            aws_retry=True,
            Filters=ansible_dict_to_boto3_filter_list(peer_filter),
        )
    return result


def is_active(peering_conn):
    return peering_conn['Status']['Code'] == 'active'


def is_pending(peering_conn):
    return peering_conn['Status']['Code'] == 'pending-acceptance'


def create_peer_connection(client, module):
    changed = False
    params = dict()
    params['VpcId'] = module.params.get('vpc_id')
    params['PeerVpcId'] = module.params.get('peer_vpc_id')
    if module.params.get('peer_region'):
        if not module.botocore_at_least('1.8.6'):
            module.fail_json(msg="specifying peer_region parameter requires botocore >= 1.8.6")
        params['PeerRegion'] = module.params.get('peer_region')
    if module.params.get('peer_owner_id'):
        params['PeerOwnerId'] = str(module.params.get('peer_owner_id'))
    peering_conns = describe_peering_connections(params, client)
    for peering_conn in peering_conns['VpcPeeringConnections']:
        pcx_id = peering_conn['VpcPeeringConnectionId']
        if tags_changed(pcx_id, client, module):
            changed = True
        if is_active(peering_conn):
            return (changed, peering_conn['VpcPeeringConnectionId'])
        if is_pending(peering_conn):
            return (changed, peering_conn['VpcPeeringConnectionId'])
    try:
        peering_conn = client.create_vpc_peering_connection(aws_retry=True, **params)
        pcx_id = peering_conn['VpcPeeringConnection']['VpcPeeringConnectionId']
        if module.params.get('wait'):
            wait_for_state(client, module, 'pending-acceptance', pcx_id)
        if module.params.get('tags'):
            create_tags(pcx_id, client, module)
        changed = True
        return (changed, peering_conn['VpcPeeringConnection']['VpcPeeringConnectionId'])
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))


def remove_peer_connection(client, module):
    pcx_id = module.params.get('peering_id')
    if pcx_id:
        peering_conns = client.describe_vpc_peering_connections(aws_retry=True, VpcPeeringConnectionIds=[pcx_id])
    else:
        params = dict()
        params['VpcId'] = module.params.get('vpc_id')
        params['PeerVpcId'] = module.params.get('peer_vpc_id')
        params['PeerRegion'] = module.params.get('peer_region')
        if module.params.get('peer_owner_id'):
            params['PeerOwnerId'] = str(module.params.get('peer_owner_id'))
        peering_conns = describe_peering_connections(params, client)

    if not peering_conns:
        module.exit_json(changed=False)
    else:
        pcx_id = pcx_id or peering_conns['VpcPeeringConnections'][0]['VpcPeeringConnectionId']

    if peering_conns['VpcPeeringConnections'][0]['Status']['Code'] == 'deleted':
        module.exit_json(msg='Connection in deleted state.', changed=False)
    if peering_conns['VpcPeeringConnections'][0]['Status']['Code'] == 'rejected':
        module.exit_json(msg='Connection has been rejected.  State cannot be changed and will be removed automatically by AWS', changed=False)

    try:
        params = dict()
        params['VpcPeeringConnectionId'] = pcx_id
        client.delete_vpc_peering_connection(aws_retry=True, **params)
        if module.params.get('wait'):
            wait_for_state(client, module, 'deleted', pcx_id)
        module.exit_json(changed=True)
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))


def peer_status(client, module):
    params = dict()
    params['VpcPeeringConnectionIds'] = [module.params.get('peering_id')]
    try:
        vpc_peering_connection = client.describe_vpc_peering_connections(aws_retry=True, **params)
        return vpc_peering_connection['VpcPeeringConnections'][0]['Status']['Code']
    except is_boto3_error_code('InvalidVpcPeeringConnectionId.Malformed') as e:
        module.fail_json_aws(e, msg='Malformed connection ID')
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:  # pylint: disable=duplicate-except
        module.fail_json_aws(e, msg='Error while describing peering connection by peering_id')


def accept_reject(state, client, module):
    changed = False
    params = dict()
    pcx_id = module.params.get('peering_id')
    params['VpcPeeringConnectionId'] = pcx_id
    current_state = peer_status(client, module)
    if current_state not in ['active', 'rejected']:
        try:
            if state == 'accept':
                client.accept_vpc_peering_connection(aws_retry=True, **params)
                target_state = 'active'
            else:
                client.reject_vpc_peering_connection(aws_retry=True, **params)
                target_state = 'rejected'
            if module.params.get('tags'):
                create_tags(params['VpcPeeringConnectionId'], client, module)
            changed = True
            if module.params.get('wait'):
                wait_for_state(client, module, target_state, pcx_id)
        except botocore.exceptions.ClientError as e:
            module.fail_json(msg=str(e))
    if tags_changed(params['VpcPeeringConnectionId'], client, module):
        changed = True
    return changed, params['VpcPeeringConnectionId']


def load_tags(module):
    tags = []
    if module.params.get('tags'):
        for name, value in module.params.get('tags').items():
            tags.append({'Key': name, 'Value': str(value)})
    return tags


def create_tags(pcx_id, client, module):
    try:
        delete_tags(pcx_id, client, module)
        client.create_tags(aws_retry=True, Resources=[pcx_id], Tags=load_tags(module))
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))


def delete_tags(pcx_id, client, module):
    try:
        client.delete_tags(aws_retry=True, Resources=[pcx_id])
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))


def find_pcx_by_id(pcx_id, client, module):
    try:
        return client.describe_vpc_peering_connections(aws_retry=True, VpcPeeringConnectionIds=[pcx_id])
    except botocore.exceptions.ClientError as e:
        module.fail_json(msg=str(e))


def main():
    argument_spec = dict(
        vpc_id=dict(),
        peer_vpc_id=dict(),
        peer_region=dict(),
        peering_id=dict(),
        peer_owner_id=dict(),
        tags=dict(required=False, type='dict'),
        state=dict(default='present', choices=['present', 'absent', 'accept', 'reject']),
        wait=dict(default=False, type='bool'),
    )
    required_if = [
        ('state', 'present', ['vpc_id', 'peer_vpc_id']),
        ('state', 'accept', ['peering_id']),
        ('state', 'reject', ['peering_id'])
    ]

    module = AnsibleAWSModule(argument_spec=argument_spec, required_if=required_if)

    state = module.params.get('state')
    peering_id = module.params.get('peering_id')
    vpc_id = module.params.get('vpc_id')
    peer_vpc_id = module.params.get('peer_vpc_id')

    try:
        client = module.client('ec2', retry_decorator=AWSRetry.jittered_backoff())
    except (botocore.exceptions.ClientError, botocore.exceptions.BotoCoreError) as e:
        module.fail_json_aws(e, msg='Failed to connect to AWS')

    if state == 'present':
        (changed, results) = create_peer_connection(client, module)
        module.exit_json(changed=changed, peering_id=results)
    elif state == 'absent':
        if not peering_id and (not vpc_id or not peer_vpc_id):
            module.fail_json(msg='state is absent but one of the following is missing: peering_id or [vpc_id, peer_vpc_id]')

        remove_peer_connection(client, module)
    else:
        (changed, results) = accept_reject(state, client, module)
        module.exit_json(changed=changed, peering_id=results)


if __name__ == '__main__':
    main()
