import cProfile
import pstats
from competition import profile

cProfile.run('profile()', 'profile_output')
