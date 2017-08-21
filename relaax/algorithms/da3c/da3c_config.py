from relaax.common.python.config.loaded_config import options

config = options.get('algorithm')

for key, value in [('use_convolutions', [])]:
    if not hasattr(config, key):
        setattr(config, key, value)

config.output.scale = options.get('algorithm/output/scale', 1.0)
config.output.loss_type = options.get('algorithm/output/loss_type', 'Normal')
config.optimizer = options.get('algorithm/optimizer', 'Adam')
config.use_icm = options.get('algorithm/use_icm', False)
config.use_gae = options.get('algorithm/use_gae', False)
config.output.action_high = options.get('algorithm/output/action_high', [])
config.output.action_low = options.get('algorithm/output/action_low', [])
config.gradients_norm_clipping = options.get('algorithm/gradients_norm_clipping', False)

# ICM parameters
config.icm.nu = options.get('algorithm/icm/nu', 0.8)
config.icm.alpha = options.get('algorithm/icm/alpha', 0.1)
config.icm.beta = options.get('algorithm/icm/beta', 0.2)
