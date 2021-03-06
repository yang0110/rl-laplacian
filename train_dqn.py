import os
import argparse
import importlib

from rl_lap.agent import dqn_agent

from rl_lap.tools import flag_tools
from rl_lap.tools import timer_tools
from rl_lap.tools import logging_tools


parser = argparse.ArgumentParser()
parser.add_argument('--log_base_dir', type=str, 
        default=os.path.join(os.getcwd(), 'log'))
parser.add_argument('--log_sub_dir', type=str, default='test')
parser.add_argument('--env_id', type=str, default='OneRoom')
parser.add_argument('--config_dir', type=str, default='rl_lap.configs')
parser.add_argument('--config_file', 
        type=str, default='dqn_config_gridworld')
parser.add_argument('--exp_name', type=str, default='dqn')
parser.add_argument('--args', type=str, action='append', default=[])

FLAGS = parser.parse_args()


def get_config_cls():
    config_module = importlib.import_module(
            FLAGS.config_dir+'.'+FLAGS.config_file)
    config_cls = config_module.Config
    return config_cls


def main():
    timer = timer_tools.Timer()
    if FLAGS.log_sub_dir == 'auto_d':
        FLAGS.log_sub_dir = logging_tools.get_datetime()
    if FLAGS.log_sub_dir == 'auto_n':
        FLAGS.log_sub_dir = logging_tools.get_unique_dir()
    # pass args to config
    cfg_cls = get_config_cls()
    flags = flag_tools.Flags()
    flags.log_dir = os.path.join(
            FLAGS.log_base_dir,
            FLAGS.exp_name,
            FLAGS.env_id,
            FLAGS.log_sub_dir)
    flags.env_id = FLAGS.env_id
    flags.args = FLAGS.args
    logging_tools.config_logging(flags.log_dir)
    cfg = cfg_cls(flags)
    flag_tools.save_flags(cfg.flags, flags.log_dir)
    agent = dqn_agent.DqnAgent(**cfg.args)
    agent.train()
    print('Total time cost: {:.4g}s.'.format(timer.time_cost()))


if __name__ == '__main__':
    main()
