import numpy as np
import gym
import gym_merged

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

import tensorflow as tf
tf.compat.v1.disable_eager_execution()

env = gym.make('gym_merged:merged-v0')
np.random.seed(123)
env.seed(123)
nb_actions = env.action_space.n

model = Sequential()
print(env.observation_space)
model.add(Flatten(input_shape=(1,)+env.observation_space.shape))
model.add(Dense(27))
model.add(Activation('relu'))
model.add(Dense(27))
model.add(Activation('relu'))
model.add(Dense(27))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('softmax'))
print(model.summary())

memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

dqn.fit(env, nb_steps=50000, visualize=True, verbose=1)

dqn.save_weights('dqn_{}_weights.h5f'.format(ENV_NAME), overwrite=True)

dqn.test(env, nb_episodes=5, visualize=True)


fit(self, env, nb_steps, action_repetition=1, callbacks=None, verbose=1, visualize=False, nb_max_start_steps=0, start_step_policy=None, log_interval=10000, nb_max_episode_steps=None)


