#    Copyright 2017 phData Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import argparse
import logging
from conf import Conf
from commands import promote_pipeline, export_pipeline, import_pipeline

logging.basicConfig(level=logging.DEBUG)

config = Conf()

def promote_command(args):
    promote_pipeline.main(config, args)

def export_command(args):
    export_pipeline.main(config, args)


def import_command(args):
    import_pipeline.main(config, args)

def main():
    """Main script entry point."""
    parser = argparse.ArgumentParser(description='Promote an SDC pipeline from one environment to another.')
    subparsers = parser.add_subparsers(help='sdc-util')

    define_pipeline_args(subparsers)

    args = parser.parse_args()
    args.func(args)

def define_pipeline_args(subparsers):

    pipeline_parser = subparsers.add_parser("pipeline", help='Available commands: \'pipeline\'')

    pipeline_subparsers = pipeline_parser.add_subparsers(help="Pipeline commands")

    # pipeline promote arguments
    promote_parser = pipeline_subparsers.add_parser('promote', help='Promote a pipeline from one SDC to another.')
    promote_parser.add_argument('--src', required=True, dest='src_instance', metavar='source_instance_name',
                                help='The instance name of the source SDC (must match the name in conf.yml)')
    promote_parser.add_argument('--dest', required=True, dest='dest_instance', metavar='dest_instance_name',
                                help='The instance name of the destination SDC (must match the name in conf.yml)')
    promote_parser.add_argument('--srcPipelineId', required=True, dest='src_pipeline_id',
                                metavar='source-pipeline-id',
                                help='The ID of a pipeline in the source SDC')
    promote_parser.add_argument('--destPipelineId', required=False, dest='dest_pipeline_id',
                                metavar='destination-pipeline-id',
                                help='The ID of a pipeline in the destination SDC')
    promote_parser.add_argument('--start', action='store_true', dest='start_dest',
                                help='Start the destination pipeline if the import is successful.')
    promote_parser.set_defaults(func=promote_command)

    # pipeline export arguments
    export_parser = pipeline_subparsers.add_parser('export', help='Export a pipeline to a file.')
    export_parser.add_argument('--src', required=True, dest='src_instance', metavar='source',
                               help='The instance name of the source SDC (must match the name in conf.yml)')
    export_parser.add_argument('--pipelineId', required=True, dest='src_pipeline_id',
                               metavar='sourcePipelineId', help='The ID of a pipeline in the source SDC')
    export_parser.add_argument('--out', required=True, dest='out', help='Output file path')
    export_parser.set_defaults(func=export_command)

    # pipeline import arguments
    import_parser = pipeline_subparsers.add_parser('import', help='Import a pipeline from a JSON file.')
    import_parser.add_argument('--dest', required=True, dest='dst_instance', metavar='dest_instance',
                               help='The name of the destination SDC (must match an instance name in conf.yml)')
    import_parser.add_argument('--pipelineId', required=True, dest='pipeline_id',
                               metavar='destinationPipelineId', help='The ID of a pipeline in the source SDC')
    import_parser.add_argument('--pipelineJson', required=True, dest='pipeline_json', help='Pipeline json file path')
    import_parser.set_defaults(func=import_command)

if __name__ == '__main__':
    main()
