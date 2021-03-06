from functools import partial

from midi_utils import m_to_s
from simple_controller_base import SimpleControllerBase


class PMIDIPD30(SimpleControllerBase):

  def __init__(self, c_instance):
    super(PMIDIPD30, self).__init__(c_instance)

  def _setup(self):
    # Set up transport.
    self._register_trigger(self.__toggle_record, 44)
    self._register_trigger(self.song.start_playing, 45)
    self._register_trigger(self.song.stop_playing, 46)
    self._register_trigger(self.song.jump_to_prev_cue, 47)
    self._register_trigger(self.song.jump_to_next_cue, 48)
    self._register_trigger(self.song.set_or_delete_cue, 49)
    # Set up crossfader.
    self._register_slider(self.__set_crossfader, 9)
    self._register_trigger(partial(self.__set_crossfader, 0), 67)
    self._register_trigger(partial(self.__set_crossfader, 127), 64)
    # Live 10 capture functionality.
    self._register_trigger(self.song.capture_midi, 1)
    # Set up a property listener, just because we can.
    self._register_listener(self.__log_play_state, self.song, 'is_playing')

  def __toggle_record(self):
    self.song.record_mode = not self.song.record_mode

  def __set_crossfader(self, value):
    self.song.master_track.mixer_device.crossfader.value = m_to_s(value)

  def __log_play_state(self):
    self._log_message('play state:', self.song.is_playing)
