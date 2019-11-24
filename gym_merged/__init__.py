from gym.envs.registration import register

register(
    id='merged-v0',
    entry_point='gym_merged.envs:MergedEnv',
)
register(
    id='merged-extrahard-v0',
    entry_point='gym_merged.envs:MergedExtraHardEnv',
)
