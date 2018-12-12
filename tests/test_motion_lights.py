import pytest
from apps.motion_light import MotionLight
# from apps.demo_class import MotionLight

# Important:
# For this example to work, do not forget to copy the `conftest.py` file.
# See README.md for more info
TEST_LIGHT = 'light.test_light';
TEST_SENSOR = 'binary_sensor.test_sensor';
DELAY = 120;
@pytest.fixture
def motion_light(given_that):
    motion_light = MotionLight(None, None, None, None, None, None, None, None)
    given_that.passed_arg('__name__').is_set_to('david')
    given_that.passed_arg('delay').is_set_to(DELAY)
    given_that.time_is(0)
    return motion_light


    
def test_basic(given_that, motion_light, assert_that, time_travel):
    given_that.passed_arg('entity').is_set_to(TEST_LIGHT)
    motion_light.initialize()
    given_that.mock_functions_are_cleared()
    given_that.state_of(TEST_LIGHT).is_set_to('off') 
    given_that.state_of(TEST_SENSOR).is_set_to('off') 
    
    time_travel.assert_current_time(0).seconds();

    # Initial Motion
    motion_light.motion('binary_sensor.test_sensor', None, 'off', 'on', None)
    motion_light.motion('binary_sensor.test_sensor', None, 'on', 'off', None)
    # assert_that('light/turn_on').was.called_with(entity_id=TEST_LIGHT)
    assert_that(TEST_LIGHT).was.turned_on()


    time_travel.fast_forward(DELAY/2).seconds()
    assert_that('light.test_light').was_not.turned_off()

    # New motion
    motion_light.motion('binary_sensor.test_sensor', None, 'off', 'on', None)
    motion_light.motion('binary_sensor.test_sensor', None, 'on', 'off', None)
    assert_that('light.test_light').was_not.turned_off()
    time_travel.fast_forward(DELAY).seconds()

    # given_that.state_of('light.test_light').is_set_to('on') 

    
    time_travel.assert_current_time(DELAY+DELAY/2).seconds()

    assert_that('light.test_light').was.turned_off()