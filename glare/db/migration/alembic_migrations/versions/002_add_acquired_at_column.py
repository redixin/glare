# Copyright 2016 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Add acquired_at column

Revision ID: 002
Revises: 001
Create Date: 2016-10-05 16:03:43.207147

"""

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'

from alembic import op
import sqlalchemy as sa


def upgrade():
    engine = op.get_bind()
    if engine.dialect.dialect_description.startswith('sqlite'):
        op.add_column(
            'glare_artifact_locks',
            sa.Column(
                'acquired_at', sa.DateTime(), nullable=False,
                server_default=sa.text('NOW'))
        )
    else:
        op.add_column(
            'glare_artifact_locks',
            sa.Column(
                'acquired_at', sa.DateTime(), nullable=False,
                server_default=sa.text('NOW()'))
        )


def downgrade():
    op.drop_column('glare_artifact_locks', 'acquired_at')
